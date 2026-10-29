"""Describe annotation durations per identified rook, not independent trials."""
import argparse
import csv
import io
import statistics
import zipfile
from collections import defaultdict
from pathlib import Path
from rook_inventory import inventory

SPECIAL = {"Inc", "Pls", "Comment", "Ignore", ""}
FIELDS = ("colony", "source", "sex", "song", "rows", "median_duration_s", "files")


def summarize(archive_path):
    checked = inventory(archive_path)
    if checked["invalid_intervals"]:
        raise ValueError("Invalid intervals in archive")
    groups = defaultdict(list)
    files = defaultdict(set)
    metadata = defaultdict(set)
    with zipfile.ZipFile(archive_path) as archive:
        for name in sorted(archive.namelist()):
            if not name.endswith(".tsv"):
                continue
            with archive.open(name) as raw:
                for row in csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""), delimiter="\t"):
                    source = row["Source"].strip()
                    colony = row["Colony"].strip()
                    sex = row["Sex"].strip()
                    song = row["Song"].strip().upper()
                    if source in SPECIAL:
                        continue
                    if not colony or sex not in {"Male", "Female"} or song not in {"TRUE", "FALSE"}:
                        raise ValueError(f"Unexpected metadata for {source} in {name}")
                    metadata[(colony, source)].add(sex)
                    key = (colony, source, sex, song)
                    groups[key].append(float(row["End"]) - float(row["Start"]))
                    files[key].add(name)
    if any(len(sexes) != 1 for sexes in metadata.values()):
        raise ValueError("Inconsistent sex label for a source within a colony")
    return [{"colony": k[0], "source": k[1], "sex": k[2], "song": k[3],
             "rows": len(values), "median_duration_s": f"{statistics.median(values):.6f}",
             "files": len(files[k])} for k, values in sorted(groups.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.output.resolve() == args.archive.resolve():
            raise ValueError("Output must not overwrite the input archive")
        rows = summarize(args.archive)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} individual-by-song summaries to {args.output}")
        paired = defaultdict(dict)
        for row in rows:
            paired[(row["colony"], row["source"])][row["song"]] = float(row["median_duration_s"])
        differences = [v["TRUE"] - v["FALSE"] for v in paired.values() if set(v) == {"TRUE", "FALSE"}]
        print(f"Identified annotation rows: {sum(row['rows'] for row in rows)}; "
              f"individuals: {len(paired)}; individuals with both labels: {len(differences)}")
        if differences:
            print(f"Within-individual TRUE minus FALSE median durations: "
                  f"{sum(d < 0 for d in differences)} negative, {sum(d > 0 for d in differences)} positive, "
                  f"{sum(d == 0 for d in differences)} tied; median difference {statistics.median(differences):.6f} s")
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
