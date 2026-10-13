"""Scan Delpher newspaper article texts (1618-1799 ZIPs) for dodo names and Mauritius fauna terms.

Reads *_articletext.xml members directly from the ZIPs (no extraction) and writes
matching articles to results/delpher_dodo_hits.jsonl.
"""
import json, re, sys, zipfile
from pathlib import Path

ZIPS = Path.home() / "Code/Historical Mysteries/corpora/delpher-kranten/zips"
OUT = Path(__file__).resolve().parents[1] / "results/delpher_dodo_hits.jsonl"
PAT = re.compile(r"\b(do+d[ae]+e?r[st]\w*|dod[ae]+rs\w*|dodo\w*|dronte\w*|walg+h?vog\w*|walchvog\w*|kermisgans\w*"
                 r"|mauriti\w*|mauritz\s+eyland\w*|eyland\s+mauritius)\b", re.I)
TAG = re.compile(r"<[^>]+>")

OUT.parent.mkdir(parents=True, exist_ok=True)
n = 0
with open(OUT, "w") as out:
    for zp in sorted(ZIPS.glob("kranten_pd_*.zip")):
        with zipfile.ZipFile(zp) as z:
            for name in z.namelist():
                if not name.endswith("_articletext.xml"):
                    continue
                text = TAG.sub(" ", z.read(name).decode("utf-8", "replace"))
                hits = sorted({m.group(0).lower() for m in PAT.finditer(text)})
                if hits:
                    out.write(json.dumps({"zip": zp.name, "member": name, "hits": hits,
                                          "text": " ".join(text.split())[:4000]}, ensure_ascii=False) + "\n")
                    n += 1
        print(zp.name, "cumulative hits", n, flush=True)
print("done", n)
