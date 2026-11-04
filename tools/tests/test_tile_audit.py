"""Regression coverage for the cloud tile build's offline audit."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('tile_builder', Path(__file__).parents[1] / 'build_tiles.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class TileAuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.previous_root = builder.ROOT
        builder.ROOT = self.temp.name
        self.web = Path(self.temp.name) / 'web'
        (self.web / 'icons' / 'source-library').mkdir(parents=True)
        (self.web / 'coastal.css').write_text('body{}')
        (self.web / 'icons' / 'app.png').write_bytes(b'fixture')
        (self.web / 'sw.js').write_text('const CRITICAL = [\n"./", "coastal.css?v=75", "icons/app.png"\n].concat([]);\nconst OPTIONAL = [\n\n].concat([]);')
        (self.web / 'manifest.json').write_text(json.dumps({'icons': [{'src': 'icons/app.png'}]}))

    def tearDown(self):
        builder.ROOT = self.previous_root
        self.temp.cleanup()

    def audit(self):
        with contextlib.redirect_stdout(io.StringIO()):
            builder.audit_precache()

    def test_versioned_assets_resolve_and_unused_source_collections_are_not_precached(self):
        self.audit()

    def test_missing_declared_asset_still_fails(self):
        (self.web / 'sw.js').write_text((self.web / 'sw.js').read_text().replace('coastal.css', 'missing.css'))
        with self.assertRaises(SystemExit):
            self.audit()

    def test_unlisted_launcher_icon_still_fails(self):
        (self.web / 'manifest.json').write_text(json.dumps({'icons': [{'src': 'icons/missing.png'}]}))
        with self.assertRaises(SystemExit):
            self.audit()


if __name__ == '__main__':
    unittest.main()
