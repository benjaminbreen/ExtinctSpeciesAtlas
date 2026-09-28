"""Refresh local, small thumbnails of Commons' Cyrene silphium coin category.

This is an editorial inventory, not a runtime dependency. Recheck each Commons
file page and its license before updating the gallery or republishing images.
"""

import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "silphium-gallery"
OUT.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "HistoricalLostSpeciesAtlas/0.2 (https://github.com/benjaminbreen/ExtinctSpeciesAtlas)"}


def request(url):
    with urlopen(Request(url, headers=HEADERS), timeout=45) as response:
        return response.read()


api = "https://commons.wikimedia.org/w/api.php?"
category = json.loads(request(api + urlencode({
    "action": "query", "list": "categorymembers", "cmtitle": "Category:Coins_of_Cyrene_-_Silphium",
    "cmtype": "file", "cmlimit": "50", "format": "json",
})))
titles = [item["title"] for item in category["query"]["categorymembers"]]
info = json.loads(request(api + urlencode({
    "action": "query", "prop": "imageinfo", "titles": "|".join(titles),
    "iiprop": "url|extmetadata", "iiurlwidth": "480", "format": "json",
})))
pages = {page["title"]: page for page in info["query"]["pages"].values()}
manifest = []
for n, title in enumerate(titles, 1):
    data = pages[title]["imageinfo"][0]
    path = OUT / f"coin-{n:02d}.webp"
    raw = request(data.get("thumburl", data["url"]))
    from io import BytesIO
    with Image.open(BytesIO(raw)) as image:
        image.convert("RGB").save(path, "WEBP", quality=78, method=6)
    metadata = data.get("extmetadata", {})
    manifest.append({
        "title": title,
        "file": path.relative_to(ROOT).as_posix(),
        "commons": data["descriptionurl"],
        "license": metadata.get("LicenseShortName", {}).get("value", "See file page"),
        "artist_html": metadata.get("Artist", {}).get("value", ""),
    })
    print(f"{n:02d} {title} ({path.stat().st_size // 1024} KiB)")

(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
