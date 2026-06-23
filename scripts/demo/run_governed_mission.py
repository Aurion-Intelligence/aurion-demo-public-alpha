#!/usr/bin/env python3
"""
Direct-script fallback for the bounded governed mission runtime.

Equivalent to `python3 -m aurion_demo run` (Linux/macOS) or `py -m aurion_demo run` (Windows). This
script just makes the repo root importable and delegates to the package CLI, so it works on any platform
with the Python standard library only — no network, no private imports.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from aurion_demo.cli import main  # noqa: E402

if __name__ == "__main__":
    # Default to `run` when invoked with no args.
    argv = sys.argv[1:] or ["run"]
    sys.exit(main(argv))
