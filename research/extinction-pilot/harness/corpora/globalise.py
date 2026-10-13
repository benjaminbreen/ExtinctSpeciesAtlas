"""GLOBALISE v2 VOC transcriptions (NA 1.04.02), indexed locally in SQLite FTS5."""
import os, re, sqlite3, sys
from pathlib import Path

DB = Path.home() / "Code/Historical Mysteries/globalise-drugs/data/voc.sqlite"
VOCAB = Path(__file__).resolve().parents[2] / "data/derived/globalise_vocab.tsv"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import fold, fingerprint  # noqa: E402

VIEWER = "https://www.nationaalarchief.nl/onderzoeken/archief/1.04.02/invnr/{inv}/file/{scan}"


class Globalise:
    name = "globalise"

    def __init__(self, config=None):
        self.path = Path((config or {}).get("path") or os.environ.get("GLOBALISE_DB") or DB).expanduser()
        if not self.path.exists():
            raise SystemExit(f"GLOBALISE index not found at {self.path}")
        self.db = sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)
        self._years = None

    def identity(self):
        stat = self.path.stat()
        return {"adapter": self.name, "version": 2, "path": str(self.path.resolve()),
                "bytes": stat.st_size, "mtime_ns": stat.st_mtime_ns}

    def years(self):
        if self._years is None:
            self._years = {inv: (a, b) for inv, a, b in self.db.execute(
                "select inventory, min(year_start), max(year_end) from catalogue group by inventory")}
        return self._years

    def _row(self, scan_id, inv, seq, text):
        return {"scan_id": scan_id, "inventory": inv, "sequence": seq, "label": f"inv. {inv}",
                "years": self.years().get(inv), "url": VIEWER.format(inv=inv, scan=scan_id),
                "scan_url": VIEWER.format(inv=inv, scan=scan_id), "language": "nl", "text": text}

    def page(self, scan_id):
        r = self.db.execute("select scan_id, inventory, sequence, text from pages where scan_id=?", (scan_id,)).fetchone()
        return self._row(*r) if r else None

    def _volumes(self, years, vf):
        q = "select distinct inventory from catalogue where year_start<=? and coalesce(year_end,year_start)>=?"
        args = [years[1], years[0]]
        if vf.get("all_volumes"):
            return {r[0] for r in self.db.execute(q, args)}
        conds = []
        for s in vf.get("settlements", []):
            conds.append("settlement = ?"); args.append(s)
        for d in vf.get("description_like", []):
            conds.append("description like ?"); args.append(f"%{d}%")
        for lo, hi in vf.get("inventory_ranges", []):
            conds.append("cast(inventory as integer) between ? and ?"); args.extend((lo, hi))
        for inventory in vf.get("inventories", []):
            conds.append("inventory = ?"); args.append(str(inventory))
        if not conds:
            raise SystemExit("scope.volumes needs a catalogue selector, inventories, or all_volumes")
        return {r[0] for r in self.db.execute(q + " and (" + " or ".join(conds) + ")", args)}

    def scope(self, cfg):
        years = tuple(cfg["years"])
        invs = self._volumes(years, cfg["volumes"])
        lo, hi = cfg.get("window", [0, 0])
        mintok = cfg.get("min_tokens", 40)
        if cfg.get("anchor_fts"):
            hits = self.db.execute("select inventory, sequence from pages where id in "
                                   "(select rowid from pages_fts where pages_fts match ?)", (cfg["anchor_fts"],)).fetchall()
            keep = sorted({(i, s) for i, q in hits if i in invs for s in range(q + lo, q + hi + 1)})
            rows = []
            for inv, s in keep:
                r = self.db.execute("select scan_id, inventory, sequence, text from pages where inventory=? and "
                                    "sequence=? and token_count>=?", (inv, s, mintok)).fetchone()
                if r:
                    rows.append(self._row(*r))
        else:
            rows = [self._row(*r) for inv in sorted(invs)
                    for r in self.db.execute("select scan_id, inventory, sequence, text from pages where inventory=? "
                                             "and token_count>=? order by sequence", (inv, mintok))]
        print(f"scope: {len(invs)} volumes")
        return rows

    def vocabulary(self):
        cache = VOCAB.with_name("globalise_vocab-" + fingerprint(self.identity())[:16] + ".tsv")
        if not cache.exists():
            print("building GLOBALISE vocabulary cache (about a minute)...")
            self.db.execute("create virtual table if not exists temp.v using fts5vocab(main, 'pages_fts', 'row')")
            cache.parent.mkdir(parents=True, exist_ok=True)
            tmp = cache.with_suffix(".tmp")
            with open(tmp, "w") as f:
                for t, n in self.db.execute("select term, doc from temp.v"):
                    f.write(f"{t}\t{n}\n")
            os.replace(tmp, cache)
        out = []
        with open(cache) as f:
            for line in f:
                t, n = line.rstrip("\n").split("\t")
                out.append((t, int(n)))
        return out

    def fts(self, query, years=None):
        rows = [self._row(*r) for r in self.db.execute(
            "select scan_id, inventory, sequence, text from pages where id in "
            "(select rowid from pages_fts where pages_fts match ?)", (query,))]
        if years:
            rows = [r for r in rows if r["years"] and r["years"][0] is not None
                    and r["years"][0] <= years[1] and (r["years"][1] or r["years"][0]) >= years[0]]
        return rows

    def pages_with_terms(self, terms, years=None):
        hits = {}
        for i in range(0, len(terms), 200):
            chunk = terms[i:i + 200]
            for r in self.fts(" OR ".join(f'"{t}"' for t in chunk), years):
                words = set(re.findall(r"\w+", fold(r["text"])))
                r["terms"] = [t for t in chunk if t in words] or ["(diacritic-folded index match)"]
                if r["scan_id"] in hits:
                    hits[r["scan_id"]]["terms"] += r["terms"]
                else:
                    hits[r["scan_id"]] = r
        return hits
