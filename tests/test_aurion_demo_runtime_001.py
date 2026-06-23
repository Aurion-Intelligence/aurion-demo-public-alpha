"""
Deterministic tests for the bounded governed-mission runtime (aurion_demo).

Offline, no network, no private imports. Each run writes into a pytest tmp_path so tests never depend on
or pollute the repo's generated directory.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from aurion_demo import model, permissions  # noqa: E402
from aurion_demo.executor import run_mission  # noqa: E402
from aurion_demo.paths import GENERATED_DIR, SAMPLE_NOTE, WORKSPACE_DIR  # noqa: E402


# --- mission plan creation ---------------------------------------------------
def test_mission_plan_is_deterministic():
    p1 = model.build_plan()
    p2 = model.build_plan()
    assert p1.plan_id == p2.plan_id
    assert [s.capability for s in p1.microsteps] == ["fs.read", "net.request", "fs.write"]
    assert len(p1.microsteps) == 3


def test_plan_has_blocked_network_step():
    plan = model.build_plan()
    net = [s for s in plan.microsteps if s.capability == "net.request"]
    assert net and net[0].expects == "denied"


# --- permission contract -----------------------------------------------------
def test_permitted_bundled_file_read():
    d = permissions.evaluate("fs.read", "aurion_demo/workspace/project_note.md")
    assert d.allowed and d.reason_code == "READ_IN_WORKSPACE"


def test_denied_out_of_workspace_read():
    d = permissions.evaluate("fs.read", "README.md")
    assert not d.allowed and d.reason_code == "READ_OUTSIDE_WORKSPACE"
    d2 = permissions.evaluate("fs.read", "../../etc/passwd")
    assert not d2.allowed


def test_permitted_generated_artifact_write():
    d = permissions.evaluate("fs.write", "artifacts/demo/generated/x.md")
    assert d.allowed and d.reason_code == "WRITE_IN_GENERATED"


def test_denied_out_of_workspace_write():
    d = permissions.evaluate("fs.write", "README.md")
    assert not d.allowed and d.reason_code == "WRITE_OUTSIDE_GENERATED"
    d2 = permissions.evaluate("fs.write", "artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.json")
    assert not d2.allowed  # existing committed evidence is NOT writable


def test_denied_network_step():
    d = permissions.evaluate("net.request", "https://example.com/research")
    assert not d.allowed and d.reason_code == "NETWORK_NOT_PERMITTED"


def test_unknown_capability_denied_by_default():
    d = permissions.evaluate("process.spawn", "rm -rf /")
    assert not d.allowed and d.reason_code == "CAPABILITY_UNKNOWN"


# --- execution: evidence generation -----------------------------------------
def test_run_generates_audit_blackbox_receipt(tmp_path):
    out = run_mission(generated_dir=tmp_path)
    assert out.status == "completed"
    # AuditLedger present + non-empty
    audit = Path(out.abs_audit_path)
    assert audit.is_file()
    lines = [l for l in audit.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) == out.audit_event_count >= 5
    # BlackBox: one record per microstep (3)
    bb_dir = Path(out.abs_blackbox_dir)
    bb_files = list(bb_dir.glob("*.json"))
    assert len(bb_files) == out.blackbox_record_count == 3
    # Mission Receipt present
    receipt = Path(out.abs_receipt_path)
    assert receipt.is_file()


def test_receipt_evidence_reference_integrity(tmp_path):
    out = run_mission(generated_dir=tmp_path)
    receipt = json.loads(Path(out.abs_receipt_path).read_text(encoding="utf-8"))
    audit_text = Path(out.abs_audit_path).read_text(encoding="utf-8")
    # Every audit_event_id referenced in the receipt actually exists in the ledger.
    for aid in receipt["evidence"]["audit_event_ids"]:
        assert aid in audit_text, f"receipt references missing audit id {aid}"
    # Every blackbox trace id referenced exists as a file.
    bb_dir = Path(out.abs_blackbox_dir)
    for tid in receipt["evidence"]["blackbox_trace_ids"]:
        assert (bb_dir / f"{tid}.json").is_file(), f"missing blackbox file for {tid}"


def test_run_performs_real_read_and_write(tmp_path):
    out = run_mission(generated_dir=tmp_path)
    # Real write happened
    assert out.abs_generated_artifacts, "a generated artifact must be written"
    written = Path(out.abs_generated_artifacts[0])
    assert written.is_file()
    text = written.read_text(encoding="utf-8")
    # The three action items came from the bundled note (real read), deterministically.
    assert "PermissionGraph contract" in text
    assert "terminal summary" in text
    assert "CI matrix" in text


def test_run_blocks_network_and_does_not_perform_it(tmp_path):
    out = run_mission(generated_dir=tmp_path)
    blocked = [r for r in out.step_results if not r.allowed]
    assert any(r.capability == "net.request" and not r.performed for r in blocked)


# --- run identity + no fabrication ------------------------------------------
def test_repeated_runs_get_unique_run_ids(tmp_path):
    a = run_mission(generated_dir=tmp_path)
    b = run_mission(generated_dir=tmp_path)
    assert a.run_id != b.run_id
    assert a.abs_receipt_path != b.abs_receipt_path
    assert Path(a.abs_run_dir).name != Path(b.abs_run_dir).name


def test_no_fabricated_success(tmp_path):
    out = run_mission(generated_dir=tmp_path)
    receipt = json.loads(Path(out.abs_receipt_path).read_text(encoding="utf-8"))
    # The receipt must not claim public alpha readiness, and must record the blocked step honestly.
    assert receipt["public_alpha_ready_claimed"] is False
    assert receipt["is_replay_of_historical"] is False
    assert len(receipt["blocked_steps"]) >= 1
    # A blocked step must never be marked performed.
    for r in out.step_results:
        if not r.allowed:
            assert r.performed is False


def test_no_absolute_local_paths_in_artifacts(tmp_path):
    out = run_mission(generated_dir=tmp_path)
    # All artifacts produced for this run live under tmp_path; scan them for absolute/local leakage.
    bad_tokens = ["/home/", "/Users/", "C:\\Users", str(Path.home())]
    for p in tmp_path.rglob("*"):
        if p.is_file():
            content = p.read_text(encoding="utf-8", errors="ignore")
            for tok in bad_tokens:
                assert tok not in content, f"absolute/local path {tok!r} leaked into {p.name}"
    # Receipt paths are repo-relative POSIX (no backslashes, no drive letters, no leading slash).
    for key in ("audit_path", "blackbox_dir", "receipt_path"):
        val = getattr(out, key)
        assert not val.startswith("/") and ":" not in val and "\\" not in val


# --- workspace sanity --------------------------------------------------------
def test_sample_note_and_workspace_present():
    assert SAMPLE_NOTE.is_file()
    assert WORKSPACE_DIR.is_dir()
    assert GENERATED_DIR.name == "generated"
