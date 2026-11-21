#!/usr/bin/env python3
"""Entrypoint: place the pre-rendered front page at the output path.

The picture itself is drawn by draw21.py and committed as entry.png.
This program only copies that exact file to $MAKEFUN_OUTPUT_DIR/entry.png
so both grading runs produce identical bytes. It never renders, never
touches the network, and never writes anywhere but the output directory.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        print("entry.png is missing next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    before = sha256_of(SOURCE)
    shutil.copyfile(SOURCE, target)
    after = sha256_of(target)
    if before != after:
        print("copy mismatch: source and output differ", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)"
          % (target, os.path.getsize(target), after))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
