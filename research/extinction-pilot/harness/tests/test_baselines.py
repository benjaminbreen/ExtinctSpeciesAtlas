"""Protect distinctions in Cheke and Parish's Table A1 reconciliation."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BaselineEvidence(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'baselines/dodo.json').read_text())
        self.records = {r['record_id']: r for r in self.data['records']}

    def test_dodo_names_do_not_override_described_red_hens(self):
        for rid in ('dodo-1666-1669-johannes-pretorius', 'dodo-1668-john-marshall', 'dodo-1673-1675-johann-c-hoffmann'):
            with self.subTest(record=rid):
                r = self.records[rid]
                self.assertEqual(r['taxa'], ['red-hen'])
                self.assertEqual(r['identification']['proposed_taxa'], ['red-hen'])
                self.assertTrue(r['names_used']['dodo_column'])

    def test_undescribed_late_birds_keep_uncertainty(self):
        for rid in ('dodo-1681-benjamin-harry', 'dodo-1685-1688-isaac-j-lamotius'):
            with self.subTest(record=rid):
                r = self.records[rid]
                self.assertEqual(r['taxa'], [])
                self.assertEqual(r['identification']['certainty'], 'probable')
                self.assertEqual(r['identification']['proposed_taxa'], ['red-hen'])

    def test_hugo_report_is_not_a_current_sighting(self):
        r = self.records['dodo-1673-1677-hubert-hugo']
        self.assertEqual(r['taxa'], [])
        self.assertEqual(r['identification_components'][1]['evidence_type'], 'reported_absence_among_current_residents')

    def test_reconciliation_preserves_rows_locators_and_date_discrepancy(self):
        self.assertEqual(len(self.records), 32)
        for r in self.records.values():
            self.assertEqual(r['identification']['authority'], 'cheke-parish-2020')
            self.assertTrue(r['baseline_locator'].startswith('Table A1, p.'))
        self.assertIn('1693–1696', self.records['dodo-1691-francois-leguat']['date_qualification'])


if __name__ == '__main__':
    unittest.main()
