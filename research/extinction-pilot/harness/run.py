"""CLI: python3 research/extinction-pilot/harness/run.py <case> <stage|all> [--budget USD] [--yes]"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine, corpora

ap = argparse.ArgumentParser()
ap.add_argument("case"); ap.add_argument("stage", choices=list(engine.STAGES) + ["all", "local"])
ap.add_argument("--budget", type=float, default=5.0, help="USD ceiling per paid stage")
ap.add_argument("--yes", action="store_true", help="run a paid stage even if over budget")
a = ap.parse_args()
case = engine.load_case(a.case)
corpus = corpora.get(case["corpus"]["adapter"], case["corpus"])
stages = {"all": list(engine.STAGES), "local": ["scope", "sweep", "report"]}.get(a.stage, [a.stage])
for s in stages:
    print(f"== {s}")
    engine.STAGES[s](case, corpus, budget=a.budget, yes=a.yes)
