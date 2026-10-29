import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rook_durations import summarize

ROOT = Path(__file__).resolve().parents[1]


class DurationTests(unittest.TestCase):
    def test_source_rows_are_grouped_and_specials_excluded(self):
        rows = summarize(ROOT / "data/rook/clean_labels.zip")
        self.assertEqual(sum(row["rows"] for row in rows), 27828)
        self.assertEqual(len({(row["colony"], row["source"]) for row in rows}), 22)
        self.assertTrue(all(row["source"] not in {"Inc", "Pls", "Ignore", "Comment"} for row in rows))
        aristotle = next(row for row in rows if row["source"] == "Aristotle" and row["song"] == "FALSE")
        self.assertEqual((aristotle["rows"], aristotle["median_duration_s"]), (451, "0.513057"))


if __name__ == "__main__":
    unittest.main()
