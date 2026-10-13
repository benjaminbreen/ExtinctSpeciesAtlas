import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('pilot', Path(__file__).resolve().parents[1] / 'scripts/pilot.py')
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)

class PilotTests(unittest.TestCase):
    def test_historical_ocr_normalization(self):
        self.assertEqual(pilot.normalize('Lori-\nrojo; ſilphium; Camagüey'), 'lorirojo; silphium; camaguey')

    def test_boolean_search_preserves_or_operator(self):
        with tempfile.TemporaryDirectory() as td:
            previous = pilot.DERIVED
            pilot.DERIVED = Path(td)
            try:
                data = [dict(page_id=str(i),source_id='test',scan_url='https://example.org',printed_page=None,text=t) for i,t in enumerate(['macaw','tortoise','macaw tortoise'])]
                (pilot.DERIVED/'pages.jsonl').write_text(''.join(json.dumps(p)+'\n' for p in data))
                with contextlib.redirect_stdout(io.StringIO()):pilot.index()
                out = io.StringIO()
                with contextlib.redirect_stdout(out):pilot.search('macaw OR tortoise', 10)
                self.assertEqual(len(json.loads(out.getvalue())['results']),3)
                out = io.StringIO()
                with contextlib.redirect_stdout(out):pilot.search('macaw AND tortoise', 10)
                self.assertEqual(len(json.loads(out.getvalue())['results']),1)
            finally:pilot.DERIVED = previous

    def extraction_fixture(self, scan_xml):
        with tempfile.TemporaryDirectory() as td:
            previous = pilot.RAW, pilot.DERIVED, pilot.RESULTS
            pilot.RAW, pilot.DERIVED, pilot.RESULTS = [Path(td)/x for x in ['raw','derived','results']]
            try:
                folder = pilot.RAW/'internet-archive'/'test'
                folder.mkdir(parents=True)
                (folder/'ocr.xml').write_text('<DJVU><OBJECT><LINE><WORD>tortoise</WORD></LINE></OBJECT></DJVU>')
                (folder/'scandata.xml').write_text(scan_xml)
                pilot.write(pilot.RESULTS/'acquisition_manifest.json',[dict(source_id='test',ia_identifier='test',status='downloaded')])
                with contextlib.redirect_stdout(io.StringIO()):pilot.extract()
                return next(pilot.pages())
            finally:pilot.RAW, pilot.DERIVED, pilot.RESULTS = previous

    def test_scan_mapping_skips_excluded_leaves(self):
        page=self.extraction_fixture('<book><pageData><page leafNum="0"><addToAccessFormats>false</addToAccessFormats></page><page leafNum="7"><pageNumber>32</pageNumber></page></pageData></book>')
        self.assertEqual(page['scan_leaf'],7)
        self.assertEqual(page['printed_page'],'32')
        self.assertIn('/page/n7/',page['scan_url'])

    def test_scan_mapping_mismatch_never_invents_page_link(self):
        page=self.extraction_fixture('<book><pageData><page leafNum="0"/><page leafNum="7"/></pageData></book>')
        self.assertIsNone(page['scan_leaf'])
        self.assertNotIn('/page/n',page['scan_url'])

if __name__ == '__main__':unittest.main()
