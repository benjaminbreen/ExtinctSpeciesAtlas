"""Refresh credited Wikimedia thumbnails for the primary-authority index.

This is an editorial maintenance script. It is not part of the website runtime.
Review the file pages, license metadata, and crops after each refresh.
"""

import json
from io import BytesIO
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets" / "authorities"
DEST.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "HistoricalLostSpeciesAtlas/0.3 (https://github.com/benjaminbreen/ExtinctSpeciesAtlas)"}
items = json.loads((ROOT / "data" / "authorities.json").read_text())


def fetch(url):
    with urlopen(Request(url, headers=HEADERS), timeout=45) as response:
        return response.read()


api = "https://commons.wikimedia.org/w/api.php?" + urlencode({
    "action": "query",
    "prop": "imageinfo",
    "titles": "|".join("File:" + item["image_file"] for item in items),
    "iiprop": "url|extmetadata",
    "iiurlwidth": "420",
    "format": "json",
})
results = json.loads(fetch(api))["query"]["pages"].values()
pages = {page["title"]: page for page in results}
manifest = []
for item in items:
    title = "File:" + item["image_file"]
    info = pages[title]["imageinfo"][0]
    path = DEST / (item["slug"] + ".webp")
    image = Image.open(BytesIO(fetch(info.get("thumburl", info["url"]))))
    ImageOps.exif_transpose(image).convert("RGB").save(path, "WEBP", quality=82, method=6)
    manifest.append({
        "authority": item["slug"],
        "source": info["descriptionurl"],
        "license": info.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "Check file page"),
        "file": path.relative_to(ROOT).as_posix(),
        "display_credit": item["image_credit"],
        "depiction": item["image_description"],
    })
    print(item["slug"], path.stat().st_size // 1024, "KiB")

(DEST / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
