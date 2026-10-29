import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rook_inventory import inventory

ROOT = Path(__file__).resolve().parents[1]


class ArchiveTests(unittest.TestCase):
    def test_published_archive_totals(self):
        report = inventory(ROOT / "data/rook/clean_labels.zip")
        self.assertEqual(report["tsv_files"], 107)
        self.assertEqual(report["counts"]["annotation_rows"], 31148)
        self.assertEqual(report["counts"]["special_source"], 3320)
        self.assertEqual(report["invalid_intervals"], [])

    def test_changed_archive_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "changed.zip"
            path.write_bytes(b"not the source archive")
            with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                inventory(path)


if __name__ == "__main__":
    unittest.main()
