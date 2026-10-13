"""Embed Dutch-period Mauritius pages from GLOBALISE and rank them for animal observations.

Selection: volumes whose catalogue entries mention Mauritius (1638-1712); in them,
every page naming Mauritius/Rodrigues/Bourbon or a Mauritian landmark, plus the
preceding page and the six following pages (continuation pages rarely repeat the
place name). Model: text-embedding-3-large. Outputs in results/embed_mauritius/.

    python3 research/extinction-pilot/scripts/embed_mauritius.py select
    python3 research/extinction-pilot/scripts/embed_mauritius.py embed
    python3 research/extinction-pilot/scripts/embed_mauritius.py rank
"""
import array, json, math, os, sqlite3, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/extinction-pilot/results" / os.environ.get("EMBED_RUN", "embed_mauritius")
YEARS = tuple(int(y) for y in os.environ.get("EMBED_YEARS", "1638-1712").split("-"))
VOC = Path.home() / "Code/Historical Mysteries/globalise-drugs/data/voc.sqlite"
MODEL, DIM, MAX_CHARS, BATCH = "text-embedding-3-large", 3072, 6000, 48
PLACES = ('mauritio OR mauriti OR cerne OR mauritius OR mauritus OR mauritsius OR mauritiul OR mauritij OR "diego ruys" OR rodrigo OR '
          'mascarenhas OR mascarin* OR "isle de bourbon" OR cronenb* OR "noordwester haven" OR '
          '"noord wester haven" OR "zuydooster haven" OR "zuijdooster haven"')
KNOWN = {f"NL-HaNA_1.04.02_4005_{n:04d}" for n in range(600, 607)}  # Pretorius 1669, published by Hume & Winters

# Written for this run; descriptive, not quotations.
QUERIES = {
    "fauna_inventory": "Description of the wild animals and birds on the island, which are good to eat and how they are caught.",
    "tortoises_land": "Land tortoises on the island: how many, where they are found, what they eat, and how they are collected or eaten.",
    "tortoises_ship": "Tortoises taken on board ships or brought to the lodge as food for the sick and the crew.",
    "flightless": "A large bird that cannot fly, caught by hand or with sticks by the men.",
    "tame_birds": "Birds so tame and unafraid that they let people approach and do not flee when shot at.",
    "geese_ducks": "Wild geese, ducks and waterbirds on the island, shot or caught for the table.",
    "pigeons_parrots": "Pigeons, parrots and other forest birds, their colours, and whether they can be caught alive.",
    "red_hen": "A red bird about the size of a hen that runs on the ground and is attracted by a red cloth.",
    "hunting_journal": "Day register: the men went hunting and brought back game, birds or tortoises.",
    "scarcity": "Game and tortoises have become scarce near the lodge; hunters must go far to find any.",
    "introduced": "Goats, pigs, deer and rats on the island, their numbers and the damage they do.",
    "islets": "Birds and turtles on the small islands off the coast, their eggs and nesting.",
    "bats_reptiles": "Large bats, lizards, crocodiles or snakes seen on the island.",
    "nl_early_fauna": "veel wilt gevogelte dat men met de hant can grijpen, ende schiltpadden die goet om eeten zijn",
    "nl_modern_fauna": "Beschrijving van de dieren, vogels en schildpadden op het eiland en hoe men ze vangt en eet.",
    "report": "A report on the island's natural state: animals, birds, fish, trees, rivers and climate.",
}


def key():
    for line in open(ROOT / ".env.local"):
        if line.startswith("OPENAI_API_KEY="):
            return line.split("=", 1)[1].strip().strip("\"'")
    raise SystemExit("OPENAI_API_KEY missing from .env.local")


def embed(texts, k):
    req = urllib.request.Request(
        "https://api.openai.com/v1/embeddings",
        data=json.dumps({"model": MODEL, "input": texts}).encode(),
        headers={"Authorization": "Bearer " + k, "Content-Type": "application/json"})
    for attempt in range(8):
        try:
            r = json.load(urllib.request.urlopen(req, timeout=180))
            return [d["embedding"] for d in r["data"]], r["usage"]["total_tokens"]
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            code = getattr(e, "code", None)
            if code not in (None, 429, 500, 502, 503) or attempt == 7:
                raise
            time.sleep(min(60, 3 * 2 ** attempt))


def select():
    OUT.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(VOC)
    if YEARS[1] <= 1640:  # pre-settlement: any volume of the period, since visits are filed with voyage papers
        invs = {r[0] for r in db.execute("select inventory from catalogue group by inventory "
                                         "having min(year_start) between ? and ?", YEARS)}
    else:
        invs = {r[0] for r in db.execute(
            "select distinct inventory from catalogue where (description like '%Mauritius%' or "
            "description like '%Mauritus%' or settlement='Mauritius') and year_start between ? and ?", YEARS)}
    hits = db.execute("select inventory, sequence from pages where id in "
                      "(select rowid from pages_fts where pages_fts match ?)", (PLACES,)).fetchall()
    keep = sorted({(i, s) for i, q in hits if i in invs for s in range(q - 1, q + 7)})
    years = {}
    for inv, y0, y1 in db.execute("select inventory, min(year_start), max(year_end) from catalogue group by inventory"):
        years[inv] = (y0, y1)
    n = 0
    with open(OUT / "pages.jsonl", "w") as f:
        for inv, s in keep:
            r = db.execute("select scan_id, text from pages where inventory=? and sequence=? and token_count>=40",
                           (inv, s)).fetchone()
            if r:
                f.write(json.dumps({"scan_id": r[0], "inventory": inv, "sequence": s,
                                    "volume_years": years.get(inv), "text": r[1][:MAX_CHARS]},
                                   ensure_ascii=False) + "\n")
                n += 1
    print(len(invs), "volumes;", n, "pages")


def pages():
    return [json.loads(l) for l in open(OUT / "pages.jsonl")]


def do_embed():
    k, ps = key(), pages()
    vec_path, done_path = OUT / "vectors.f32", OUT / "embedded_count.json"
    done = json.load(open(done_path))["count"] if done_path.exists() else 0
    tokens = json.load(open(done_path))["tokens"] if done_path.exists() else 0
    batches = [ps[i:i + BATCH] for i in range(done, len(ps), BATCH)]
    with ThreadPoolExecutor(4) as pool, open(vec_path, "ab") as vf:
        for start in range(0, len(batches), 8):
            group = batches[start:start + 8]
            for vecs, t in pool.map(lambda b: embed([p["text"] or " " for p in b], k), group):
                array.array("f", [x for v in vecs for x in v]).tofile(vf)
                done += len(vecs); tokens += t
            vf.flush()
            json.dump({"count": done, "tokens": tokens}, open(done_path, "w"))
            print(f"{done}/{len(ps)} pages, {tokens:,} tokens", flush=True)
    qv, qt = embed(list(QUERIES.values()), k)
    json.dump({"queries": dict(zip(QUERIES, qv)), "tokens": qt}, open(OUT / "queries.json", "w"))
    print("done; total tokens", tokens + qt, "approx cost $%.2f" % ((tokens + qt) / 1e6 * 0.13))


def rank(per_query=25, overall=150):
    ps = pages()
    raw = array.array("f"); raw.frombytes((OUT / "vectors.f32").read_bytes())
    assert len(raw) == len(ps) * DIM
    q = json.load(open(OUT / "queries.json"))["queries"]
    qn = {k: [x / math.sqrt(sum(y * y for y in v)) for x in v] for k, v in q.items()}
    scores = {k: [] for k in qn}
    for i in range(len(ps)):
        v = raw[i * DIM:(i + 1) * DIM]
        n = math.sqrt(sum(x * x for x in v))
        for k, qq in qn.items():
            scores[k].append(sum(a * b for a, b in zip(qq, v)) / n)
    chosen = {}
    for k, sc in scores.items():
        order = sorted(range(len(ps)), key=lambda i: -sc[i])
        known_ranks = [r + 1 for r, i in enumerate(order) if ps[i]["scan_id"] in KNOWN]
        print(f"{k}: Pretorius ranks {known_ranks}")
        for r, i in enumerate(order[:per_query]):
            chosen.setdefault(i, []).append((k, r + 1))
    best = sorted(range(len(ps)), key=lambda i: -max(scores[k][i] for k in scores))
    for i in best[:overall]:
        chosen.setdefault(i, []).append(("max", best.index(i) + 1))
    out = []
    for i, why in chosen.items():
        p = ps[i]
        out.append({"scan_id": p["scan_id"], "known": p["scan_id"] in KNOWN, "volume_years": p["volume_years"],
                    "best_score": round(max(scores[k][i] for k in scores), 4), "hits": why, "text": p["text"]})
    out.sort(key=lambda x: -x["best_score"])
    json.dump(out, open(OUT / "candidates.json", "w"), ensure_ascii=False, indent=1)
    print(len(out), "candidate pages;", sum(not x["known"] for x in out), "excluding Pretorius")


if __name__ == "__main__":
    {"select": select, "embed": do_embed, "rank": rank}[sys.argv[1]]()
