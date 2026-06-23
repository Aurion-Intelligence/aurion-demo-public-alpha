"""
Path helpers — cross-platform, pathlib-only, with strict workspace boundaries.

All public artifacts use repo-relative POSIX paths so nothing platform-specific or local leaks into
committed/evidence files.
"""
from __future__ import annotations

from pathlib import Path

# Repo root = parent of the aurion_demo package directory.
REPO_ROOT = Path(__file__).resolve().parents[1]

# The bundled, read-only sample workspace shipped with the package.
WORKSPACE_DIR = (Path(__file__).resolve().parent / "workspace").resolve()

# The single sample file the mission is allowed to read.
SAMPLE_NOTE = WORKSPACE_DIR / "project_note.md"

# Generated artifacts live here (git-ignored). Created at run time.
GENERATED_DIR = (REPO_ROOT / "artifacts" / "demo" / "generated").resolve()


def rel_to_repo(path: Path) -> str:
    """Return a repo-relative POSIX path string (never an absolute/local path)."""
    p = Path(path).resolve()
    try:
        return p.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        # Outside the repo — return just the name so we never leak an absolute local path.
        return p.name


def is_within(child: Path, parent: Path) -> bool:
    """True if `child` is `parent` or a descendant of it, after resolving. No path escapes."""
    child_r = Path(child).resolve()
    parent_r = Path(parent).resolve()
    return child_r == parent_r or parent_r in child_r.parents
