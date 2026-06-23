"""
CLI for aurion_demo.

  run     Execute a fresh miniature governed mission (real read + write + blocked network + fresh
          AuditLedger/BlackBox/Mission Receipt).
  replay  Validate the historical exported proof artifacts (does not execute a new mission).

Model integration is intentionally NOT included yet.
"""
from __future__ import annotations

import argparse
import sys

from .executor import run_mission
from .paths import REPO_ROOT


def _print_run_summary(outcome) -> None:
    line = "=" * 72
    print(line)
    print("Aurion bounded governed mission — FRESH RUN (offline, deterministic)")
    print(line)
    print(f"Goal:\n  {outcome.goal}")
    print(f"\nRun ID: {outcome.run_id}   Plan ID: {outcome.plan_id}   Status: {outcome.status}")

    print("\nAllowed steps:")
    allowed = [r for r in outcome.step_results if r.allowed]
    if allowed:
        for r in allowed:
            mark = "performed" if r.performed else "allowed (no-op)"
            print(f"  [+] step {r.index} {r.capability} {r.target}  -> {mark} ({r.reason_code})")
    else:
        print("  (none)")

    print("\nBlocked steps:")
    blocked = [r for r in outcome.step_results if not r.allowed]
    if blocked:
        for r in blocked:
            print(f"  [-] step {r.index} {r.capability} {r.target}  -> denied ({r.reason_code})")
    else:
        print("  (none)")

    print("\nGenerated artifacts:")
    for a in outcome.generated_artifacts:
        print(f"  - {a}")
    if not outcome.generated_artifacts:
        print("  (none)")

    print(f"\nAuditLedger path : {outcome.audit_path}   ({outcome.audit_event_count} events)")
    print(f"BlackBox path    : {outcome.blackbox_dir}   ({outcome.blackbox_record_count} decisions)")
    print(f"Mission Receipt  : {outcome.receipt_path}")
    print(line)
    print("This was a REAL bounded mission, freshly executed — not a replay. No network, no cloud,")
    print("no spend, no live autonomy. public_alpha_ready remains false.")
    print(line)


def cmd_run(_args) -> int:
    outcome = run_mission()
    _print_run_summary(outcome)
    return 0


def cmd_replay(_args) -> int:
    # Delegate to the existing self-contained replay runner, which validates the historical exported
    # proof artifacts. Imported lazily so `run` has zero dependency on it.
    import importlib.util

    runner = REPO_ROOT / "scripts" / "demo" / "run_public_spine_demo.py"
    if not runner.is_file():
        print("replay: historical proof runner not found (scripts/demo/run_public_spine_demo.py).")
        return 1
    spec = importlib.util.spec_from_file_location("run_public_spine_demo", runner)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return int(mod.validate())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aurion_demo",
        description="Bounded, offline, cross-platform Aurion governed-mission runtime (Demo Public Alpha).",
    )
    sub = parser.add_subparsers(dest="command")

    p_run = sub.add_parser("run", help="execute a fresh miniature governed mission")
    p_run.set_defaults(func=cmd_run)

    p_replay = sub.add_parser("replay", help="validate the historical exported proof artifacts")
    p_replay.set_defaults(func=cmd_replay)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        # Default to `run` so a bare `python -m aurion_demo` does something useful.
        return cmd_run(args)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
