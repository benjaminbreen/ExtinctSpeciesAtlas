"""Small comparison of OpenAI embedding models on a GLOBALISE Mauritius/Cape sample.

Builds a ~3,000-page pool (random place-filtered pages, keyword fauna pages, and
the seven pages of Pretorius's 1669 Mauritius report), embeds it with each model,
runs descriptive queries that avoid Pretorius's wording, and writes rankings plus
a blind judging sheet. Outputs go to results/embed_test/ (Git-ignored).

    python3 research/extinction-pilot/scripts/embed_test.py sample
    python3 research/extinction-pilot/scripts/embed_test.py embed
    python3 research/extinction-pilot/scripts/embed_test.py rank
"""
import json, math, random, sqlite3, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/extinction-pilot/results/embed_test"
VOC = Path.home() / "Code/Historical Mysteries/globalise-drugs/data/voc.sqlite"
MODELS = ["text-embedding-3-small", "text-embedding-3-large"]
PRETORIUS = [f"NL-HaNA_1.04.02_4005_{n:04d}" for n in range(600, 607)]
PLACES = ('mauritius OR mauritus OR mauritsius OR "goede hoop" OR caep OR cabo OR '
          'rodrigo OR "diego ruys" OR "isle de bourbon" OR mascarenhas OR mascarin*')
FAUNA = ('schildpad* OR dodaer* OR dodaars OR ganssen OR gansen OR walgvogel* OR '
         'hartebeest* OR elandt* OR zeekoe* OR flamingo* OR papegaeij* OR "wilde bocken" '
         'OR "wilt gevogelte" OR vogelen')
MAX_CHARS = 6000

# Written for this test; none quotes Pretorius.
QUERIES = {
    "q01_island_fauna": "Description of the wild animals and birds found on an island, which are good to eat and how they are caught.",
    "q02_tortoises": "Large land tortoises collected in great numbers by sailors and settlers for food.",
    "q03_flightless": "A large bird that cannot fly and is easily caught by hunters.",
    "q04_tame_birds": "Birds so tame and unafraid that they do not flee when people shoot at them.",
    "q05_nl_modern": "Beschrijving van de dieren en vogels op het eiland Mauritius en hoe men ze vangt.",
    "q06_fr": "Les oiseaux de cette île ne volent point; ils sont gros et on les prend facilement à la course.",
    "q07_cape_game": "Antelope and other wild game hunted near the Cape settlement.",
    "q08_depletion": "Hunting has exhausted the game; animals are now scarce near the fort and must be sought far away.",
    "q09_nl_early": "veel wilt gevogelte dat men met de hant can grijpen, ende schiltpadden die goet om eeten zijn",
    "q10_report": "A report on the island's natural resources: animals, birds, fish, trees, rivers and climate.",
}
PRETORIUS_QUERIES = {"q01_island_fauna", "q02_tortoises", "q03_flightless", "q04_tame_birds",
                     "q05_nl_modern", "q06_fr", "q09_nl_early", "q10_report"}


def key():
    for line in open(ROOT / ".env.local"):
        if line.startswith("OPENAI_API_KEY="):
            return line.split("=", 1)[1].strip().strip("\"'")
    raise SystemExit("OPENAI_API_KEY missing from .env.local")


def embed(model, texts, k):
    req = urllib.request.Request(
        "https://api.openai.com/v1/embeddings",
        data=json.dumps({"model": model, "input": texts}).encode(),
        headers={"Authorization": "Bearer " + k, "Content-Type": "application/json"})
    for attempt in range(6):
        try:
            r = json.load(urllib.request.urlopen(req, timeout=120))
            return [d["embedding"] for d in r["data"]], r["usage"]["total_tokens"]
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 5:
                time.sleep(2 ** attempt * 3); continue
            raise SystemExit(f"HTTP {e.code}: {e.read()[:300]}")


def sample():
    OUT.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(VOC)
    q = ("select scan_id, inventory, sequence, text from pages where token_count >= 40 and id in "
         "(select rowid from pages_fts where pages_fts match ?)")
    place = db.execute(q, (PLACES,)).fetchall()
    fauna = db.execute(q, (f"({PLACES}) AND ({FAUNA})",)).fetchall()
    rng = random.Random(1669)
    pool = {r[0]: ("pretorius", r) for r in db.execute(
        "select scan_id, inventory, sequence, text from pages where scan_id in (%s)" % ",".join("?" * 7), PRETORIUS)}
    for r in rng.sample(fauna, min(300, len(fauna))):
        pool.setdefault(r[0], ("fauna_keyword", r))
    for r in rng.sample(place, 2700):
        pool.setdefault(r[0], ("random_place", r))
    rows = [{"scan_id": s, "stratum": st, "inventory": r[1], "sequence": r[2], "text": r[3][:MAX_CHARS]}
            for s, (st, r) in pool.items()]
    with open(OUT / "pool.jsonl", "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    counts = {}
    for row in rows:
        counts[row["stratum"]] = counts.get(row["stratum"], 0) + 1
    print(len(place), "place pages;", len(fauna), "fauna-keyword pages; pool", counts)


def load_pool():
    return [json.loads(l) for l in open(OUT / "pool.jsonl")]


def do_embed():
    k, pool = key(), load_pool()
    for model in MODELS:
        path = OUT / f"vectors-{model}.json"
        if path.exists():
            print("cached", model); continue
        vecs, tokens = [], 0
        for i in range(0, len(pool), 64):
            v, t = embed(model, [p["text"] or " " for p in pool[i:i + 64]], k)
            vecs += v; tokens += t
        qv, qt = embed(model, list(QUERIES.values()), k)
        json.dump({"model": model, "tokens": tokens + qt, "pages": vecs,
                   "queries": dict(zip(QUERIES, qv))}, open(path, "w"))
        print(model, "tokens", tokens + qt)


def norm(v):
    n = math.sqrt(sum(x * x for x in v)); return [x / n for x in v]


def rank():
    pool = load_pool()
    results, judge = {}, {}
    for model in MODELS:
        d = json.load(open(OUT / f"vectors-{model}.json"))
        pages = [norm(v) for v in d["pages"]]
        results[model] = {"tokens": d["tokens"], "queries": {}}
        for qid, qv in d["queries"].items():
            qv = norm(qv)
            scores = sorted(((sum(a * b for a, b in zip(qv, p)), i) for i, p in enumerate(pages)), reverse=True)
            order = [pool[i]["scan_id"] for _, i in scores]
            pret = [order.index(s) + 1 for s in PRETORIUS if s in order]
            results[model]["queries"][qid] = {"top10": order[:10], "pretorius_ranks": sorted(pret)}
            for s in order[:10]:
                judge.setdefault(s, set()).add(qid)
    by_id = {p["scan_id"]: p for p in pool}
    rng = random.Random(7)
    items = list(judge.items()); rng.shuffle(items)
    sheet = [{"scan_id": s, "queries": {q: QUERIES[q] for q in sorted(qs)},
              "text": by_id[s]["text"][:2500]} for s, qs in items]
    json.dump(results, open(OUT / "rankings.json", "w"), indent=1)
    json.dump(sheet, open(OUT / "judge_sheet.json", "w"), ensure_ascii=False, indent=1)
    for model in MODELS:
        print(model)
        for qid, r in results[model]["queries"].items():
            mark = " (Pretorius target)" if qid in PRETORIUS_QUERIES else ""
            print(f"  {qid}: best Pretorius rank {r['pretorius_ranks'][0]}, ranks {r['pretorius_ranks']}{mark}")
    print(len(sheet), "pages to judge")


if __name__ == "__main__":
    {"sample": sample, "embed": do_embed, "rank": rank}[sys.argv[1]]()
