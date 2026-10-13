"""Passage-level variant of embed_gifts.py: embed ~500-character windows around each
animal word in the gift/cargo page pool, so single-line mentions are not diluted by
the rest of the page. Outputs in results/embed_gifts/windows*.

    python3 research/extinction-pilot/scripts/embed_gift_windows.py build|embed|rank
"""
import array, json, math, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from embed_mauritius import key, embed, DIM  # noqa: E402
from embed_gifts import OUT, QUERIES  # noqa: E402

CUE = re.compile(r"(?i)\b(vogel\w*|gevogelte|gedier\w*|levend\w*|dieren|beest\w*|casu\w*ar\w*|casuw\w*|swaen|swanen|"
                 r"stru[iy]j?s\w*|hert|harten|hinde\w*|porco|dodaer\w*|dodeer\w*|doders\w*|dronte\w*|walg\w*|"
                 r"papega\w*|aep|apen)\b")
HALF = 250


def build():
    out = []
    for line in open(OUT / "pages.jsonl"):
        p = json.loads(line); t = p["text"]; last_end = -1
        for m in CUE.finditer(t):
            a, b = max(0, m.start() - HALF), min(len(t), m.end() + HALF)
            if a < last_end:  # merge overlapping windows
                out[-1]["text"] = t[out[-1]["start"]:b]; out[-1]["end"] = b; last_end = b; continue
            out.append({"scan_id": p["scan_id"], "volume_years": p["volume_years"], "start": a, "end": b, "text": t[a:b]})
            last_end = b
    json.dump(out, open(OUT / "windows.json", "w"), ensure_ascii=False)
    print(len(out), "windows", sum(len(w["text"]) for w in out) // 1000, "k chars")


def do_embed():
    k = key(); ws = json.load(open(OUT / "windows.json"))
    batches = [ws[i:i + 96] for i in range(0, len(ws), 96)]
    tokens = 0
    with ThreadPoolExecutor(4) as pool, open(OUT / "windows.f32", "wb") as vf:
        for vecs, t in pool.map(lambda b: embed([w["text"] for w in b], k), batches):
            array.array("f", [x for v in vecs for x in v]).tofile(vf); tokens += t
    print("tokens", tokens, "approx $%.2f" % (tokens / 1e6 * 0.13))


def rank(per_query=40):
    ws = json.load(open(OUT / "windows.json"))
    raw = array.array("f"); raw.frombytes((OUT / "windows.f32").read_bytes())
    q = json.load(open(OUT / "queries.json"))["queries"]
    qn = {k: [x / math.sqrt(sum(y * y for y in v)) for x in v] for k, v in q.items()}
    best = {}
    for i, w in enumerate(ws):
        v = raw[i * DIM:(i + 1) * DIM]; n = math.sqrt(sum(x * x for x in v))
        s = max(sum(a * b for a, b in zip(qq, v)) / n for qq in qn.values())
        if s > best.get(w["scan_id"], (0,))[0]:
            best[w["scan_id"]] = (s, w)
    order = sorted(best.values(), key=lambda x: -x[0])
    json.dump([{"scan_id": w["scan_id"], "volume_years": w["volume_years"], "score": round(s, 4), "window": w["text"]}
               for s, w in order[:400]], open(OUT / "window_candidates.json", "w"), ensure_ascii=False, indent=1)
    ids = [w["scan_id"] for s, w in order]
    for k in ["1164_0738", "1165_0143", "3992_0916"]:
        sid = "NL-HaNA_1.04.02_" + k; print(k, ids.index(sid) + 1 if sid in ids else "-", "of", len(ids))


if __name__ == "__main__":
    {"build": build, "embed": do_embed, "rank": rank}[sys.argv[1]]()
