#!/usr/bin/env python3
"""
Check that every Markdown table in the book carries a numbered caption and a
source line, and that table numbers are unique and sequential within a file.

Conventions enforced:
  - A caption of the form ``**Table N.M: Title**`` sits above the table,
    separated from it by a blank line. N is the chapter number, the Interlude
    uses ``I``, and appendices use their letter (A, B, C, ...).
  - An attribution line follows within three lines of the table: either
    ``*Source: ...*`` or, for a table that illustrates a mechanism rather than
    reporting measured data, ``*Author's schematic*`` or ``*Illustrative...*``.
    It must be the whole line -- prose that merely mentions a source does not
    count. See book/how-to-use.md for the convention.
"""
import os
import re
import sys

BOOK_DIR = "book"
SEPARATOR = re.compile(r'^\|[ :|-]+\|\s*$')
CAPTION = re.compile(r'^\*\*Table ([0-9A-Z]+)\.(\d+):\s*.+\*\*\s*$')
# An attribution must be a declaration line of its own, not any nearby prose
# that happens to contain the word. Matching a bare substring let "Port
# Authorities" satisfy the check, silently exempting several tables.
ATTRIBUTION = re.compile(
    r"^\*(?:Source|Sources|Note):\s*\S.*\*$"
    r"|^\*(?:Illustrative|Author's (?:schematic|summary|compilation|synthesis))\b.*\*$",
    re.IGNORECASE,
)
# Files whose numbering prefix cannot be inferred from the filename.
PREFIX_OVERRIDES = {"interlude-inequality.md": "I"}


def prefix_for(fname):
    """Return the expected table-number prefix for a manuscript file."""
    if fname in PREFIX_OVERRIDES:
        return PREFIX_OVERRIDES[fname]
    chapter = re.match(r'ch(\d+)-', fname)
    if chapter:
        return str(int(chapter.group(1)))
    appendix = re.match(r'appendix-([a-z])-', fname)
    if appendix:
        return appendix.group(1).upper()
    return None


def tables(lines):
    """Yield (separator_index, end_index) for each Markdown table."""
    i = 0
    while i < len(lines):
        if SEPARATOR.match(lines[i]) and i > 0 and lines[i - 1].startswith("|"):
            j = i + 1
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            yield i, j
            i = j
        else:
            i += 1


errors = []
checked = 0

for root, dirs, files in os.walk(BOOK_DIR):
    for fname in sorted(files):
        if not fname.endswith(".md") or fname == "SUMMARY.md":
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, encoding="utf-8") as f:
            lines = f.read().split("\n")

        expected_prefix = prefix_for(fname)
        seen = {}
        expected_number = 0

        for sep, end in tables(lines):
            checked += 1
            # The caption is the nearest non-blank line above the header row.
            k = sep - 2
            while k >= 0 and not lines[k].strip():
                k -= 1
            caption = lines[k] if k >= 0 else ""
            match = CAPTION.match(caption)
            if not match:
                errors.append(f"  {fpath}:{sep + 1} — table has no numbered caption")
            else:
                prefix, number = match.group(1), int(match.group(2))
                expected_number += 1
                if expected_prefix and prefix != expected_prefix:
                    errors.append(
                        f"  {fpath}:{k + 1} — caption says Table {prefix}.{number}, "
                        f"expected prefix {expected_prefix}"
                    )
                if number in seen:
                    errors.append(
                        f"  {fpath}:{k + 1} — Table {prefix}.{number} duplicates "
                        f"line {seen[number]}"
                    )
                else:
                    seen[number] = k + 1
                if number != expected_number:
                    errors.append(
                        f"  {fpath}:{k + 1} — Table {prefix}.{number} is out of "
                        f"sequence, expected .{expected_number}"
                    )

            if not any(ATTRIBUTION.match(l.strip()) for l in lines[end:end + 4]):
                errors.append(f"  {fpath}:{end} — table has no source line")

print(f"Checked {checked} tables.")

if errors:
    print(f"\n❌ {len(errors)} table convention problem(s) found:\n")
    for e in errors:
        print(e)
    print(
        "\nEvery table needs a caption (**Table N.M: Title**) above it and a "
        "*Source:* line below it. See book/how-to-use.md."
    )
    sys.exit(1)
else:
    print("✅ All tables are numbered and sourced.")
