"""Offline adapter for GLOBALISE's TANAP Council of Policy Markdown editions.

Units are printed page ranges/resolution sections, not manuscript scan leaves.
Editorial footnotes are retained separately and excluded from retrieval text.
"""
import hashlib
import html
import json
import os
import re
import sqlite3
from datetime import date as calendar_date
from pathlib import Path
from urllib.parse import quote

from engine import HERE, atomic_json, fingerprint, fold

BASE = "https://docs.globalise.huygens.knaw.nl/tanap/cape-transcriptions/Council-of-Policy/"
DEFAULT = HERE.parent / "data/raw/tanap/Council-of-Policy"
HEADING = re.compile(r"^## ([^\n]+)$", re.M)


def plain(markdown):
    text = re.sub(r"<[^>]+>", " ", markdown)
    text = re.sub(r"\[\^[^]]+\]", "", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\[[^]]*\]", r"\1", text)
    return html.unescape(text).strip()


def parse_volume(path, root):
    source = path.read_text()
    # Definitions can have indented continuation lines. Keep them outside primary text.
    notes = []
    body = []
    in_note = False
    for line in source.splitlines(keepends=True):
        if re.match(r"^\[\^[^]]+\]:", line):
            in_note = True
        elif in_note and line.strip() and not line.startswith((" ", "\t")):
            in_note = False
        (notes if in_note else body).append(line)
    body = "".join(body)
    headings = list(HEADING.finditer(body))
    for i, h in enumerate(headings):
        chunk = body[h.end():headings[i + 1].start() if i + 1 < len(headings) else len(body)]
        label = h[1]
        locator = re.match(r"(C\.|V\.C\.|Koloniaal Archief No\.)\s*(\d+)[.,]*\s*pp?[.,]?\s*(\d+)(?:\s*[-–]\s*(\d+))?", label)
        hague = re.match(r"Haagse Kopie, Fol\.\s*(\d+)(?:\s*[-–]\s*(\d+))?", label)
        if locator:
            series = {"C.": "C", "V.C.": "VC", "Koloniaal Archief No.": "NA"}[locator[1]]
            volume, first, last = int(locator[2]), int(locator[3]), int(locator[4] or locator[3])
            inventory, unit = f"{series}{volume:03d}", "p"
        elif hague:
            inventory = "Hague-" + re.match(r"C\d+", path.name)[0]
            first, last, unit = int(hague[1]), int(hague[2] or hague[1]), "f"
        else:
            raise ValueError(f"unrecognized edition heading in {path.name}: {label}")
        text = plain(chunk)
        # Curly-brace dates were supplied by TANAP editors, not inferred from prose.
        date = re.search(r"\{((?:16|17)\d{2})(\d{2})(\d{2})\}", text[:400])
        year = int(date[1]) if date else None
        document_date, precision = None, None
        if date:
            month, day = int(date[2]), int(date[3])
            if month == 0 and day == 0:
                document_date, precision = date[1], "year"
            elif 1 <= month <= 12 and day == 0:
                document_date, precision = f"{date[1]}-{date[2]}", "month"
            else:
                try:
                    document_date = calendar_date(year, month, day).isoformat()
                    precision = "day"
                except ValueError:
                    precision = "invalid_tag"
        relative = path.relative_to(root).as_posix()
        url = BASE + quote(str(Path(relative).with_suffix("")), safe="/") + "/"
        referenced = set(re.findall(r"\[\^([^]]+)\]", chunk))
        note_text = "".join(notes)
        note_parts = re.split(r"(?=^\[\^[^]]+\]:)", note_text, flags=re.M)
        relevant_notes = "".join(n for n in note_parts if re.match(r"\[\^([^]]+)\]:", n)
                                 and re.match(r"\[\^([^]]+)\]:", n)[1] in referenced)
        date_suffix = "_d" + "".join(date.groups()) if date else ""
        yield {"scan_id": f"TANAP_{inventory}_{unit}{first:04d}-{last:04d}" + date_suffix,
               "source_id": f"tanap-council-{inventory}", "inventory": inventory,
               "sequence": first, "label": h.group()[3:].rstrip("."), "years": [year, year],
               "document_date": document_date, "date_basis": "TANAP date tag" if date else None,
               "document_date_precision": precision, "date_tag": date[0] if date else None,
               "url": url, "transcription_url": url, "scan_url": None, "language": "nl",
               "unit_type": "edition_section", "text": text, "editorial_notes": relevant_notes,
               "source_file": relative, "license": "https://creativecommons.org/publicdomain/zero/1.0/"}


class Tanap:
    name = "tanap"

    def __init__(self, config=None):
        cfg = config or {}
        self.root = Path(cfg.get("path") or os.environ.get("TANAP_ROOT") or DEFAULT).expanduser()
        files = sorted(self.root.glob("**/*.md"))
        # Reference works are not Council minutes.
        files = [p for p in files if re.match(r"C\d", p.name)]
        if not files:
            raise ValueError(f"no TANAP Council Markdown at {self.root}; see harness README")
        receipt = [{"path": p.relative_to(self.root).as_posix(),
                    "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
        self.signature = fingerprint({"version": 5, "files": receipt})
        cache = HERE.parent / "data/derived/tanap"
        cache.mkdir(parents=True, exist_ok=True)
        self.path = cache / (self.signature + ".sqlite")
        if not self.path.exists():
            tmp = self.path.with_suffix(".tmp")
            db = sqlite3.connect(tmp)
            try:
                db.executescript("create table pages(id integer primary key, scan_id text unique, inventory text, sequence integer, year integer, data text);"
                                 "create virtual table pages_fts using fts5(text);"
                                 "create virtual table vocab using fts5vocab(pages_fts, 'row');")
                seen, duplicates = {}, 0
                for path in files:
                    for row in parse_volume(path, self.root):
                        s = row["scan_id"]
                        if s in seen:
                            if seen[s] == row["text"]:
                                duplicates += 1
                                continue
                            # Retain distinct resolutions/variants sharing an edition locator.
                            row["shared_locator"] = s
                            s += "_v" + hashlib.sha256(row["text"].encode()).hexdigest()[:12]
                            row["scan_id"] = s
                            if s in seen:
                                duplicates += 1
                                continue
                        seen[s] = row["text"]
                        cur = db.execute("insert into pages(scan_id,inventory,sequence,year,data) values(?,?,?,?,?)",
                                         (s, row["inventory"], row["sequence"], row["years"][0], json.dumps(row, ensure_ascii=False)))
                        db.execute("insert into pages_fts(rowid,text) values(?,?)", (cur.lastrowid, fold(row["text"])))
                db.commit()
            except Exception:
                db.close(); tmp.unlink(missing_ok=True); raise
            db.close(); os.replace(tmp, self.path)
            atomic_json(cache / (self.signature + ".json"), {"repository": "https://github.com/globalise-huygens/tanap.docs.globalise.huygens.knaw.nl",
                        "input": self.signature, "files": receipt, "units": len(seen), "duplicate_units": duplicates})
        self.db = sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)

    def identity(self):
        return {"adapter": self.name, "input": self.signature}

    def page(self, scan_id):
        r = self.db.execute("select data from pages where scan_id=?", (scan_id,)).fetchone()
        return json.loads(r[0]) if r else None

    def vocabulary(self):
        return self.db.execute("select term,doc from vocab").fetchall()

    def fts(self, query, years=None):
        sql = "select data from pages where id in (select rowid from pages_fts where pages_fts match ?)"
        args = [query]
        if years:
            sql += " and (year between ? and ? or year is null)"; args.extend(years)
        return [json.loads(r[0]) for r in self.db.execute(sql + " order by inventory,sequence", args)]

    def scope(self, cfg):
        years = cfg["years"]
        if cfg.get("anchor_fts"):
            anchors = self.fts(cfg["anchor_fts"], years)
            lo, hi = cfg.get("window", [0, 0])
            # Adjacent transcription sections, not consecutive printed page numbers.
            all_rows = [json.loads(r[0]) for r in self.db.execute("select data from pages order by inventory,sequence")]
            keep = set()
            indices = {p["scan_id"]: i for i, p in enumerate(all_rows)}
            for p in anchors:
                i = indices[p["scan_id"]]
                keep.update(j for j in range(max(0, i + lo), min(len(all_rows), i + hi + 1))
                            if all_rows[j]["inventory"] == p["inventory"])
            rows = [all_rows[i] for i in sorted(keep)]
        else:
            rows = [json.loads(r[0]) for r in self.db.execute(
                "select data from pages where year between ? and ? or year is null order by inventory,sequence", years)]
        return [p for p in rows if (p["years"][0] is None or years[0] <= p["years"][0] <= years[1])
                and len(p["text"].split()) >= cfg.get("min_tokens", 0)]

    def pages_with_terms(self, terms, years=None):
        hits = {}
        for i in range(0, len(terms), 200):
            chunk = terms[i:i + 200]
            for p in self.fts(" OR ".join('"' + t.replace('"', '""') + '"' for t in chunk), years):
                words = set(re.findall(r"\w+", fold(p["text"])))
                matched = [t for t in chunk if t in words]
                if p["scan_id"] in hits:
                    hits[p["scan_id"]]["terms"].extend(matched)
                else:
                    hits[p["scan_id"]] = dict(p, terms=matched)
        return hits
