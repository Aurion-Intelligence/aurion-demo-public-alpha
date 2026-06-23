#!/usr/bin/env python3
"""
Public Spine Demo runner — self-contained, offline, deterministic.

This is the public, self-contained entry point for Aurion's bounded **Demo Public Alpha** spine. It
works entirely from files included in this repository. It does **not**:

  - import any private/non-exported Aurion module,
  - use the network, invoke cloud models, or spend money,
  - modify any account, or
  - claim or perform live autonomous execution.

It has two modes:

  validate  (default)  Load the exported canonical Public Spine Demo Mission Receipt, verify its
                       structure and honest flags, and check which referenced AuditLedger / BlackBox
                       evidence files are actually present in this export. Evidence is **replayed /
                       fixture-backed** — it is the real evidence captured during the original bounded
                       run, shipped as fixtures. Nothing is fabricated; missing references are reported
                       honestly.

  generate             Produce a *new* bounded demo Mission Receipt deterministically from the exported
                       alpha-status data + demo scenario, written to --out. The generated receipt is
                       clearly labelled as newly generated and carries the same honest flags
                       (public_alpha_ready = false, dry run, no live autonomy). It references the
                       existing exported evidence as fixture-backed; it does not invent new evidence.

Usage:
  python scripts/demo/run_public_spine_demo.py                 # validate (default)
  python scripts/demo/run_public_spine_demo.py --mode validate
  python scripts/demo/run_public_spine_demo.py --mode generate --out artifacts/demo/generated_receipt.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Repo root = two levels up from scripts/demo/.
REPO_ROOT = Path(__file__).resolve().parents[2]

DEMO_JSON = REPO_ROOT / "artifacts" / "demo" / "PUBLIC_SPINE_DEMO_LOOP_001.json"
ALPHA_STATUS = REPO_ROOT / "artifacts" / "alpha" / "alpha_status.json"
AUDIT_LEDGER = REPO_ROOT / "artifacts" / "demo" / "PUBLIC_SPINE_DEMO_LOOP_001.audit.jsonl"
BLACKBOX_DIR = REPO_ROOT / "artifacts" / "demo" / "PUBLIC_SPINE_DEMO_LOOP_001.blackbox"

MISSION_ID = "demo-PUBLIC-SPINE-DEMO-LOOP-001"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _present_blackbox_files() -> list[str]:
    if not BLACKBOX_DIR.is_dir():
        return []
    return sorted(
        str(p.relative_to(REPO_ROOT))
        for p in BLACKBOX_DIR.rglob("*.json")
    )


def validate() -> int:
    """Validate / replay the exported canonical demo receipt. Returns process exit code."""
    print("=" * 72)
    print("Aurion Public Spine Demo — VALIDATE / REPLAY (offline, fixture-backed)")
    print("=" * 72)

    if not DEMO_JSON.is_file():
        print(f"FAIL: canonical demo receipt not found: {DEMO_JSON.relative_to(REPO_ROOT)}")
        return 1

    demo = _load_json(DEMO_JSON)
    problems: list[str] = []

    # --- core identity + honest flags ---
    if demo.get("mission_id") != MISSION_ID:
        problems.append(f"mission_id mismatch: {demo.get('mission_id')!r}")
    if demo.get("status") != "completed":
        problems.append(f"status is not 'completed': {demo.get('status')!r}")
    if demo.get("public_alpha_ready_claimed") not in (False, None):
        problems.append("public_alpha_ready_claimed must be false")

    # --- spine + permission structure (no fabrication; just presence checks) ---
    spine = demo.get("spine_walkthrough") or []
    perms = demo.get("permission_checks") or []
    if len(spine) < 1:
        problems.append("spine_walkthrough is empty")
    if len(perms) < 1:
        problems.append("permission_checks is empty")

    # --- evidence: which referenced AuditLedger / BlackBox files are actually in THIS export ---
    audit_present = AUDIT_LEDGER.is_file()
    bb_files = _present_blackbox_files()

    print(f"  mission_id .................. {demo.get('mission_id')}")
    print(f"  receipt_id .................. {demo.get('receipt_id')}")
    print(f"  status ...................... {demo.get('status')}")
    print(f"  public_alpha_ready_claimed .. {demo.get('public_alpha_ready_claimed')}")
    print(f"  spine steps ................. {len(spine)}")
    print(f"  permission checks ........... {len(perms)}")
    print(f"  AuditLedger (jsonl) ......... {'present' if audit_present else 'MISSING'}"
          f" ({AUDIT_LEDGER.relative_to(REPO_ROOT) if audit_present else 'n/a'})")
    print(f"  BlackBox trace files ........ {len(bb_files)} present (fixture-backed/replayed)")
    for f in bb_files:
        print(f"      - {f}")

    # --- honestly report referenced-but-absent evidence (do NOT fabricate it) ---
    produced = demo.get("artifacts_produced") or {}
    referenced_missing: list[str] = []
    for key, val in produced.items():
        candidates = []
        if isinstance(val, str):
            candidates = [val]
        elif isinstance(val, dict):
            candidates = [v for v in val.values() if isinstance(v, str)]
        for ref in candidates:
            if not (REPO_ROOT / ref).exists():
                referenced_missing.append(f"{key}: {ref}")
    if referenced_missing:
        print("  Referenced-but-not-in-export evidence (original run lived in the private repo;")
        print("  NOT fabricated here):")
        for r in referenced_missing:
            print(f"      - {r}")

    if not audit_present:
        problems.append("AuditLedger jsonl missing from export")
    if not bb_files:
        problems.append("no BlackBox trace files present in export")

    print("-" * 72)
    if problems:
        print("RESULT: VALIDATION FAILED")
        for p in problems:
            print(f"   - {p}")
        return 1
    print("RESULT: VALIDATED / REPLAYED the exported canonical demo receipt.")
    print("        Evidence is real, fixture-backed, and shipped with this repo. No live autonomy,")
    print("        no network, no spend. public_alpha_ready remains false.")
    return 0


def generate(out_path: Path) -> int:
    """Generate a new bounded demo receipt deterministically from exported data."""
    print("=" * 72)
    print("Aurion Public Spine Demo — GENERATE (offline, deterministic)")
    print("=" * 72)

    if not DEMO_JSON.is_file():
        print(f"FAIL: canonical demo source not found: {DEMO_JSON.relative_to(REPO_ROOT)}")
        return 1

    demo = _load_json(DEMO_JSON)
    status = _load_json(ALPHA_STATUS) if ALPHA_STATUS.is_file() else {}

    bb_files = _present_blackbox_files()
    receipt = {
        "generated_by": "scripts/demo/run_public_spine_demo.py",
        "generated_mode": "newly_generated_bounded_demo_receipt",
        "is_replay_of_canonical": False,
        "mission_id": MISSION_ID,
        "title": "Aurion Public Spine Demo (bounded, offline, deterministic)",
        "status": "completed",
        "receipt_classification": "dry_run",
        "public_alpha_ready_claimed": False,
        "demo_public_alpha_ready": bool(status.get("demo_public_alpha_ready", True)),
        "public_alpha_ready": bool(status.get("public_alpha_ready", False)),
        "user_goal": demo.get("user_goal"),
        "spine_walkthrough": demo.get("spine_walkthrough"),
        "permission_checks": demo.get("permission_checks"),
        "loop_plan_summary": demo.get("loop_plan_summary"),
        "evidence_note": (
            "AuditLedger and BlackBox evidence are REPLAYED / FIXTURE-BACKED references to the exported "
            "demo evidence; this generated receipt does not fabricate new evidence."
        ),
        "evidence_fixture_refs": {
            "audit_ledger": str(AUDIT_LEDGER.relative_to(REPO_ROOT)) if AUDIT_LEDGER.is_file() else None,
            "blackbox_traces": bb_files,
        },
        "boundaries": [
            "no network", "no cloud models", "no spend", "no account changes",
            "no live autonomy", "dry run only",
        ],
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    print(f"  GENERATED a new bounded demo receipt: {out_path}")
    print(f"  mission_id .................. {receipt['mission_id']}")
    print(f"  classification .............. {receipt['receipt_classification']}")
    print(f"  public_alpha_ready .......... {receipt['public_alpha_ready']}")
    print(f"  evidence .................... replayed/fixture-backed ({len(bb_files)} blackbox files)")
    print("-" * 72)
    print("RESULT: GENERATED a new bounded demo receipt (offline, deterministic). Evidence is")
    print("        fixture-backed/replayed, not fabricated. public_alpha_ready remains false.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Aurion Public Spine Demo runner (offline, self-contained)")
    parser.add_argument("--mode", choices=["validate", "generate"], default="validate",
                        help="validate/replay the exported canonical receipt (default), or generate a new bounded one")
    parser.add_argument("--out", default="artifacts/demo/generated_public_spine_demo_receipt.json",
                        help="output path for --mode generate (relative to repo root)")
    args = parser.parse_args(argv)

    if args.mode == "validate":
        return validate()
    out = Path(args.out)
    if not out.is_absolute():
        out = REPO_ROOT / out
    return generate(out)


if __name__ == "__main__":
    sys.exit(main())
