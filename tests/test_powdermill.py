import csv
import hashlib
import io
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PowdermillTests(unittest.TestCase):
    def test_source_integrity_and_annotation_window(self):
        audio = ROOT / "data/powdermill/Recording_1_Segment_22.mp3"
        annotations = ROOT / "data/powdermill/annotation_Files.zip"
        self.assertEqual(hashlib.sha256(audio.read_bytes()).hexdigest(),
                         "3cc6aadb45c7adbf44f2f514686a16bc2965a9d87446763cf95dff3fce22c789")
        self.assertEqual(hashlib.md5(annotations.read_bytes()).hexdigest(),
                         "8f78ba7cf9fc5d25656f7747ed3406d1")
        with zipfile.ZipFile(annotations) as archive:
            with archive.open("Recording_1/Recording_1_Segment_22.Table.1.selections.txt") as raw:
                rows = list(csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig"), delimiter="\t"))
        matches = [r for r in rows if r["Species"] == "AMCR"
                   and float(r["Begin Time (s)"]) >= 145 and float(r["End Time (s)"]) <= 205]
        self.assertEqual(len(matches), 7)


if __name__ == "__main__":
    unittest.main()
