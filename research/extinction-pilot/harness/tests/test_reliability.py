"""Regression tests for evidence validation, coverage, and checkpoint recovery."""
import array
import copy
import json
import math
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import engine
import review
from corpora.globalise import Globalise
from corpora.tanap import parse_volume


class Corpus:
    def __init__(self, pages):
        self.pages = pages
    def identity(self):
        return {'fixture': 1}
    def page(self, scan):
        return next((p for p in self.pages if p['scan_id'] == scan), None)


def response(content, reason='stop'):
    return {'choices': [{'message': {'content': content}, 'finish_reason': reason}],
            'usage': {'prompt_tokens': 10, 'completion_tokens': 5}}


class Reliability(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name)
        self.case = {'case_id': 'fixture', '_out': self.out, 'title': 'fixture', 'baseline': 'fixture.json',
            'corpus': {'adapter': 'globalise'}, 'scope': {}, 'sweep': {}, 'queries': {'q': 'a bird'},
            'embed': {'dimensions': 3, 'window_chars': 1000, 'overlap_chars': 100},
            'screen': {'prompt': 'Read birds.', 'categories': ['dodo'], 'source': 'both',
                       'window_chars': 500, 'overlap_chars': 50, 'per_call': 2, 'threads': 1},
            'planted': []}
        self.pages = [{'scan_id': 'archive_0002', 'text': 'Some textiles aboard the ship.',
                       'terms': ['textiles'], 'url': 'https://example.org/scan', 'years': [1700, 1700]}]
        self.corpus = Corpus(self.pages)
        self.save_inputs()

    def save_inputs(self):
        for stage in ('pool', 'sweep'):
            engine.save_pages(self.case, self.corpus, stage, self.pages)

    def screen(self, payload):
        with patch.object(engine, 'api_key', return_value='mock'), patch.object(engine, 'post', return_value=payload) as post:
            engine.stage_screen(self.case, self.corpus)
            return post.call_count

    def test_invented_quote_is_rejected_and_audited(self):
        self.screen(response(json.dumps({'flags': [{'id': 0, 'category': 'dodo', 'quote': '1 dodeers'}]})))
        self.assertEqual(engine.jsonl(self.out / 'screen.jsonl'), [])
        self.assertEqual(engine.jsonl(self.out / 'screen_rejected.jsonl')[0]['reason'], 'quotation absent from input')

    def test_whitespace_matching_preserves_exact_offsets(self):
        self.pages[0]['text'] = 'Before\n1   dodeers\nafter'
        self.save_inputs()
        self.screen(response(json.dumps({'flags': [{'id': 0, 'category': 'dodo', 'quote': '1 dodeers'}]})))
        flag = engine.jsonl(self.out / 'screen.jsonl')[0]
        self.assertEqual(flag['quote'], '1   dodeers')
        self.assertEqual(self.pages[0]['text'][flag['quote_start']:flag['quote_end']], flag['quote'])
        self.assertEqual(flag['verification'], 'matched_machine_text')

    def test_bad_json_retries_on_resume(self):
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            self.screen(response('not json'))
        self.assertEqual(engine.jsonl(self.out / 'screen_raw.jsonl')[0]['status'], 'failed')
        self.assertEqual(self.screen(response('{"flags":[]}')), 1)
        self.assertEqual(self.screen(response('{"flags":[]}')), 0)

    def test_truncated_model_response_is_not_complete(self):
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            self.screen(response('{"flags":[]}', 'length'))

    def test_changed_prompt_refuses_checkpoint_reuse(self):
        self.screen(response('{"flags":[]}'))
        self.case['screen']['prompt'] = 'Changed reading task.'
        with self.assertRaisesRegex(ValueError, 'inputs/settings changed'):
            self.screen(response('{"flags":[]}'))

    def test_same_size_changed_pool_refuses_reuse(self):
        self.screen(response('{"flags":[]}'))
        self.pages[0]['text'] = 'A changed page, with the same scan ID.'
        self.save_inputs()
        with self.assertRaisesRegex(ValueError, 'inputs/settings changed'):
            self.screen(response('{"flags":[]}'))

    def test_missing_or_stale_local_input_is_refused(self):
        self.case['scope']['years'] = [1600, 1700]
        with self.assertRaisesRegex(ValueError, 'inputs changed'):
            engine.screen_pages(self.case, self.corpus)
        (self.out / 'pool.meta.json').unlink()
        with self.assertRaisesRegex(ValueError, 'legacy'):
            engine.screen_pages(self.case, self.corpus)

    def test_full_text_wins_over_truncated_copy(self):
        full = dict(self.pages[0], text='x' * 7000 + ' 1 dodeers')
        self.corpus.pages = [full]
        engine.save_pages(self.case, self.corpus, 'pool', [dict(full, text=full['text'][:6000])])
        engine.save_pages(self.case, self.corpus, 'sweep', [full])
        self.assertEqual(engine.screen_pages(self.case, self.corpus)[0]['text'], full['text'])
        self.assertTrue(any('dodeers' in w for w in engine.windows(full['text'])))

    def test_invalid_window_configuration_raises(self):
        with self.assertRaises(ValueError):
            engine.windows('abc', size=200, overlap=200)

    def test_normalization_uses_one_norm_and_rejects_zero(self):
        with patch.object(engine.math, 'sqrt', wraps=math.sqrt) as sqrt:
            self.assertEqual(engine.normalize_vector([3, 4]), [.6, .8])
            self.assertEqual(sqrt.call_count, 1)
        with self.assertRaises(ValueError):
            engine.normalize_vector([0, 0])

    def embed(self):
        def post(url, body, key):
            return {'data': [{'index': i, 'embedding': [1., 0., 0.]} for i, _ in enumerate(body['input'])],
                    'usage': {'total_tokens': 10}}
        with patch.object(engine, 'api_key', return_value='mock'), patch.object(engine, 'post', side_effect=post) as api:
            engine.stage_embed(self.case, self.corpus)
            return api.call_count

    def test_embedding_recovers_uncommitted_vector_tail(self):
        self.embed()
        path = self.out / 'vectors.f32'
        size = path.stat().st_size
        with open(path, 'ab') as f:
            array.array('f', [99.]).tofile(f)
        self.assertEqual(self.embed(), 0)
        self.assertEqual(path.stat().st_size, size)

    def test_embedding_rejects_same_count_changed_text(self):
        self.embed()
        self.pages[0]['text'] = 'Different text.'
        self.save_inputs()
        with self.assertRaisesRegex(ValueError, 'inputs/settings changed'):
            self.embed()

    def test_embedding_covers_page_tail(self):
        self.pages[0]['text'] = 'x' * 7000 + ' 1 dodeers'
        self.save_inputs()
        inputs = []
        def post(url, body, key):
            inputs.extend(body['input'])
            return {'data': [{'index': i, 'embedding': [1., 0., 0.]} for i, _ in enumerate(body['input'])], 'usage': {'total_tokens': 1}}
        with patch.object(engine, 'api_key', return_value='mock'), patch.object(engine, 'post', side_effect=post):
            engine.stage_embed(self.case, self.corpus)
        self.assertTrue(any('dodeers' in text for text in inputs))

    def test_partial_journal_tail_is_recovered(self):
        path = self.out / 'journal.jsonl'
        path.write_bytes(b'{"batch":0}\n{"batch":')
        self.assertEqual(engine.read_journal(path), [{'batch': 0}])
        self.assertEqual(path.read_bytes(), b'{"batch":0}\n')
        path.write_bytes(b'not json\n')
        with self.assertRaises(json.JSONDecodeError):
            engine.read_journal(path)

    def test_neighbour_and_planted_find_remain_pending(self):
        self.case['planted'] = [{'scan_id': 'archive_0002', 'label': 'pilot find'}]
        baseline = {'records': [{'record_id': 'known', 'match_keys': {'globalise_scans': ['archive_0001']}}]}
        with patch.object(engine, 'baseline', return_value=baseline):
            engine.stage_report(self.case, self.corpus)
        row = engine.jsonl(self.out / 'candidates.jsonl')[0]
        self.assertEqual(row['baseline_matches'][0]['status'], 'possible_context')
        self.assertIn('Pending review (1 pages)', (self.out / 'report.md').read_text())

    def test_known_page_does_not_claim_exact_passage(self):
        baseline = {'records': [{'record_id': 'known', 'match_keys': {'globalise_scans': ['archive_0002']}}]}
        with patch.object(engine, 'baseline', return_value=baseline):
            matches = engine.baseline_matches(self.case, self.pages[0])
        self.assertEqual(matches[0]['status'], 'known_page')

    def test_exact_passage_key_requires_matching_quote(self):
        keys = {'passages': [{'adapter': 'globalise', 'scan_id': 'archive_0002', 'quote': 'absent'}]}
        baseline = {'records': [{'record_id': 'known', 'match_keys': keys}]}
        with patch.object(engine, 'baseline', return_value=baseline):
            self.assertEqual(engine.baseline_matches(self.case, self.pages[0]), [])
            keys['passages'][0]['quote'] = 'textiles aboard'
            self.assertEqual(engine.baseline_matches(self.case, self.pages[0])[0]['status'], 'exact_passage')

    def test_ledger_survives_report_and_flags_changed_text(self):
        ledger = self.out / 'reviews.json'
        with patch.object(engine, 'review_path', return_value=ledger), patch.object(engine, 'baseline', return_value={'records': []}):
            engine.stage_report(self.case, self.corpus)
            review.record_decision(self.case, 'archive_0002', 'reviewed', 'rejected', 'Textiles only.', 'fixture reviewer')
            before = ledger.read_bytes()
            engine.stage_report(self.case, self.corpus)
            self.assertEqual(ledger.read_bytes(), before)
            self.pages[0]['text'] += ' New transcription.'
            self.save_inputs()
            engine.stage_report(self.case, self.corpus)
            self.assertTrue(engine.jsonl(self.out / 'candidates.jsonl')[0]['review_stale'])

    def test_no_controls_is_explicitly_unevaluated(self):
        self.assertEqual(engine.recall_line(self.case, 'sweep', {})['evaluation'], 'not_evaluated')

    def test_globalise_overlap_and_full_text(self):
        path = self.out / 'globalise.sqlite'
        db = sqlite3.connect(path)
        db.executescript('create table catalogue(inventory text,year_start integer,year_end integer);'
                         'create table pages(scan_id text,inventory text,sequence integer,text text,token_count integer);')
        db.execute('insert into catalogue values(?,?,?)', ('1', 1640, 1660))
        db.execute('insert into pages values(?,?,?,?,?)', ('scan_0001', '1', 1, 'x' * 9000, 100))
        db.commit(); db.close()
        c = Globalise({'path': str(path)})
        self.addCleanup(c.db.close)
        rows = c.scope({'years': [1652, 1653], 'volumes': {'all_volumes': True}})
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(rows[0]['text']), 9000)

    def test_tanap_notes_dates_and_locators(self):
        root = self.out / 'tanap'; root.mkdir()
        path = root / 'C001_v1.20.md'
        path.write_text('## C. 1, pp. 7-10.\n\n{16520408} Some <span>hartebeesten</span>.[^1]\n\n'
                        '## C. 1, p. 11.\n\n{16520409} Textiles only.\n\n[^1]: A later bluebuck editorial note.\n')
        rows = list(parse_volume(path, root))
        self.assertEqual(rows[0]['document_date'], '1652-04-08')
        self.assertNotIn('bluebuck', rows[0]['text'])
        self.assertIn('bluebuck', rows[0]['editorial_notes'])
        self.assertFalse(rows[1]['editorial_notes'])
        self.assertIsNone(rows[0]['scan_url'])
        self.assertEqual(rows[0]['scan_id'], 'TANAP_C001_p0007-0010_d16520408')

    def test_tanap_alternative_locators_are_separate_sections(self):
        root = self.out / 'tanap'; root.mkdir()
        path = root / 'C001_v1.20.md'
        path.write_text('## C. 1., pp, 7-10.\n\n{16520408} First.\n\n'
                        '## Haagse Kopie, Fol. 520-526\n\n{16520409} Second.\n\n'
                        '## V.C. 12, pp. 9-10.\n\n{16890101} Third.\n')
        rows = list(parse_volume(path, root))
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1]['inventory'], 'Hague-C001')
        self.assertEqual(rows[2]['inventory'], 'VC012')
        self.assertNotIn('Second', rows[0]['text'])

    def test_tanap_unrecognized_heading_is_not_silently_merged(self):
        root = self.out / 'tanap'; root.mkdir()
        path = root / 'C001_v1.20.md'
        path.write_text('## An unrecognized edition locator\n\nSome text.\n')
        with self.assertRaisesRegex(ValueError, 'unrecognized edition heading'):
            list(parse_volume(path, root))

    def test_tanap_unknown_day_preserves_month_precision(self):
        root = self.out / 'tanap'; root.mkdir()
        path = root / 'C019_v1.20.md'
        path.write_text('## C. 19, pp. 119-120.\n\n{16880400} Unknown day.\n')
        row = list(parse_volume(path, root))[0]
        self.assertEqual(row['document_date'], '1688-04')
        self.assertEqual(row['document_date_precision'], 'month')
        self.assertEqual(row['date_tag'], '{16880400}')
        self.assertEqual(row['scan_id'], 'TANAP_C019_p0119-0120_d16880400')

    def test_report_refuses_changed_screening_inputs(self):
        self.screen(response('{"flags":[]}'))
        self.case['screen']['prompt'] = 'Changed task.'
        with self.assertRaisesRegex(ValueError, 'stale or incomplete'):
            engine.read_paid_output(self.case, self.corpus, 'screen')

    def test_embedding_ranking_changes_require_regeneration(self):
        self.embed()
        self.case['embed_top_per_query'] = 1
        with self.assertRaisesRegex(ValueError, 'ranking selection changed'):
            engine.read_paid_output(self.case, self.corpus, 'embed')

    def test_screen_control_requires_expected_category(self):
        self.case['planted'] = [{'scan_id': 'archive_0002', 'label': 'game control',
                                'expected_categories': ['game_list']}]
        self.screen(response(json.dumps({'flags': [{'id': 0, 'category': 'dodo', 'quote': 'textiles'}]})))
        recall = json.loads((self.out / 'recall.json').read_text())['screen']
        self.assertEqual(recall['recovered'], 0)
        self.assertEqual(recall['planted'], 1)

    def test_model_category_does_not_become_accepted_evidence(self):
        self.pages[0]['text'] = '1 dodeers'
        self.save_inputs()
        self.screen(response(json.dumps({'flags': [{'id': 0, 'category': 'dodo', 'quote': '1 dodeers'}]})))
        with patch.object(engine, 'baseline', return_value={'records': []}):
            engine.stage_report(self.case, self.corpus)
        draft = engine.jsonl(self.out / 'evidence_records.jsonl')[0]
        self.assertEqual(draft['taxon_ids'], [])
        self.assertEqual(draft['review_status'], 'unreviewed')
        self.assertEqual(draft['novelty_status'], 'not_assessed')
        self.assertEqual(draft['machine_verification'], 'matched_machine_text')


if __name__ == '__main__':
    unittest.main()
