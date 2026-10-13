"""Record an explicit page-level review decision without changing generated results."""
import argparse
from datetime import datetime, timezone
import engine


def record_decision(case, scan_id, status, novelty, note, reviewer):
    if status not in ("unreviewed", "needs_scan_check", "needs_literature_check", "reviewed"):
        raise ValueError("unknown review status")
    if novelty not in ("not_assessed", "known", "possible_new", "rejected"):
        raise ValueError("unknown novelty status")
    if not note.strip() or not reviewer.strip():
        raise ValueError("reviewer and explanatory note are required")
    candidates = engine.jsonl(case["_out"] / "candidates.jsonl")
    candidate = next((c for c in candidates if c["scan_id"] == scan_id), None)
    if not candidate:
        raise ValueError("page is not in the generated candidate queue")
    ledger = engine.load_reviews(case)
    previous = ledger["decisions"].get(scan_id, {})
    decision = {"scope": "page", "review_status": status, "novelty_status": novelty,
                "note": note, "reviewer": reviewer,
                "text_sha256": engine.text_hash(candidate["page"]["text"]),
                "updated_at": datetime.now(timezone.utc).isoformat()}
    decision["history"] = previous.get("history", []) + ([{k: v for k, v in previous.items() if k != "history"}] if previous else [])
    ledger["decisions"][scan_id] = decision
    path = engine.review_path(case)
    path.parent.mkdir(parents=True, exist_ok=True)
    engine.atomic_json(path, ledger)
    return path


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("case"); ap.add_argument("scan_id")
    ap.add_argument("--status", required=True, choices=["unreviewed", "needs_scan_check", "needs_literature_check", "reviewed"])
    ap.add_argument("--novelty", default="not_assessed", choices=["not_assessed", "known", "possible_new", "rejected"])
    ap.add_argument("--note", required=True); ap.add_argument("--reviewer", required=True)
    args = ap.parse_args()
    print(record_decision(engine.load_case(args.case), args.scan_id, args.status, args.novelty, args.note, args.reviewer))
