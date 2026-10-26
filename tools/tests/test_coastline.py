"""Regression checks for offset curls, using only the Python standard library."""
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('coastline', ROOT / 'tools/osm_coastline.py')
coast = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coast)


class CoastlineTests(unittest.TestCase):
    def test_crossed_offset_loop_is_trimmed_without_mutating_source(self):
        points = [(0, 0), (4, 4), (0, 4), (4, 0), (6, 0)]
        original = points.copy()
        self.assertEqual(coast.remove_offset_loops(points), [(0, 0), (2, 2), (4, 0), (6, 0)])
        self.assertEqual(points, original)

    def test_real_headland_is_not_sorted_or_flattened(self):
        points = [(0, 0), (4, 0), (4, 4), (2, 4), (2, 6), (8, 6)]
        self.assertEqual(coast.remove_offset_loops(points), points)

    def test_generated_beaches_share_exact_endpoints(self):
        data = json.loads((ROOT / 'web/data/zones-geometry.json').read_text())
        beaches = list(data['zones'].values()) + list(data['provisional'].values())
        for left, right in zip(beaches, beaches[1:]):
            self.assertEqual(left[-1], right[0])

    def test_cocles_does_not_double_back_at_reported_hook(self):
        data = json.loads((ROOT / 'web/data/zones-geometry.json').read_text())
        points = data['zones']['cg:zone/cocles']
        bend = [p for p in points if -82.7424 < p[1] < -82.7415]
        self.assertGreater(len(bend), 2)
        self.assertTrue(all(b[1] >= a[1] for a, b in zip(bend, bend[1:])), bend)


if __name__ == '__main__':
    unittest.main()
