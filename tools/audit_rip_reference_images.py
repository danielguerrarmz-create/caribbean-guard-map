"""Recheck the Aguas Claras reference image against the map's local z17 tiles.

The other four supplied JPEGs do not produce a reliable satellite feature match.
Their map markers are area associations from the named 2026 map locations, not
pixel-level registrations. This audit deliberately does not invent one.
"""

import json
import math
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "web/data/rip-reference-images.json").read_text(encoding="utf8"))
REFERENCE = next(f for f in DATA["features"] if f["id"] == "aguas")
ZOOM = 17
TILE_SIZE = 256


def tile_at(lon, lat):
    n = 2**ZOOM
    return (int((lon + 180) / 360 * n),
            int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n))


def geographic_at(px, py, origin_x, origin_y):
    n = 2**ZOOM
    x = origin_x + px / TILE_SIZE
    y = origin_y + py / TILE_SIZE
    return [x / n * 360 - 180,
            math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))]


def main():
    center_x, center_y = tile_at(-82.717, 9.643)
    origin_x, origin_y = center_x - 2, center_y - 2
    mosaic = np.zeros((5 * TILE_SIZE, 5 * TILE_SIZE, 3), dtype=np.uint8)
    for x in range(origin_x, origin_x + 5):
        for y in range(origin_y, origin_y + 5):
            file = ROOT / f"web/tiles/{ZOOM}/{x}/{y}.jpg"
            if not file.is_file():
                raise SystemExit(f"Missing tile: {file}")
            mosaic[(y - origin_y) * TILE_SIZE:(y - origin_y + 1) * TILE_SIZE,
                   (x - origin_x) * TILE_SIZE:(x - origin_x + 1) * TILE_SIZE] = cv2.imread(str(file))

    source = cv2.imread(str(ROOT / "web" / REFERENCE["image"]))
    height, width = source.shape[:2]
    cropped = source[85:height - 35, 40:width - 25]
    hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    hue, saturation, _ = cv2.split(hsv)
    red = ((hue < 12) | (hue > 170)) & (saturation > 90)
    mask = np.where(red, 0, 255).astype("uint8")

    sift = cv2.SIFT_create(nfeatures=50000)
    source_points, source_descriptors = sift.detectAndCompute(
        cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY), mask)
    tile_points, tile_descriptors = sift.detectAndCompute(
        cv2.cvtColor(mosaic, cv2.COLOR_BGR2GRAY), None)
    pairs = cv2.BFMatcher().knnMatch(source_descriptors, tile_descriptors, k=2)
    matches = [m for m, n in pairs if m.distance < 0.7 * n.distance]
    src = np.float32([source_points[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst = np.float32([tile_points[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    matrix, selected = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
    if matrix is None or selected is None or int(selected.sum()) < 1000:
        raise SystemExit("Image registration lacks enough inliers")

    h, w = cropped.shape[:2]
    corners = np.float32([[[0, 0]], [[w, 0]], [[w, h]], [[0, h]]])
    pixels = cv2.perspectiveTransform(corners, matrix)[:, 0, :]
    fitted = [geographic_at(float(x), float(y), origin_x, origin_y) for x, y in pixels]
    stored = REFERENCE["image_footprint"]
    # Rough local conversion is sufficient for a comparison against the stored
    # transform, not a claim of independent geographic accuracy.
    differences = [math.hypot((a[0] - b[0]) * 109700, (a[1] - b[1]) * 110600)
                   for a, b in zip(fitted, stored)]
    if max(differences) > 5:
        raise SystemExit(f"Stored image footprint drifted by {max(differences):.1f} m")
    print(f"PASS: {int(selected.sum())} inliers; footprint drift <= {max(differences):.1f} m")


if __name__ == "__main__":
    main()
