"""Build the small, self-contained Natural Earth land layer used by the atlas.

Source: Natural Earth 1:50m land, public domain.
https://www.naturalearthdata.com/about/terms-of-use/
https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_50m_land.geojson

Usage: python3 scripts/build_map.py /path/to/ne_50m_land.geojson
The generated JS is committed, so deployment has no network dependency.
"""

import json
import sys
from pathlib import Path

WEST, EAST, SOUTH, NORTH = 13.0, 31.0, 27.0, 39.0
WIDTH, HEIGHT = 1200, 700


def clip(points, axis, bound, keep_greater):
    """Sutherland–Hodgman clipping against one geographic edge."""
    if not points:
        return []
    output = []

    def inside(point):
        value = point[axis]
        return value >= bound if keep_greater else value <= bound

    previous = points[-1]
    for current in points:
        current_inside = inside(current)
        previous_inside = inside(previous)
        if current_inside != previous_inside:
            difference = current[axis] - previous[axis]
            if difference:
                ratio = (bound - previous[axis]) / difference
                intersection = [
                    previous[0] + ratio * (current[0] - previous[0]),
                    previous[1] + ratio * (current[1] - previous[1]),
                ]
                output.append(intersection)
        if current_inside:
            output.append(current)
        previous = current
    return output


def project(point):
    lon, lat = point
    return (
        (lon - WEST) * WIDTH / (EAST - WEST),
        (NORTH - lat) * HEIGHT / (NORTH - SOUTH),
    )


def main():
    source = Path(sys.argv[1])
    data = json.loads(source.read_text())
    paths = []
    for feature in data["features"]:
        geometry = feature["geometry"]
        polygons = (
            [geometry["coordinates"]]
            if geometry["type"] == "Polygon"
            else geometry["coordinates"]
        )
        for polygon in polygons:
            ring = polygon[0]  # Outer coastlines; inland water is not needed here.
            if not any(WEST - 1 <= p[0] <= EAST + 1 and SOUTH - 1 <= p[1] <= NORTH + 1 for p in ring):
                continue
            points = ring
            for axis, bound, greater in (
                (0, WEST, True),
                (0, EAST, False),
                (1, SOUTH, True),
                (1, NORTH, False),
            ):
                points = clip(points, axis, bound, greater)
            if len(points) < 3:
                continue
            projected = [project(p) for p in points]
            path = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in projected) + "Z"
            paths.append(path)

    target = Path(__file__).parent.parent / "assets" / "map-geometry.js"
    target.write_text(
        "// Public-domain Natural Earth 1:50m land, projected and clipped to Cyrenaica.\n"
        + "export const landPaths = "
        + json.dumps(paths, separators=(",", ":"))
        + ";\n"
    )
    print(f"Wrote {len(paths)} polygons to {target} ({target.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
