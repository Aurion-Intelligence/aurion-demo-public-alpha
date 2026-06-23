#!/usr/bin/env python3
"""Generate alpha readiness status + known issues from real repo artifacts.

[alpha-status-autogenerator-001]

Writes (all GENERATED — do not edit by hand):
  - artifacts/alpha/alpha_status.json
  - docs/alpha/ALPHA_STATUS.md
  - docs/alpha/KNOWN_ISSUES.md

Evidence-derived + anti-fake-green: `public_alpha_ready` is false unless every hard gate passes;
missing/stale artifacts become staleness warnings, never a fake green. No network, no `.env`.

Run:
    python scripts/alpha/generate_alpha_status.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from aurion.alpha.status import GENERATED_NOTICE, build_status  # noqa: E402

JSON_PATH = _REPO_ROOT / "artifacts" / "alpha" / "alpha_status.json"
STATUS_MD = _REPO_ROOT / "docs" / "alpha" / "ALPHA_STATUS.md"
ISSUES_MD = _REPO_ROOT / "docs" / "alpha" / "KNOWN_ISSUES.md"

_BADGE = {"green": "🟢 GREEN", "yellow": "🟡 YELLOW", "red": "🔴 RED"}
_GATE_ICON = {"pass": "✅", "fail": "❌", "unknown": "❓"}


def _gate_table(gates: dict) -> str:
    rows = ["| Gate | Status | Detail / reason |", "|---|---|---|"]
    for key, g in gates.items():
        icon = _GATE_ICON.get(g.get("status"), "❓")
        detail = g.get("detail") or g.get("reason") or ("" if g.get("status") == "pass" else "")
        rows.append(f"| {g.get('label', key)} | {icon} {g.get('status')} | {str(detail)[:160]} |")
    return "\n".join(rows)


def _bullets(items: list) -> str:
    items = [str(x) for x in (items or []) if str(x).strip()]
    return "\n".join(f"- {x}" for x in items) if items else "_(none)_"


def render_status_md(status: dict) -> str:
    fs = (status.get("evidence") or {}).get("full_safe") or {}
    fs_line = (
        f"`{fs.get('run_id')}` — {fs.get('jobs_passed')}/{fs.get('jobs_run')} jobs"
        if fs.get("available") else "_no full-safe run found_"
    )
    return f"""# Aurion Alpha Status

> **{GENERATED_NOTICE}**
> Regenerate with `python scripts/alpha/generate_alpha_status.py`.

**Generated:** {status['generated_at']}

## Overall status

# {_BADGE.get(status['overall_status'], status['overall_status'])}

{status['readiness_summary']}

## Readiness

- **Public alpha ready:** {'**yes**' if status['public_alpha_ready'] else '**no**'}
- **Demo public alpha ready:** {'**yes**' if status.get('demo_public_alpha_ready') else '**no**'} _(bounded, fixture-backed proof pack — not full release)_
- **Developer alpha ready:** {'**yes**' if status['developer_alpha_ready'] else '**no**'}

## Gates

{_gate_table(status['gates'])}

## Latest full-safe run

{fs_line}

## Latest mission drill receipts

{_bullets(status.get('last_drill_receipts'))}

## Known blockers (public alpha)

{_bullets(status.get('blocking_issues'))}

## Non-blocking debt

{_bullets(status.get('non_blocking_debt'))}

## Staleness warnings

{_bullets(status.get('staleness_warnings'))}

## Evidence TODO refs

{_bullets(status.get('todo_refs'))}

---

*This page is the source of truth for Aurion's alpha readiness. Public alpha must not be claimed
while `public_alpha_ready` is `no`. See [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md).*
"""


def render_issues_md(status: dict) -> str:
    return f"""# Aurion Alpha — Known Issues

> **{GENERATED_NOTICE}**
> Regenerate with `python scripts/alpha/generate_alpha_status.py`.

**Generated:** {status['generated_at']} · Overall: **{status['overall_status']}** ·
Public alpha ready: **{'yes' if status['public_alpha_ready'] else 'no'}**

## Public-alpha blockers

{_bullets(status.get('blocking_issues'))}

## Developer-alpha caveats / known issues

{_bullets(status.get('known_issues'))}

## Non-alpha test debt

{_bullets(status.get('non_blocking_debt'))}

## Staleness warnings

{_bullets(status.get('staleness_warnings'))}

## What Aurion should NOT claim yet

- Aurion is **not production ready** and is **not** a finished product.
- Do **not** claim public alpha readiness while the status page says `public_alpha_ready: no`.
- Do **not** present unfinished dev/lab modules (behind Developer Mode) as alpha features.
- Missing data, refused actions, and unavailable links are shown honestly — never as fake green.

---

*Generated from real repo/test/drill/artifact evidence so alpha claims cannot drift into
fake-green marketing.*
"""


def main() -> int:
    status = build_status()
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_MD.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
    STATUS_MD.write_text(render_status_md(status), encoding="utf-8")
    ISSUES_MD.write_text(render_issues_md(status), encoding="utf-8")
    print("Alpha status generated:")
    print(f"  overall: {status['overall_status']} | public_alpha_ready: {status['public_alpha_ready']} | "
          f"developer_alpha_ready: {status['developer_alpha_ready']}")
    print(f"  JSON : {JSON_PATH.relative_to(_REPO_ROOT)}")
    print(f"  STATUS: {STATUS_MD.relative_to(_REPO_ROOT)}")
    print(f"  ISSUES: {ISSUES_MD.relative_to(_REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
