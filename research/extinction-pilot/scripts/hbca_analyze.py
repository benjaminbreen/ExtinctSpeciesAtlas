"""Summarise machine-read Fort Chipewyan journal entries (results/hbca/B39/pages.jsonl).

Writes results/hbca/B39/entries.jsonl (one row per extracted entry, with an inferred year)
and results/hbca/B39/by_year.csv, and prints a yearly table. Years come from the page's own
date header as read by the model, falling back to the previous page of the same volume.
Counts are machine readings: every figure used in prose must be checked against the scan.

    python3 research/extinction-pilot/scripts/hbca_analyze.py
"""
import csv, json, re
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "results/hbca/B39"
BISON = re.compile(r"buffal|bison|\bbeuf|boeuf|\bcattle\b", re.I)
SCARCE = re.compile(r"scarc|starv|famine|no animals|killed nothing|nothing to eat|want of provisions|reduced", re.I)


# Volume date ranges from the Keystone listings (HBCA B.39/a), in listing order.
VOLUMES = {"B39-A-1": (1802, 1803), "B39-A-2": (1801, 1803), "B39-A-3": (1803, 1804), "B39-A-4": (1804, 1805),
    "B39-A-5a": (1805, 1806), "B39-A-5b": (1803, 1805), "B39-A-6": (1815, 1816), "B39-A-7": (1816, 1817),
    "B39-A-8": (1816, 1817), "B39-A-9": (1816, 1817), "B39-A-10": (1817, 1817), "B39-A-11": (1817, 1817),
    "B39-A-12": (1817, 1817), "B39-A-13": (1817, 1818), "B39-A-14": (1818, 1819), "B39-A-15": (1819, 1820),
    "B39-A-16": (1820, 1821), "B39-A-17": (1821, 1821), "B39-A-18": (1820, 1821), "B39-A-19": (1820, 1820),
    "B39-A-20": (1821, 1822), "B39-A-21A": (1822, 1822), "B39-A-21B": (1822, 1823), "B39-A-22": (1823, 1824),
    "B39-A-23": (1824, 1825), "B39-A-24": (1825, 1826), "B39-A-25": (1826, 1827), "B39-A-26": (1827, 1828),
    "B39-A-27": (1828, 1829), "B39-A-28": (1831, 1832), "B39-A-29": (1831, 1834), "B39-A-30": (1834, 1835),
    "B39-A-31": (1834, 1836), "B39-A-32": (1835, 1836), "B39-A-33": (1836, 1837), "B39-A-34": (1837, 1838),
    "B39-A-35": (1838, 1839), "B39-A-36": (1836, 1839), "B39-A-38": (1839, 1840), "B39-A-40": (1839, 1842),
    "B39-A-41": (1842, 1845), "B39-A-42": (1846, 1852), "B39-A-43": (1852, 1854), "B39-A-44A": (1855, 1858),
    "B39-A-44B": (1858, 1861), "B39-A-45": (1865, 1867), "B39-A-46": (1867, 1869), "B39-A-47": (1869, 1871)}


# B.39/a/2 opens with Peter Fidler's Chesterfield House (South Saskatchewan) journal, 1800-02:
# Blackfeet, buffalo pounds. Scans before 33 (August 1802 departure for Athabasca) are plains bison.
EXCLUDE = {("B39-A-2.pdf", i) for i in range(0, 33)}


def norm(q):
    return re.sub(r"[^a-z0-9]", "", (q or "").lower())[:60]


def clamp(pdf, ys):
    lo, hi = VOLUMES.get(pdf.replace(".pdf", ""), (1700, 1900))
    ok = [y for y in ys if lo <= y <= hi]
    return ok


def year_of(s):
    ys = [int(y) for y in re.findall(r"\b(18[0-7]\d|179\d)\b", s or "")]
    return ys


def main():
    rows = [json.loads(l) for l in open(OUT / "pages.jsonl")]
    rows.sort(key=lambda r: ([int(t) if t.isdigit() else t for t in re.split(r"(\d+)", r["pdf"])], r["image"]))
    entries, last_year, seen = [], {}, set()
    rows = [r for r in rows if (r["pdf"], r["image"]) not in EXCLUDE]
    for r in rows:
        res = r["result"]
        if isinstance(res, list):
            res = res[0] if res else {}
        if not isinstance(res, dict) or "error" in res:
            continue
        ys = clamp(r["pdf"], year_of(res.get("dates", "")))
        if not ys:
            ys = [last_year.get(r["pdf"], VOLUMES.get(r["pdf"].replace(".pdf", ""), (None,))[0])]
        last_year[r["pdf"]] = ys[-1]
        r["_year"] = ys[-1]
        for e in res.get("e", []) or []:
            q = e.get("q") or ""
            ey = clamp(r["pdf"], year_of(e.get("d", ""))) or ys
            k = (ey[-1] if ey else None, norm(q))
            if len(k[1]) >= 25 and k in seen:
                continue  # same entry in an overlapping copy volume
            seen.add(k)
            entries.append({"pdf": r["pdf"], "image": r["image"], "year": ey[-1] if ey else None,
                            "date": e.get("d"), "quote": q,
                            "bison_model": e.get("bison"), "bison_named": bool(BISON.search(q)),
                            "meat_lb": e.get("meat_lb"), "place": e.get("place"),
                            "scarce": bool(e.get("scarce")) or bool(SCARCE.search(q))})
    with open(OUT / "entries.jsonl", "w") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    agg = defaultdict(lambda: {"pages": 0, "bison_entries": 0, "bison_count": 0, "meat_lb": 0, "scarce": 0, "entries": 0})
    for r in rows:
        if r.get("_year"):
            agg[r["_year"]]["pages"] += 1
    for e in entries:
        a = agg[e["year"]]
        a["entries"] += 1
        if e["bison_named"]:
            a["bison_entries"] += 1
            if isinstance(e["bison_model"], int) and 0 < e["bison_model"] < 200:
                a["bison_count"] += e["bison_model"]
        if isinstance(e["meat_lb"], int) and 0 < e["meat_lb"] < 20000:
            a["meat_lb"] += e["meat_lb"]
        a["scarce"] += e["scarce"]
    with open(OUT / "by_year.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["year", "pages", "entries", "bison_entries", "bison_count_model", "meat_lb_model", "scarcity_entries"])
        for y in sorted(k for k in agg if k):
            a = agg[y]
            w.writerow([y, a["pages"], a["entries"], a["bison_entries"], a["bison_count"], a["meat_lb"], a["scarce"]])
    print(f"{len(rows)} pages, {len(entries)} entries; {sum(e['bison_named'] for e in entries)} name bison")
    print(open(OUT / "by_year.csv").read())


if __name__ == "__main__":
    main()
