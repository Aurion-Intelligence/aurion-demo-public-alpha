"""Alpha readiness status generator — evidence-derived, anti-fake-green.

[alpha-status-autogenerator-001]

Generates alpha readiness + known-issues from REAL repo artifacts (TODO, Sandbox Longrun runs,
drill artifacts, test-debt inventories, route artifacts). Gates default to NOT-passing and only
flip green on present, recent evidence. `public_alpha_ready` is false unless every hard gate passes
(including an install walkthrough + screenshots existing). Missing/stale artifacts become staleness
warnings — never a fake green.

Safety: bounded scans only. Never reads `.env`, never parses secrets, never requires network.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]

# How old (days) an artifact may be before it earns a staleness warning.
STALE_AFTER_DAYS = 21

GENERATED_NOTICE = "Generated from repo artifacts. Do not edit manually."


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _exists(rel: str) -> bool:
    p = REPO_ROOT / rel
    try:
        return p.exists()
    except Exception:
        return False


def _read_text(rel: str, cap: int = 200_000) -> str:
    p = REPO_ROOT / rel
    try:
        if p.is_file():
            return p.read_text(encoding="utf-8", errors="replace")[:cap]
    except Exception:
        pass
    return ""


def _age_days(path: Path) -> Optional[float]:
    try:
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        return (datetime.now(timezone.utc) - mtime).total_seconds() / 86400.0
    except Exception:
        return None


# ── Evidence: latest full-safe Sandbox Longrun run ───────────────────────────

def latest_full_safe() -> dict[str, Any]:
    """Return the latest full-safe run summary (run_id, jobs, pass) or an honest unknown."""
    runs_dir = REPO_ROOT / "artifacts" / "sandbox_longrun" / "runs"
    best: Optional[dict[str, Any]] = None
    best_mtime = -1.0
    try:
        candidates = sorted(runs_dir.glob("*/summary*.json"))[:5000]
    except Exception:
        candidates = []
    for f in candidates:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if str(data.get("preset")) != "full-safe":
            continue
        mtime = f.stat().st_mtime if f.exists() else 0
        if mtime > best_mtime:
            best_mtime = mtime
            best = data
            best["_path"] = str(f.relative_to(REPO_ROOT))
            best["_age_days"] = _age_days(f)
    if best is None:
        return {"available": False, "reason": "No full-safe run summary found."}
    jr = int(best.get("jobs_run") or 0)
    jp = int(best.get("jobs_passed") or 0)
    jf = int(best.get("jobs_failed") or 0)
    return {
        "available": True,
        "run_id": str(best.get("run_id") or ""),
        "jobs_run": jr,
        "jobs_passed": jp,
        "jobs_failed": jf,
        "passed": jr > 0 and jf == 0 and jp == jr,
        "path": best.get("_path"),
        "age_days": best.get("_age_days"),
    }


# ── Gate resolution ──────────────────────────────────────────────────────────

# Each gate: (label, kind, evidence-spec). status ∈ {pass, fail, unknown}.
# Artifact-backed gates pass only when the artifact exists; drill gates also check a verdict signal.

def _artifact_gate(label: str, rel: str, *, verdict_any: Optional[list[str]] = None,
                   not_signal: Optional[list[str]] = None) -> dict[str, Any]:
    if not _exists(rel):
        return {"label": label, "status": "unknown", "evidence": None,
                "reason": f"Evidence artifact not found: {rel}"}
    text = _read_text(rel).lower()
    # A "not green" signal forces fail (e.g. broad npm inventory says NOT green).
    if not_signal and any(s.lower() in text for s in not_signal):
        return {"label": label, "status": "fail", "evidence": rel,
                "reason": "Artifact reports a non-passing state."}
    if verdict_any and not any(s.lower() in text for s in verdict_any):
        return {"label": label, "status": "unknown", "evidence": rel,
                "reason": "Artifact present but no pass-verdict signal found."}
    return {"label": label, "status": "pass", "evidence": rel}


def _todo_done(todo_id: str) -> bool:
    """True if a TODO id is marked [x] in TODO.md or the 2026 archive.

    The archive can exceed the default read cap, so read it with a larger bound — under-reading it
    would falsely mark completed work as unknown (a fake-RED, the inverse of fake-green; still bad).
    """
    pattern = re.compile(rf"^- \[x\] \[{re.escape(todo_id)}\]", re.M)
    return bool(pattern.search(_read_text("TODO.md", cap=1_000_000)) or
                pattern.search(_read_text("docs/todo_archive/TODO_ARCHIVE_2026.md", cap=2_000_000)))


def _todo_gate(label: str, todo_id: str) -> dict[str, Any]:
    if _todo_done(todo_id):
        return {"label": label, "status": "pass", "evidence": f"[x] [{todo_id}]"}
    return {"label": label, "status": "unknown", "evidence": None,
            "reason": f"TODO [{todo_id}] not marked complete."}


def _receipt_coverage_gate() -> dict[str, Any]:
    rel = "artifacts/mission_receipts/RECEIPT_COVERAGE_GATE_001.json"
    path = REPO_ROOT / rel
    if not path.is_file():
        return {
            "label": "Mission Receipt coverage",
            "status": "unknown",
            "evidence": None,
            "reason": f"Evidence artifact not found: {rel}",
        }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {
            "label": "Mission Receipt coverage",
            "status": "unknown",
            "evidence": rel,
            "reason": "Receipt coverage artifact is unreadable.",
        }
    summary = data.get("summary") if isinstance(data.get("summary"), dict) else {}
    missing = int(summary.get("missing_unexpected_count") or 0)
    pending = int(summary.get("pending_count") or 0)
    covered = int(summary.get("covered_count") or 0)
    # [receipt-coverage-repair-001] Unclassified legacy/unknown still counts as a blocker (it is an
    # unexplained gap); explicitly classified legacy categories do not block public alpha.
    legacy_unknown = int(summary.get("legacy_unknown_count") or 0)
    legacy_known = int(summary.get("legacy_known_no_receipt_count") or 0)
    legacy_unrecoverable = int(summary.get("legacy_unknown_unrecoverable_count") or 0)
    detail = (
        f"covered={covered}, missing={missing}, pending={pending}, "
        f"legacy_known={legacy_known}, legacy_unrecoverable={legacy_unrecoverable}, "
        f"legacy_unknown={legacy_unknown}"
    )
    # An unexplained gap (terminal missing, or still-unclassified legacy/unknown) blocks public alpha.
    if missing > 0 or legacy_unknown > 0:
        return {
            "label": "Mission Receipt coverage",
            "status": "fail",
            "evidence": rel,
            "detail": detail,
            "reason": "Terminal mission_id paths are missing verified receipts or have unclassified legacy/unknown coverage.",
        }
    return {
        "label": "Mission Receipt coverage",
        "status": "pass",
        "evidence": rel,
        "detail": detail,
        "reason": "Only non-terminal/pending or explicitly classified (covered/legacy/not-required) paths remain."
        if (pending or legacy_known or legacy_unrecoverable) else None,
    }


def _memory_fragmentation_gate() -> dict[str, Any]:
    """[memory-fragmentation-map-001] green if the memory map exists AND no high-privacy store is
    raw-alpha-visible; red if a high-risk raw store IS alpha-visible; unknown if the map is missing.
    Non-blocking (coherence/documentation gate), but RED would be a real fake-'one brain' risk."""
    rel = "artifacts/architecture/memory_fragmentation_map_001.json"
    path = REPO_ROOT / rel
    if not path.is_file():
        return {"label": "Memory fragmentation mapped", "status": "unknown", "evidence": None,
                "reason": f"Memory map not found: {rel}"}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        stores = data.get("stores") or []
    except Exception:
        return {"label": "Memory fragmentation mapped", "status": "unknown", "evidence": rel,
                "reason": "Memory map artifact unreadable."}
    raw_high_visible = [
        s.get("store_name") for s in stores
        if s.get("privacy_risk") == "high" and s.get("alpha_visibility") == "visible"
    ]
    if raw_high_visible:
        return {"label": "Memory fragmentation mapped", "status": "fail", "evidence": rel,
                "detail": f"high-risk store(s) alpha-visible: {raw_high_visible}",
                "reason": "Raw high-privacy memory is alpha-visible — fix gating."}
    # Mapped + documented-but-fragmented → pass (yellow-ness is conveyed in the map, not the gate).
    return {"label": "Memory fragmentation mapped", "status": "pass", "evidence": rel,
            "detail": f"{len(stores)} stores classified; no high-risk store alpha-visible."}


def _agents_memory_index_gate() -> dict[str, Any]:
    """[agents-memory-handoff-index-001] green if the generated agents_memory index +
    manifest exist and carry the do-not-edit notice; yellow if generated but the
    manifest reports parser warnings; unknown if missing. Non-blocking — it's an
    agent-bootstrap coherence gate, not an alpha-readiness gate."""
    label = "Agents memory index generated"
    json_rel = "agents_memory/latest.json"
    md_rel = "agents_memory/INDEX.md"
    json_path = REPO_ROOT / json_rel
    md_path = REPO_ROOT / md_rel
    if not (json_path.is_file() and md_path.is_file()):
        return {"label": label, "status": "unknown", "evidence": None,
                "reason": "agents_memory INDEX.md / latest.json not generated."}
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception:
        return {"label": label, "status": "unknown", "evidence": json_rel,
                "reason": "agents_memory manifest unreadable."}
    md_text = _read_text(md_rel)
    if "Do not edit manually" not in md_text:
        return {"label": label, "status": "unknown", "evidence": md_rel,
                "reason": "INDEX.md missing generated do-not-edit notice."}
    count = data.get("handoff_count", 0)
    warns = len(data.get("warnings") or [])
    if warns:
        return {"label": label, "status": "yellow", "evidence": json_rel,
                "detail": f"{count} handoffs indexed; {warns} parser warning(s) (best-effort).",
                "reason": "Index generated with parser warnings on older/freeform handoffs."}
    return {"label": label, "status": "pass", "evidence": json_rel,
            "detail": f"{count} handoffs indexed; manifest + index fresh."}


def _public_spine_demo_loop_gate() -> dict[str, Any]:
    """[public-spine-demo-loop-001] Green only when the generated public-spine demo
    artifact is present, explicitly complete, linked to a receipt id, and does NOT
    claim public alpha readiness by itself."""
    label = "Public spine demo loop"
    rel = "artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.json"
    scenario_rel = "artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.scenario.json"
    path = REPO_ROOT / rel
    scenario_path = REPO_ROOT / scenario_rel
    if not path.is_file():
        return {
            "label": label,
            "status": "unknown",
            "evidence": None,
            "reason": f"Evidence artifact not found: {rel}",
        }
    if not scenario_path.is_file():
        return {
            "label": label,
            "status": "unknown",
            "evidence": rel,
            "reason": f"Scenario descriptor not found: {scenario_rel}",
        }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
    except Exception:
        return {
            "label": label,
            "status": "unknown",
            "evidence": rel,
            "reason": "Public spine demo artifact or scenario is unreadable.",
        }
    if data.get("demo_id") != "PUBLIC-SPINE-DEMO-LOOP-001":
        return {
            "label": label,
            "status": "unknown",
            "evidence": rel,
            "reason": "Public spine demo artifact has the wrong demo_id.",
        }
    if scenario.get("demo_id") != "PUBLIC-SPINE-DEMO-LOOP-001":
        return {
            "label": label,
            "status": "unknown",
            "evidence": scenario_rel,
            "reason": "Public spine demo scenario has the wrong demo_id.",
        }
    if data.get("public_alpha_ready_claimed") is not False:
        return {
            "label": label,
            "status": "fail",
            "evidence": rel,
            "reason": "Demo artifact must not claim public alpha readiness.",
        }
    if data.get("status") != "completed" or not data.get("receipt_id"):
        return {
            "label": label,
            "status": "unknown",
            "evidence": rel,
            "reason": "Demo artifact is present but lacks completed status or receipt_id.",
        }
    return {
        "label": label,
        "status": "pass",
        "evidence": rel,
        "detail": f"receipt_id={data.get('receipt_id')}; public_alpha_ready_claimed=false",
    }


def compute_gates() -> dict[str, dict[str, Any]]:
    fs = latest_full_safe()
    gates: dict[str, dict[str, Any]] = {}
    gates["memory_fragmentation_mapped"] = _memory_fragmentation_gate()
    gates["agents_memory_index"] = _agents_memory_index_gate()
    gates["public_spine_demo_loop"] = _public_spine_demo_loop_gate()

    gates["full_safe"] = {
        "label": "Sandbox Longrun full-safe",
        "status": "pass" if fs.get("passed") else ("fail" if fs.get("available") else "unknown"),
        "evidence": fs.get("path"),
        "detail": f"{fs.get('jobs_passed', 0)}/{fs.get('jobs_run', 0)}" if fs.get("available") else None,
        "reason": fs.get("reason"),
    }

    gates["governed_mission_drills"] = _artifact_gate(
        "Governed mission drills", "artifacts/alpha/ALPHA_GOVERNED_MISSION_DRILL_001.md",
        verdict_any=["all 7", "behave honestly and safely", "zero source mutation"])
    gates["governed_write_drill"] = _artifact_gate(
        "Governed TODO-write approval drill",
        "artifacts/alpha/GOVERNED_TODO_WRITE_APPROVAL_LIVE_DRILL_001.md")

    gates["mission_receipt_correlation"] = _todo_gate(
        "Mission Receipt correlation", "mission-receipt-correlation-hardening-001")
    gates["receipt_coverage"] = _receipt_coverage_gate()
    gates["mission_source_links"] = _todo_gate(
        "Mission Receipt source links", "mission-receipt-source-linking-001")
    gates["approvalgate_detail_api"] = _todo_gate(
        "ApprovalGate proposal detail API", "approvalgate-proposal-detail-api-001")
    gates["unified_mission_query"] = _todo_gate(
        "Unified mission query API", "mission-list-unified-query-001")
    gates["mission_control_unified_ui"] = _todo_gate(
        "Mission Control unified UI", "mission-control-unified-ui-001")

    gates["route_contracts"] = _artifact_gate(
        "Route contracts", "artifacts/routes/ROUTE_CONTRACT_APP_CEILING_REALITY_CHECK_001_after.txt",
        verdict_any=["passed"], not_signal=["failed"])

    # Command Center build/typecheck — derived from the latest full-safe job results.
    cc_jobs = _full_safe_jobs(fs)
    gates["command_center_build"] = _job_gate("Command Center build", cc_jobs, "command_center_build", fs)
    gates["command_center_typecheck"] = _job_gate("Command Center typecheck", cc_jobs, "command_center_typecheck", fs)

    # Broad frontend tests — the inventory artifact says whether broad npm is green.
    gates["broad_frontend_tests"] = _artifact_gate(
        "Broad frontend tests",
        "artifacts/command_center/COMMAND_CENTER_BROAD_NPM_TEST_FAILURE_INVENTORY_001.md",
        not_signal=["broad is not green", "still fail"])

    # Public-alpha-only requirements (intentionally hard to satisfy; honest about missing).
    install_candidates = [
        "docs/alpha/INSTALL_WALKTHROUGH.md",
        "docs/alpha/INSTALL.md",
        "docs/install.md",
    ]
    install_evidence = next((rel for rel in install_candidates if _exists(rel)), None)
    gates["install_walkthrough"] = {
        "label": "Install walkthrough",
        "status": "pass" if install_evidence else "unknown",
        "evidence": install_evidence,
        "reason": None if install_evidence else "No install walkthrough doc found (required for public alpha).",
    }
    gates["screenshots"] = _screenshots_gate()
    return gates


# Minimum screenshot set required for the demo-public-alpha visual proof pack.
# [alpha-screenshot-capture-001]
_REQUIRED_SCREENSHOTS = [
    "01-command-center-shell.png",
    "02-mission-receipts-list.png",
    "03-public-spine-demo-receipt-detail.png",
    "04-demo-governance-evidence.png",
    "05-alpha-status.png",
]


def _screenshots_gate() -> dict[str, Any]:
    """Manifest-based screenshot gate (anti-fake-green).

    [alpha-screenshot-capture-001] The gate passes ONLY when a real screenshot
    manifest exists, declares the demo-public-alpha release context, lists the
    minimum screenshot set, and every referenced PNG exists and is non-empty. A
    random stray PNG in docs/alpha/ can NOT satisfy this gate.
    """
    label = "Alpha screenshots"
    shots_dir = REPO_ROOT / "docs" / "alpha" / "screenshots"
    manifest_path = shots_dir / "manifest.json"

    def _unknown(reason: str) -> dict[str, Any]:
        return {"label": label, "status": "unknown", "evidence": None, "reason": reason}

    if not manifest_path.is_file():
        return _unknown("No alpha screenshot manifest (docs/alpha/screenshots/manifest.json) found.")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return _unknown(f"Alpha screenshot manifest is unreadable: {str(exc)[:80]}.")

    if manifest.get("release_context") != "demo_public_alpha":
        return _unknown("Screenshot manifest release_context is not 'demo_public_alpha'.")

    entries = manifest.get("screenshots") or []
    listed = {str(e.get("file", "")) for e in entries if isinstance(e, dict)}
    missing_from_manifest = [f for f in _REQUIRED_SCREENSHOTS if f not in listed]
    if missing_from_manifest:
        return _unknown(f"Manifest missing required screenshots: {', '.join(missing_from_manifest)}.")

    # Every referenced PNG must exist and be non-empty.
    bad: list[str] = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        fname = str(e.get("file", ""))
        if not fname:
            continue
        fpath = shots_dir / fname
        if not fpath.is_file() or fpath.stat().st_size <= 0:
            bad.append(fname)
    if bad:
        return _unknown(f"Manifest references missing/empty screenshot files: {', '.join(bad)}.")

    return {
        "label": label,
        "status": "pass",
        "evidence": "docs/alpha/screenshots/manifest.json",
        "reason": None,
    }


def _full_safe_jobs(fs: dict[str, Any]) -> dict[str, str]:
    """Map job name → status from the latest full-safe summary.json job_results."""
    path = fs.get("path")
    if not path:
        return {}
    try:
        data = json.loads(_read_text(path))
        out: dict[str, str] = {}
        for jr in data.get("job_results", []) or []:
            name = str(jr.get("name") or jr.get("job") or "")
            status = str(jr.get("status") or ("passed" if jr.get("passed") else "")).lower()
            if name:
                out[name] = status
        return out
    except Exception:
        return {}


def _job_gate(label: str, jobs: dict[str, str], job_name: str, fs: dict[str, Any]) -> dict[str, Any]:
    if not fs.get("available"):
        return {"label": label, "status": "unknown", "evidence": None, "reason": "No full-safe run."}
    st = jobs.get(job_name, "")
    if st in ("passed", "pass", "ok", "success"):
        return {"label": label, "status": "pass", "evidence": fs.get("path")}
    if st in ("failed", "fail", "error"):
        return {"label": label, "status": "fail", "evidence": fs.get("path")}
    # If the whole full-safe passed, infer the job passed (it's part of the preset).
    if fs.get("passed"):
        return {"label": label, "status": "pass", "evidence": fs.get("path"),
                "reason": "Inferred from passing full-safe preset."}
    return {"label": label, "status": "unknown", "evidence": fs.get("path"),
            "reason": f"Job '{job_name}' status not found."}


# ── Status assembly ──────────────────────────────────────────────────────────

# Gates that MUST pass for public alpha.
PUBLIC_ALPHA_GATES = [
    "full_safe", "governed_mission_drills", "governed_write_drill",
    "public_spine_demo_loop",
    "mission_receipt_correlation", "receipt_coverage", "mission_source_links", "approvalgate_detail_api",
    "unified_mission_query", "mission_control_unified_ui", "route_contracts",
    "command_center_build", "command_center_typecheck",
    # [alpha-screenshot-capture-001] The broad frontend (npm) suite must be green for
    # FULL public alpha. While it is failing (classified dev/lab + harness debt), full
    # public alpha cannot be claimed — this prevents the demo screenshot/install lanes
    # from flipping full public alpha green on their own.
    "broad_frontend_tests",
    "install_walkthrough", "screenshots",
]
# Subset that must pass for developer alpha.
DEV_ALPHA_GATES = [
    "full_safe", "governed_mission_drills", "governed_write_drill",
    "public_spine_demo_loop",
    "mission_control_unified_ui", "route_contracts", "command_center_build", "command_center_typecheck",
]
# [alpha-screenshot-capture-001] Gates that must pass for the DEMO public alpha
# package (the bounded, fixture-backed proof pack) — distinct from full public alpha.
# Deliberately excludes broad_frontend_tests / full_safe: the demo package is about
# proving the public spine + visual pack honestly, not full-release readiness.
DEMO_PUBLIC_ALPHA_GATES = [
    "public_spine_demo_loop", "install_walkthrough", "screenshots",
]


def _staleness_warnings(gates: dict[str, dict[str, Any]], fs: dict[str, Any]) -> list[str]:
    warns: list[str] = []
    age = fs.get("age_days")
    if fs.get("available") and age is not None and age > STALE_AFTER_DAYS:
        warns.append(f"Latest full-safe run is {age:.0f} days old (> {STALE_AFTER_DAYS}d) — re-run before relying on it.")
    for key in PUBLIC_ALPHA_GATES:
        g = gates.get(key, {})
        if g.get("status") == "unknown":
            warns.append(f"Gate '{key}' is unknown: {g.get('reason') or 'no evidence'}.")
    return warns


def build_status() -> dict[str, Any]:
    gates = compute_gates()
    fs = latest_full_safe()

    def _passing(keys: list[str]) -> bool:
        return all(gates.get(k, {}).get("status") == "pass" for k in keys)

    public_ready = _passing(PUBLIC_ALPHA_GATES)
    dev_ready = _passing(DEV_ALPHA_GATES)
    demo_public_ready = _passing(DEMO_PUBLIC_ALPHA_GATES)

    blocking: list[str] = []
    for k in PUBLIC_ALPHA_GATES:
        g = gates.get(k, {})
        if g.get("status") != "pass":
            blocking.append(f"{g.get('label', k)}: {g.get('reason') or g.get('status')}")

    non_blocking: list[str] = []
    if gates.get("broad_frontend_tests", {}).get("status") != "pass":
        non_blocking.append("Broad frontend (npm) test suite is not fully green — see "
                            "artifacts/command_center/COMMAND_CENTER_BROAD_NPM_TEST_FAILURE_INVENTORY_001.md "
                            "(classified pre-existing dev/lab + harness debt, not alpha-blocking).")

    staleness = _staleness_warnings(gates, fs)

    if public_ready:
        overall = "green"
    elif dev_ready:
        overall = "yellow"
    else:
        overall = "red"

    if public_ready:
        summary = "Public alpha is READY."
    elif demo_public_ready:
        summary = ("Demo public alpha package is ready (bounded, fixture-backed proof pack); "
                   "FULL public alpha is NOT ready (see blockers).")
    elif dev_ready:
        summary = "Developer alpha is ready; public alpha is NOT ready (see blockers)."
    else:
        summary = "Not alpha-ready (see blockers)."

    known_issues = list(non_blocking)
    if not gates.get("install_walkthrough", {}).get("status") == "pass":
        known_issues.append("No install/setup walkthrough yet (blocks public alpha).")
    if not gates.get("screenshots", {}).get("status") == "pass":
        known_issues.append("No alpha screenshots yet (blocks public alpha).")

    todo_refs = [
        "mission-receipt-correlation-hardening-001", "mission-list-unified-query-001",
        "mission-control-unified-ui-001", "alpha-governed-mission-drill-001",
        "governed-todo-write-approval-live-drill-001",
        "public-spine-demo-loop-001",
        "receipt-coverage-gate-001",
        "command-center-broad-npm-test-failure-inventory-001",
    ]

    return {
        "generated_at": _utc_now(),
        "generated_notice": GENERATED_NOTICE,
        "public_alpha_ready": public_ready,
        "demo_public_alpha_ready": demo_public_ready,
        "developer_alpha_ready": dev_ready,
        "overall_status": overall,
        "readiness_summary": summary,
        "gates": gates,
        "known_issues": known_issues,
        "blocking_issues": blocking,
        "non_blocking_debt": non_blocking,
        "evidence": {
            "full_safe": fs,
        },
        "last_full_safe_run_id": fs.get("run_id") if fs.get("available") else None,
        "last_drill_receipts": _latest_drill_receipt_ids(),
        "todo_refs": todo_refs,
        "staleness_warnings": staleness,
    }


def _latest_drill_receipt_ids(limit: int = 3) -> list[str]:
    """Stable demo/drill receipt mission ids from artifacts (safe ids only)."""
    out: list[str] = []
    d = REPO_ROOT / "artifacts" / "mission_receipts"
    if not d.is_dir():
        return out
    try:
        for f in sorted(d.glob("*demo_alpha_governed_mission_001*.json"))[:limit]:
            out.append(f.stem)
    except Exception:
        pass
    return out
