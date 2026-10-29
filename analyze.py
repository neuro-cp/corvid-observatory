"""Summarize manually annotated corvid calls; no meaning is inferred."""
import csv
import sys
from collections import Counter
from pathlib import Path

REQUIRED = {"session_id", "species", "call_type", "event", "confidence"}


def main(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
        rows = list(reader)
    for number, row in enumerate(rows, 2):
        if any(not (row.get(key) or "").strip() for key in REQUIRED):
            raise ValueError(f"Line {number}: required fields cannot be blank")
    print(f"Annotated calls: {len(rows)}; sessions with calls: {len({r['session_id'] for r in rows})}")
    print("Counts by species, event, and call type:")
    counts = Counter((r['species'].strip(), r['event'].strip(), r['call_type'].strip()) for r in rows)
    for (species, event, call), count in sorted(counts.items()):
        print(f"  {species} | {event} | {call}: {count}")
    print("Descriptive counts only; observation effort and dependence are not accounted for.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python analyze.py observations.csv")
    try:
        main(sys.argv[1])
    except (OSError, ValueError, csv.Error) as exc:
        sys.exit(f"Error: {exc}")
