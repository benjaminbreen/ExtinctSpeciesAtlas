"""Search VOC gift, cargo and rarity pages (to 1700) for live Mauritian birds in transit.

Selection: GLOBALISE pages whose text has both a gift/cargo/rarity cue and an
animal cue (full-text pre-filter), in volumes dated up to 1700. Pages are embedded
with text-embedding-3-large and ranked against queries describing a strange bird,
dodo, or Mauritius animal sent as a present or rarity. Outputs in results/embed_gifts/.

    python3 research/extinction-pilot/scripts/embed_gifts.py select|embed|rank
"""
import array, json, math, sqlite3, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from embed_mauritius import key, embed, VOC, ROOT, DIM, MAX_CHARS, BATCH  # noqa: E402

OUT = ROOT / "research/extinction-pilot/results/embed_gifts"
GIFT = ('(schenckagie* OR schenkagie* OR schenckaedje* OR vereeringh* OR vereering* OR present* OR geschenck* '
        'OR rariteijt* OR rariteyt* OR rariteit* OR ongetaxeert OR "voor den coninck" OR "aen den coninck" '
        'OR "voor de coninck")')
ANIMAL = ('(vogel* OR gevogelte OR gedier* OR "levende" OR levendich OR levendigh OR dieren OR beest* OR casuaris* '
          'OR casuw* OR swaen OR swanen OR struys* OR struijs* OR hert OR harten OR hinde OR hinden OR porco '
          'OR dodaer* OR dodeer* OR doders* OR dronte* OR walg* OR papegaij* OR papegaey* OR aep OR apen)')
QUERIES = {
    "dodo_gift": "A strange large bird from the island of Mauritius sent alive as a present to the king.",
    "rarity_bird": "A rare foreign bird sent as a rarity or curiosity to a ruler, governor or lord.",
    "cargo_live": "Cargo list including a live bird and other animals, unvalued, shipped with the goods.",
    "dodo_desc": "A fat, clumsy bird that cannot fly, with a large hooked beak and tiny wings, kept alive on board.",
    "mauritius_animals": "Live animals and birds brought from Mauritius on the ship.",
    "menagerie": "Exotic animals for the king's menagerie: birds, deer and other curious creatures presented by the Dutch.",
    "bird_died": "The strange bird died on the voyage or shortly after arriving.",
    "nl_dodo": "een vreemde vogel van 't eijlant Mauritius, levendich aen den coninck vereert",
    "nl_rarity": "levende vogels ende gedierte voor rariteijt ofte schenckagie gesonden",
}


def select():
    OUT.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(VOC)
    years = dict(db.execute("select inventory, min(year_start) from catalogue group by inventory"))
    rows = db.execute("select scan_id, inventory, sequence, text, token_count from pages where id in "
                      "(select rowid from pages_fts where pages_fts match ?)", (f"{GIFT} AND {ANIMAL}",)).fetchall()
    n = 0
    with open(OUT / "pages.jsonl", "w") as f:
        for sid, inv, seq, text, tok in rows:
            if tok >= 40 and (years.get(inv) or 9999) <= 1700:
                f.write(json.dumps({"scan_id": sid, "inventory": inv, "sequence": seq,
                                    "volume_years": years.get(inv), "text": text[:MAX_CHARS]},
                                   ensure_ascii=False) + "\n")
                n += 1
    print(n, "pages")


def pages():
    return [json.loads(l) for l in open(OUT / "pages.jsonl")]


def do_embed():
    k, ps = key(), pages()
    batches = [ps[i:i + BATCH] for i in range(0, len(ps), BATCH)]
    tokens = 0
    with ThreadPoolExecutor(4) as pool, open(OUT / "vectors.f32", "wb") as vf:
        for vecs, t in pool.map(lambda b: embed([p["text"] or " " for p in b], k), batches):
            array.array("f", [x for v in vecs for x in v]).tofile(vf)
            tokens += t
    qv, qt = embed(list(QUERIES.values()), k)
    json.dump({"queries": dict(zip(QUERIES, qv)), "tokens": tokens + qt}, open(OUT / "queries.json", "w"))
    print("tokens", tokens + qt, "approx $%.2f" % ((tokens + qt) / 1e6 * 0.13))


def rank(per_query=30, overall=100):
    ps = pages()
    raw = array.array("f"); raw.frombytes((OUT / "vectors.f32").read_bytes())
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
        for r, i in enumerate(sorted(range(len(ps)), key=lambda i: -sc[i])[:per_query]):
            chosen.setdefault(i, []).append((k, r + 1))
    for r, i in enumerate(sorted(range(len(ps)), key=lambda i: -max(scores[k][i] for k in scores))[:overall]):
        chosen.setdefault(i, []).append(("max", r + 1))
    out = [{"scan_id": ps[i]["scan_id"], "volume_years": ps[i]["volume_years"], "hits": why,
            "best_score": round(max(scores[k][i] for k in scores), 4), "text": ps[i]["text"]}
           for i, why in chosen.items()]
    out.sort(key=lambda x: -x["best_score"])
    json.dump(out, open(OUT / "candidates.json", "w"), ensure_ascii=False, indent=1)
    print(len(out), "candidates")


if __name__ == "__main__":
    {"select": select, "embed": do_embed, "rank": rank}[sys.argv[1]]()
