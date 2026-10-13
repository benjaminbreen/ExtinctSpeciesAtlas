"""One-pass lexical sweep of the BHL bulk OCR export for extinct-species names.

Streams ~/Code/Historical Mysteries/corpora/bhl-ocr/bhl-ocr-*.tar.bz2 through `bzip2 -dc` (no extraction),
matches the patterns in data/curated/bhl_sweep_vocab.json against folded page text, and writes one row per
matching page to results/bhl_sweep/hits.jsonl with the BHL page URL and a context snippet per match.
Then `annotate` joins hits to BHL item/title metadata (year, language, title) and writes summary files.

    python3 research/extinction-pilot/scripts/bhl_stream_sweep.py sweep      # 1-3 hours; resumable by item
    python3 research/extinction-pilot/scripts/bhl_stream_sweep.py annotate

A hit is a machine-OCR lexical match, not an identification. Absence of a hit is not evidence of absence.
"""
import csv, gzip, json, re, subprocess, sys, tarfile, time, unicodedata
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

PILOT = Path(__file__).resolve().parents[1]
TAR = sorted((Path.home() / "Code/Historical Mysteries/corpora/bhl-ocr").glob("bhl-ocr-*.tar.bz2"))[-1]
OUT = PILOT / "results/bhl_sweep"
VOCAB = json.loads((PILOT / "data/curated/bhl_sweep_vocab.json").read_text())["taxa"]
NAME = re.compile(r"item-(\d+)-(\d+)-(\d+)\.txt$")
PATS = [(taxon, p) for taxon, ps in VOCAB.items() for p in ps]
RX = re.compile(r"\b(?:" + "|".join(f"(?P<g{i}>{p})" for i, (_, p) in enumerate(PATS)) + r")\b")
csv.field_size_limit(10 ** 8)
# Byte-level prefilter: every pattern above must contain one of these lower-case fragments.
ANCHORS = [a.encode() for a in ['dodo', 'dront', 'walvogel', 'walgvogel', 'walghvogel', 'walchvogel', 'wal-vogel', 'walg-vogel', 'walgh-vogel', 'walch-vogel', 'walhvogel', 'dodar', 'doder', 'dodaer', 'dodeer', 'dodaar', 'dodear', 'didus', 'raphus', 'cucullat', 'nazare', 'aphanapteryx', 'poule rouge', 'pezoph', 'solitarius', 'solitaire de rodrigue', 'solitaire de bourbon', 'solitaire de la reunion', 'threskior', 'cylindrasp', 'testudo vosm', 'testudo pelt', 'testudo inep', 'testudo trise', 'testudo indica', 'lophops', 'necrops', 'mascarin', 'fregil', 'huppe de bourbon', 'erythrom', 'alectroenas', 'nitidiss', 'pigeon hollandais', 'great auk', 'garefowl', 'gairfowl', 'gare-fowl', 'gair-fowl', 'geirfugl', 'geir-fugl', 'impennis', 'grand pingouin', 'pingouin brachipt', 'riesenalk', 'ytina', 'hydrodam', 'manatus gigas', 'sea cow', 'sea-cow', 'seacow', 'korov', 'phalacrocorax perspic', 'pallas cormorant', "pallas's cormorant", "pallas' cormorant", 'pallass cormorant', 'spectacled cormorant', 'camptor', 'camptol', 'labrador duck', 'anas labrador', 'fuligula labrador', 'pied duck', 'shoal duck', 'sea mink', 'macrodon', 'blaauw', 'blauw', 'blau-b', 'blaub', 'blauer b', 'blue antelope', 'antilope bleue', 'leucophae', 'tzeiran', 'theiram', 'quagga', 'quacha', 'kwagga', 'urochs', 'auerochs', 'auer-ochs', 'primigen', 'bos urus', 'ara tricolor', 'psittacus tricolor', 'cuban macaw', 'lorirojo', 'guacamayo de cuba', 'warrah', 'antarcticus', 'loup antarctique', 'canis australis', 'dusicyon', 'falkland wolf', 'falkland fox', 'falkland dog', 'falkland island wolf', 'falkland island fox', 'falkland island dog', 'antarctic wolf', 'silphion', 'laser cyrenaic', 'silphium cyrenaic', 'dromaius', 'island emu', 'nestor productus', 'prosobon', 'aechmor', 'chaunop', 'drepanis pacifica', 'coturnix nov', 'pennula']]


def fold(s):
    s = s.replace("ſ", "s").replace("æ", "ae").replace("œ", "oe")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"-\s*\n\s*", "", s)


def scan(batch):
    rows = []
    for name, raw in batch:
        low = raw.lower()
        if not any(a in low for a in ANCHORS):
            continue
        text = fold(raw.decode("utf-8", "replace"))
        found = []
        for m in RX.finditer(text):
            i = int(m.lastgroup[1:])
            found.append({"taxon": PATS[i][0], "pattern": PATS[i][1], "match": m.group(0),
                          "context": " ".join(text[max(0, m.start() - 300):m.end() + 300].split())})
        named = NAME.search(name)
        if found and not named:
            print("unrecognized member name with matches:", name, flush=True)
        if found and named:
            item, page, seq = named.groups()
            rows.append({"item": int(item), "page_id": int(page), "seq": int(seq),
                         "url": f"https://www.biodiversitylibrary.org/page/{int(page)}",
                         "taxa": sorted({f["taxon"] for f in found}), "matches": found[:12], "n_matches": len(found)})
    return rows


def batches(state):
    proc = subprocess.Popen(["bzip2", "-dc", str(TAR)], stdout=subprocess.PIPE, bufsize=1 << 22)
    tf = tarfile.open(fileobj=proc.stdout, mode="r|")
    batch, n = [], 0
    for m in tf:
        if not m.isfile() or not m.name.endswith(".txt"):
            continue
        n += 1
        state["pages"] = n
        if n <= state["skip"]:
            continue
        if m.size:
            batch.append((m.name, tf.extractfile(m).read()))
        if len(batch) >= 2000:
            yield batch, n
            batch = []
    if batch:
        yield batch, n


def sweep():
    OUT.mkdir(parents=True, exist_ok=True)
    ckpt = OUT / "checkpoint.json"
    state = json.loads(ckpt.read_text()) if ckpt.exists() else {"done_pages": 0, "hits": 0}
    state["skip"] = state["done_pages"]
    t0 = time.time()
    with Pool(max(2, __import__("os").cpu_count() - 2)) as pool, open(OUT / "hits.jsonl", "a") as out:
        pending = []
        for batch, n in batches(state):
            pending.append((pool.apply_async(scan, (batch,)), n))
            while len(pending) > 24 or (pending and pending[0][0].ready()):
                res, upto = pending.pop(0)
                for r in res.get():
                    out.write(json.dumps(r, ensure_ascii=False) + "\n"); state["hits"] += 1
                out.flush()
                state["done_pages"] = upto
                ckpt.write_text(json.dumps({"done_pages": upto, "hits": state["hits"], "tar": TAR.name}))
                if upto % 200000 < 2000:
                    print(f"{upto:,} pages, {state['hits']:,} hit pages, {time.time()-t0:,.0f}s", flush=True)
        for res, upto in pending:
            for r in res.get():
                out.write(json.dumps(r, ensure_ascii=False) + "\n"); state["hits"] += 1
            state["done_pages"] = upto
        ckpt.write_text(json.dumps({"done_pages": state["done_pages"], "hits": state["hits"], "tar": TAR.name, "complete": True}))
    print("complete", state)


def read_tsv(path):
    with gzip.open(path, "rt", encoding="utf-8-sig") as f:
        yield from csv.DictReader(f, delimiter="\t")


def annotate():
    hits = [json.loads(l) for l in open(OUT / "hits.jsonl")]
    items = {int(r["ItemID"]): r for r in read_tsv(PILOT / "data/raw/bhl/item.txt.gz")}
    titles = {r["TitleID"]: r for r in read_tsv(PILOT / "data/raw/bhl/title.txt.gz")}
    for h in hits:
        it = items.get(h["item"], {}); ti = titles.get(it.get("TitleID"), {})
        y = re.search(r"\d{4}", it.get("Year") or "") or re.search(r"\d{4}", ti.get("StartYear") or "")
        h.update(year=int(y.group(0)) if y else None, language=ti.get("LanguageCode"),
                 title=ti.get("ShortTitle") or ti.get("FullTitle"), author=ti.get("TL2Author"),
                 item_url=f"https://www.biodiversitylibrary.org/item/{h['item']}")
    rules = json.loads((PILOT / "data/curated/bhl_sweep_vocab.json").read_text()).get("noise_rules", [])
    for h in hits:  # mark (do not delete) matches that a documented noise rule explains
        for m in h["matches"]:
            for r in rules:
                if m["taxon"] in r["taxa"] and ("year_lt" not in r or (h["year"] or 9999) < r["year_lt"]) \
                        and ("matches" not in r or m["match"] in r["matches"]) \
                        and ("languages" not in r or h["language"] in r["languages"]):
                    m["noise"] = r["rule"]
        h["signal_taxa"] = sorted({m["taxon"] for m in h["matches"] if "noise" not in m})
    with open(OUT / "hits_annotated.jsonl", "w") as f:
        for h in hits:
            f.write(json.dumps(h, ensure_ascii=False) + "\n")
    summ = defaultdict(lambda: Counter())
    for h in hits:
        dec = f"{(h['year'] // 50) * 50}s" if h["year"] else "unknown"
        for t in h["signal_taxa"]:
            summ[t][dec] += 1; summ[t]["lang:" + (h["language"] or "?")] += 1; summ[t]["total"] += 1
    (OUT / "summary.json").write_text(json.dumps(summ, indent=1, sort_keys=True))
    early = [h for h in hits if h["year"] and h["year"] <= 1860 and h["signal_taxa"]]
    with open(OUT / "early_hits.jsonl", "w") as f:
        for h in sorted(early, key=lambda h: (h["year"], h["item"], h["seq"])):
            f.write(json.dumps(h, ensure_ascii=False) + "\n")
    print(len(hits), "hit pages;", len(early), "in items dated <= 1860")
    for t, c in sorted(summ.items(), key=lambda x: -x[1]["total"]):
        print(f"{t:24s} {c['total']:7,d}  pre-1800: {sum(v for k, v in c.items() if k[:2] in ('15','16','17')):,}")


if __name__ == "__main__":
    {"sweep": sweep, "annotate": annotate}[sys.argv[1]]()
