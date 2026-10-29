"""Join independently reviewed call intervals to behavioral observation windows."""
import argparse
import csv
import math
from pathlib import Path

CALL_FIELDS = ("session_id", "call_id", "start_s", "end_s", "species", "call_type", "confidence")
EVENT_FIELDS = ("session_id", "start_s", "end_s", "event")
OUTPUT_FIELDS = (*CALL_FIELDS, "event", "link_status")


def read_table(path, fields):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not set(fields).issubset(reader.fieldnames):
            raise ValueError(f"{path}: expected columns {', '.join(fields)}")
        rows = []
        for number, row in enumerate(reader, 2):
            if any(not (row.get(field) or "").strip() for field in fields):
                raise ValueError(f"{path}:{number}: required fields must be nonblank")
            clean = {field: row[field].strip() for field in fields}
            try:
                start, end = float(clean["start_s"]), float(clean["end_s"])
            except ValueError as exc:
                raise ValueError(f"{path}:{number}: invalid timestamp") from exc
            if not (math.isfinite(start) and math.isfinite(end) and 0 <= start < end):
                raise ValueError(f"{path}:{number}: require finite 0 <= start < end")
            clean["_start"], clean["_end"] = start, end
            rows.append(clean)
        return rows


def link(calls, windows):
    ids = set()
    result = []
    for call in calls:
        key = (call["session_id"], call["call_id"])
        if key in ids:
            raise ValueError(f"Duplicate call ID in session: {key}")
        ids.add(key)
        overlaps = [w for w in windows if w["session_id"] == call["session_id"]
                    and w["_start"] < call["_end"] and call["_start"] < w["_end"]]
        output = {field: call[field] for field in CALL_FIELDS}
        if len(overlaps) == 1 and overlaps[0]["_start"] <= call["_start"] and call["_end"] <= overlaps[0]["_end"]:
            output.update(event=overlaps[0]["event"], link_status="fully_covered")
        elif not overlaps:
            output.update(event="unknown", link_status="no_observation")
        else:
            output.update(event="unknown", link_status="ambiguous_overlap")
        result.append(output)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("calls", type=Path)
    parser.add_argument("events", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.output.resolve() in {args.calls.resolve(), args.events.resolve()}:
            raise ValueError("Output must not overwrite either input")
        linked = link(read_table(args.calls, CALL_FIELDS), read_table(args.events, EVENT_FIELDS))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
            writer.writeheader()
            writer.writerows(linked)
        print(f"Linked {len(linked)} calls; unknown: {sum(r['event'] == 'unknown' for r in linked)}")
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
