#!/usr/bin/env python3
"""news-image-20261125 v9 entrypoint (standard library only).

Copies the pre-rendered entry.png (drawn by render.py, PIL, at build time)
to $MAKEFUN_OUTPUT_DIR/entry.png. Deterministic: both runs write the
same bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
