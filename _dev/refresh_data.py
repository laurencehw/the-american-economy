#!/usr/bin/env python3
"""Reconcile the manuscript's numbers against the series it cites.

The book states a reference year for every table and names its source beneath
it. This script reads those declarations, fetches the series that can be
fetched, and writes a report saying where the book and the sources disagree and
what a refresh would involve.

It never edits the manuscript. The output is a diff for a human to act on.

Usage
-----
    python3 _dev/refresh_data.py --report            # fetch and write the report
    python3 _dev/refresh_data.py --report --offline  # cached responses only
    python3 _dev/refresh_data.py --check             # verify registry locators (CI)
    python3 _dev/refresh_data.py --inventory         # dump the table inventory as CSV

Credentials
-----------
Neither provider needs a key for the volume this script uses, but keys raise the
limits and are read from the environment if set:

    FRED_API_KEY   https://fredaccount.stlouisfed.org/apikeys
    BLS_API_KEY    https://data.bls.gov/registrationEngine/
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from refresh import inventory, registry, report  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
DEFAULT_REPORT = REPO / "_dev" / "RECONCILIATION.md"


def cmd_check() -> int:
    """Verify the registry still matches the manuscript. Suitable for CI."""
    result = registry.verify_locators(REPO)
    inv = inventory.scan(REPO / "book")
    print(f"Registry locators: {len(result.ok)} matching, {len(result.broken)} broken.")
    print(f"Tables parsed: {len(inv.tables)}, problems: {len(inv.problems)}.")
    for broken in result.broken:
        print(f"  ❌ locator no longer matches: {broken}")
    for problem in inv.problems:
        print(f"  ❌ {problem}")
    if result.broken or inv.problems:
        print("\nA broken locator means the manuscript changed under the registry.")
        print("Update the pattern in _dev/refresh/registry.py to match the new wording.")
        return 1
    print("✅ Registry and manuscript agree.")
    return 0


def cmd_inventory(out: Path | None) -> int:
    inv = inventory.scan(REPO / "book")
    rows = [
        {
            "table": t.number,
            "chapter": t.chapter,
            "title": t.title,
            "file": str(t.path.relative_to(REPO)),
            "line": t.caption_line,
            "rows": t.rows,
            "source_kind": t.kind,
            "reference_year": t.year or "",
            "source": t.source_text,
        }
        for t in inv.tables
    ]
    handle = out.open("w", newline="", encoding="utf-8") if out else sys.stdout
    try:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if out:
            handle.close()
            print(f"Wrote {len(rows)} tables to {out}")
    return 0


def cmd_report(out: Path, *, offline: bool, refresh: bool, as_of: int | None) -> int:
    text = report.render(REPO, offline=offline, refresh=refresh, as_of=as_of)
    out.write_text(text, encoding="utf-8")
    print(f"Wrote {out} ({len(text.splitlines())} lines)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--report", action="store_true", help="write the reconciliation report")
    mode.add_argument("--check", action="store_true", help="verify registry locators, exit non-zero on drift")
    mode.add_argument("--inventory", action="store_true", help="dump the table inventory as CSV")
    parser.add_argument("--offline", action="store_true", help="use cached responses only, never the network")
    parser.add_argument("--refresh", action="store_true", help="re-fetch even if the cache is fresh")
    parser.add_argument("--as-of", type=int, default=None, help="year to measure table staleness against")
    parser.add_argument("--out", type=Path, default=None, help="output path")
    args = parser.parse_args(argv)

    if args.check:
        return cmd_check()
    if args.inventory:
        return cmd_inventory(args.out)
    return cmd_report(args.out or DEFAULT_REPORT, offline=args.offline,
                      refresh=args.refresh, as_of=args.as_of)


if __name__ == "__main__":
    raise SystemExit(main())
