"""Inventory the original Zenodo rook annotation archive without extracting it."""
import argparse
import collections
import csv
import hashlib
import io
import json
import math
import zipfile
from pathlib import Path

EXPECTED_MD5 = "4e500dd53a5a3f654e696e1790dd52ef"
REQUIRED = {"Start", "End", "Source", "Event", "Comment", "Sex", "Colony", "Song"}


def inventory(path):
    digest = hashlib.md5(path.read_bytes()).hexdigest()  # Source integrity, not security.
    if digest != EXPECTED_MD5:
        raise ValueError(f"Archive checksum mismatch: {digest}")
    counts = collections.Counter()
    categories = {k: collections.Counter() for k in ("Colony", "Source", "Song", "Sex")}
    bad = []
    dates = set()
    files = 0
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if not name.endswith(".tsv"):
                continue
            files += 1
            dates.add(Path(name).name[:8])
            with archive.open(name) as member:
                reader = csv.DictReader(io.TextIOWrapper(member, encoding="utf-8-sig", newline=""), delimiter="\t")
                if not REQUIRED.issubset(reader.fieldnames or []):
                    raise ValueError(f"Missing columns in {name}")
                for line, row in enumerate(reader, 2):
                    counts["annotation_rows"] += 1
                    for key, counter in categories.items():
                        counter[(row.get(key) or "").strip()] += 1
                    if not (row.get("Event") or "").strip():
                        counts["blank_event"] += 1
                    if (row.get("Source") or "").strip() in {"Inc", "Pls", "Comment", "Ignore"}:
                        counts["special_source"] += 1
                    try:
                        start, end = float(row["Start"]), float(row["End"])
                        if not (math.isfinite(start) and math.isfinite(end) and 0 <= start < end):
                            raise ValueError
                    except (KeyError, TypeError, ValueError):
                        bad.append(f"{name}:{line}")
    if not files:
        raise ValueError("No TSV files in archive")
    return {"archive_md5": digest, "tsv_files": files, "distinct_filename_dates": len(dates),
            "counts": dict(sorted(counts.items())), "categories": {k: dict(sorted(v.items())) for k, v in categories.items()},
            "invalid_intervals": bad}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = inventory(args.archive)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"{report['tsv_files']} files, {report['counts']['annotation_rows']} annotation rows, "
              f"{len(report['invalid_intervals'])} invalid intervals; wrote {args.output}")
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        parser.exit(1, f"Error: {exc}\n")
