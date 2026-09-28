"""Project public-domain Natural Earth 1:50m land for the great auk map.

Usage: python3 scripts/build_auk_map.py /path/to/ne_50m_land.geojson
Source: https://www.naturalearthdata.com/downloads/50m-physical-vectors/50m-land/
"""

import json
import sys
from pathlib import Path

from build_map import clip

WEST, EAST, SOUTH, NORTH = -67.0, 15.0, 45.0, 70.0
WIDTH, HEIGHT = 1200, 700


def project(point):
    lon, lat = point
    return ((lon - WEST) * WIDTH / (EAST - WEST), (NORTH - lat) * HEIGHT / (NORTH - SOUTH))


def main():
    data = json.loads(Path(sys.argv[1]).read_text())
    paths = []
    for feature in data["features"]:
        geometry = feature["geometry"]
        polygons = [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]
        for polygon in polygons:
            ring = polygon[0]
            if not any(WEST - 1 <= p[0] <= EAST + 1 and SOUTH - 1 <= p[1] <= NORTH + 1 for p in ring):
                continue
            points = ring
            for axis, bound, greater in ((0, WEST, True), (0, EAST, False), (1, SOUTH, True), (1, NORTH, False)):
                points = clip(points, axis, bound, greater)
            if len(points) < 3:
                continue
            coordinates = [project(p) for p in points]
            paths.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in coordinates) + "Z")
    target = Path(__file__).resolve().parents[1] / "assets/auk-map-geometry.js"
    target.write_text("// Natural Earth 1:50m land, public domain; clipped to the North Atlantic.\nexport const aukLandPaths = " + json.dumps(paths, separators=(",", ":")) + ";\n")
    print(f"Wrote {len(paths)} polygons ({target.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
