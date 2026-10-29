import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from link_annotations import link, read_table, CALL_FIELDS, EVENT_FIELDS

ROOT = Path(__file__).resolve().parents[1]


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.calls = read_table(ROOT / "examples/calls.csv", CALL_FIELDS)
        self.windows = read_table(ROOT / "examples/events.csv", EVENT_FIELDS)

    def test_full_partial_and_unobserved(self):
        rows = link(self.calls, self.windows)
        self.assertEqual([(r["event"], r["link_status"]) for r in rows],
                         [("none", "fully_covered"), ("unknown", "ambiguous_overlap"),
                          ("unknown", "no_observation")])

    def test_multiple_overlapping_windows_are_ambiguous(self):
        windows = self.windows + [dict(self.windows[0], event="other")]
        self.assertEqual(link(self.calls, windows)[0]["link_status"], "ambiguous_overlap")

    def test_duplicate_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate call ID"):
            link(self.calls + self.calls[:1], self.windows)

    def test_windows_from_another_session_do_not_match(self):
        windows = [dict(self.windows[0], session_id="other")]
        self.assertEqual(link(self.calls[:1], windows)[0]["link_status"], "no_observation")


if __name__ == "__main__":
    unittest.main()
