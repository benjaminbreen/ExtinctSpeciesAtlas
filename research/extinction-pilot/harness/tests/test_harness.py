"""python3 -m unittest discover -s research/extinction-pilot/harness/tests -v
The recall test runs the dodo sweep over local GLOBALISE (about 90 s) and is skipped if the index is absent."""
import json, sys, unittest
from pathlib import Path
H = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(H))
import engine, corpora
from corpora.globalise import DB

class Units(unittest.TestCase):
    def test_lev(self):
        self.assertEqual(engine.lev_within("dodersen", "dodeersen", 2), 1)
        self.assertIsNone(engine.lev_within("dodaers", "doctoren", 2))
    def test_neighbour(self):
        self.assertEqual(engine.neighbour("NL-HaNA_1.04.02_4005_0603", 1), "NL-HaNA_1.04.02_4005_0604")

@unittest.skipUnless(DB.exists(), "GLOBALISE index not available")
class Recall(unittest.TestCase):
    def test_dodo_sweep_recovers_all_planted(self):
        case = engine.load_case("dodo-globalise")
        engine.stage_sweep(case, corpora.get("globalise"))
        r = json.loads((case["_out"] / "recall.json").read_text())["sweep"]
        self.assertEqual(r["recovered"], r["planted"])
