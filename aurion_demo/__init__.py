"""
aurion_demo — a small, real, cross-platform bounded governed-mission runtime.

This is a deliberately bounded *public* implementation of Aurion's governed mission spine:

    Goal -> deterministic plan -> microsteps -> permission evaluation
         -> allowed local read -> allowed bounded artifact write
         -> blocked external-network step
         -> fresh AuditLedger events -> fresh BlackBox decisions -> fresh Mission Receipt

It is **not** the full Aurion runtime. It contains no private implementations, no live autonomy, no
cloud routing, no spending, no personal memory, and no network access. It runs offline with the Python
standard library only, on Linux, macOS, and Windows.

Public entry points:
    python3 -m aurion_demo run       (Linux/macOS)
    py -m aurion_demo run            (Windows)
    python scripts/demo/run_governed_mission.py   (direct script fallback)
"""
from __future__ import annotations

__all__ = ["__version__"]
__version__ = "0.1.0"
