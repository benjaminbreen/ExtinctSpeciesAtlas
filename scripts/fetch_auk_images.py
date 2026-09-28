"""Refresh selected historical great-auk images from Wikimedia Commons.

Each file links to its Commons record in the dossier. The manifest records the
source and license; the site serves small local WebP derivatives.
"""

import json
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/great-auk-gallery"
OUT.mkdir(parents=True, exist_ok=True)
FILES = [
    ("worm-1655", "Wormius' Great Auk.jpg", "Ole Worm, Museum Wormianum, 1655", "Public domain"),
    ("bewick-1804", "Great Auk Thomas Bewick 1804.jpg", "Thomas Bewick, A History of British Birds, 1804", "Public domain"),
    ("audubon-1838", "341 Great Auk.jpg", "John James Audubon, Birds of America, plate 341, 1827–1838", "Public domain"),
    ("egg-1888", "A great auk egg. Coloured lithograph by F. W. Frohawk, 1888. Wellcome V0022387.jpg", "F. W. Frohawk, 1888; Wellcome Collection", "CC BY 4.0"),
]


def image_info(filename):
    query = urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "imageinfo", "iiprop": "url|size",
        "iiurlwidth": "1400", "titles": f"File:{filename}",
    })
    request = urllib.request.Request(
        "https://commons.wikimedia.org/w/api.php?" + query,
        headers={"User-Agent": "HistoricalAtlasResearch/1.0"},
    )
    result = json.load(urllib.request.urlopen(request))
    return next(iter(result["query"]["pages"].values()))["imageinfo"][0]


manifest = []
for slug, filename, credit, license_name in FILES:
    info = image_info(filename)
    request = urllib.request.Request(info.get("thumburl", info["url"]), headers={"User-Agent": "HistoricalAtlasResearch/1.0"})
    with Image.open(BytesIO(urllib.request.urlopen(request).read())) as image:
        image.convert("RGB").save(OUT / f"{slug}.webp", "WEBP", quality=84, method=6)
        if slug == "worm-1655":
            # Preserve the original scan above; this ink-only copy sits on the
            # atlas paper color in the dossier hero.
            grey = image.convert("L")
            ink = Image.new("RGBA", grey.size, (28, 27, 25, 0))
            ink.putalpha(ImageOps.invert(grey))
            ink.save(OUT / "worm-1655-ink.webp", "WEBP", lossless=True, method=6)
    manifest.append({
        "slug": slug,
        "file": filename,
        "source": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(filename.replace(" ", "_")),
        "credit": credit,
        "license": license_name,
        "local": f"assets/great-auk-gallery/{slug}.webp",
        **({"display_derivative": "assets/great-auk-gallery/worm-1655-ink.webp"} if slug == "worm-1655" else {}),
    })
    print(slug, info["width"], info["height"])

(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
