"""Build the two small, repeatable print-grain tiles used by the interface."""

from pathlib import Path
from random import Random

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SIZE = 256


def paper_grain():
    random = Random(1904)
    tile = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    pixels = tile.load()
    for y in range(SIZE):
        for x in range(SIZE):
            if random.random() < 0.49:
                pixels[x, y] = (73, 58, 37, random.randint(2, 9))
    draw = ImageDraw.Draw(tile, "RGBA")
    for _ in range(105):
        x, y = random.randrange(SIZE), random.randrange(SIZE)
        draw.line((x, y, x + random.randrange(2, 8), y), fill=(71, 56, 36, 8))
    tile.save(ROOT / "assets" / "paper-grain.png", optimize=True)


def ink_wear():
    random = Random(1644)
    tile = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tile, "RGBA")
    for _ in range(1650):
        x, y = random.randrange(SIZE), random.randrange(SIZE)
        draw.point((x, y), fill=(249, 236, 213, random.randrange(16, 66)))
    for _ in range(160):
        x, y = random.randrange(SIZE), random.randrange(SIZE)
        draw.line((x, y, x + random.randrange(1, 4), y), fill=(247, 231, 205, random.randrange(28, 82)))
    for _ in range(280):
        x, y = random.randrange(SIZE), random.randrange(SIZE)
        draw.point((x, y), fill=(39, 27, 22, random.randrange(11, 37)))
    tile.save(ROOT / "assets" / "ink-wear.png", optimize=True)


paper_grain()
ink_wear()
