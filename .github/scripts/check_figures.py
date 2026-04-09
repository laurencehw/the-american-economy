#!/usr/bin/env python3
"""
Check that every <img src="..."> reference in the book Markdown files
points to a file that actually exists in the repository.
"""
import os
import re
import sys

BOOK_DIR = "book"
IMG_PATTERN = re.compile(r'<img\s+src="([^"]+)"')

errors = []
checked = 0

for root, dirs, files in os.walk(BOOK_DIR):
    for fname in files:
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath) as f:
            content = f.read()

        for match in IMG_PATTERN.finditer(content):
            src = match.group(1)
            # Resolve relative to the markdown file's directory
            md_dir = os.path.dirname(fpath)
            resolved = os.path.normpath(os.path.join(md_dir, src))
            checked += 1
            if not os.path.exists(resolved):
                line = content[: match.start()].count("\n") + 1
                errors.append(f"  {fpath}:{line} — missing: {src}")

print(f"Checked {checked} figure references.")

if errors:
    print(f"\n❌ {len(errors)} broken figure reference(s) found:\n")
    for e in errors:
        print(e)
    sys.exit(1)
else:
    print("✅ All figure references are valid.")
