"""Publication checks for data relationships and generated local navigation."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from atlas_data import read, validate, authorities
from build_site import outputs, check_links, species_entry


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.passages = copy.deepcopy(read('passages'))

    def test_duplicate_passage_is_rejected(self):
        self.passages.append(copy.deepcopy(self.passages[0]))
        with self.assertRaisesRegex(ValueError, 'Duplicate passage'):
            validate(passages=self.passages)

    def test_unknown_authority_is_rejected(self):
        self.passages[0]['authority_id'] = 'missing-author'
        with self.assertRaisesRegex(ValueError, 'unknown authority'):
            validate(passages=self.passages)

    def test_catalog_cannot_point_to_wrong_source(self):
        self.passages[0]['catalog']['href'] = './source-newton.html'
        with self.assertRaisesRegex(ValueError, 'links disagree'):
            validate(passages=self.passages)

    def test_broken_annotation_is_rejected(self):
        self.passages[0]['content']['note_targets'][0][1] = 'A phrase absent from this passage'
        with self.assertRaisesRegex(ValueError, 'note target missing'):
            validate(passages=self.passages)

    def test_unknown_source_relationship_is_rejected(self):
        self.passages[0]['research']['relationships'] = [{'type': 'translation_of', 'passage_id': 'missing'}]
        with self.assertRaisesRegex(ValueError, 'invalid related passage'):
            validate(passages=self.passages)

    def test_indexed_reference_does_not_become_full_source_page(self):
        result = outputs()
        for record in self.passages:
            if record['content'] is None:
                self.assertNotIn(f'source-{record["id"]}.html', result)
                self.assertIn(record['catalog']['href'].replace('&', '&amp;'), result[record['species_ids'][0]+'.html'])

    def test_authority_lists_cover_each_indexed_passage_once(self):
        self.assertEqual(sum(len(a['works']) for a in authorities()), len(self.passages))

    def test_count_uses_records_and_distinct_places(self):
        auk = next(s for s in read('species') if s['id'] == 'great-auk')
        # Removing a second St Kilda account changes the source count but not the place count.
        reduced = [r for r in self.passages if r['id'] != 'pennant']
        self.assertIn('4 sources · 3 places', species_entry(auk, reduced))

    def test_broken_local_anchor_blocks_publication(self):
        with self.assertRaisesRegex(ValueError, 'missing anchor'):
            check_links({'test.html': '<a href="./index.html#nonexistent-anchor">Broken</a>'})

    def test_duplicate_html_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate HTML id'):
            check_links({'test.html': '<p id="same"></p><p id="same"></p>'})

    def test_missing_scan_blocks_publication(self):
        record = next(r for r in self.passages if r['id'] == 'herbert')
        record['content']['scans'][1]['src'] = './assets/missing-page.webp'
        with self.assertRaisesRegex(ValueError, 'missing scan image'):
            validate(passages=self.passages)

    def test_translation_requires_credit(self):
        record = next(r for r in self.passages if r['id'] == 'clusius')
        del record['content']['translation_credit_html']
        with self.assertRaisesRegex(ValueError, 'translation credit required'):
            validate(passages=self.passages)

    def test_reader_omits_absent_notes_and_sets_language(self):
        html = outputs()['source-clusius.html']
        self.assertIn('lang="la"', html)
        self.assertIn('<h2>English</h2>', html)
        self.assertNotIn('href="#notes"', html)
        self.assertNotIn('id="fn-1"', html)

    def test_scan_controls_include_all_recorded_pages(self):
        result = outputs()
        for record in self.passages:
            content = record['content'] or {}
            scans = content.get('scans', [])
            if len(scans) > 1:
                html = result[record['page']]
                for scan in scans:
                    self.assertIn('data-scan-src="' + scan['src'] + '"', html)

    def test_committed_pages_match_build(self):
        root = Path(__file__).resolve().parents[1]
        for name, html in outputs().items():
            with self.subTest(page=name):
                self.assertEqual((root/name).read_text(encoding='utf-8'), html)

    def test_notes_cannot_include_another_species_passage(self):
        notes = copy.deepcopy(read('research-notes'))
        notes[0]['notes'][0]['passage_ids'] = ['pennant-bluebuck']
        with self.assertRaisesRegex(ValueError, 'cross-species'):
            validate(notes=notes)

    def test_notes_require_reviewed_text_and_a_scan(self):
        record = next(r for r in self.passages if r['id'] == 'tyssen-warrah')
        record['research']['reviewed_on'] = None
        with self.assertRaisesRegex(ValueError, 'require a reviewed passage and scans'):
            validate(passages=self.passages)
        record['research']['reviewed_on'] = '2026-10-03'
        record['content']['scans'] = []
        with self.assertRaisesRegex(ValueError, 'require a reviewed passage and scans'):
            validate(passages=self.passages)

    def test_notes_share_passage_text_and_exclude_research_metadata(self):
        from html import escape
        result = outputs()
        for group in read('research-notes'):
            html = result[group['page']]
            for note in group['notes']:
                for pid in note['passage_ids']:
                    record = next(r for r in self.passages if r['id'] == pid)
                    for paragraph in record['content']['paragraphs']:
                        self.assertIn(escape(paragraph), html)
                    self.assertNotIn(record['research']['reviewed_by'], html)
                    self.assertIn(record['page'], html)

    def test_species_without_dossier_can_link_to_notes(self):
        warrah = next(s for s in read('species') if s['id'] == 'warrah')
        row = species_entry(warrah, self.passages)
        self.assertIn('href="./research-notes-warrah.html"', row)
        self.assertIn('Research notes', row)
        self.assertNotIn('Dossier in preparation', row)


if __name__ == '__main__':
    unittest.main()
