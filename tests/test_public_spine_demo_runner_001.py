"""
Standalone test for the public, self-contained Public Spine Demo runner.

Exercises ONLY exported code (`scripts/demo/run_public_spine_demo.py` + exported artifacts). It does not
import any private/non-exported Aurion module, hit the network, or touch cloud/spend. Offline and
deterministic — safe to run in the public repo.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER = REPO_ROOT / "scripts" / "demo" / "run_public_spine_demo.py"
DEMO_JSON = REPO_ROOT / "artifacts" / "demo" / "PUBLIC_SPINE_DEMO_LOOP_001.json"


def _load_runner():
    spec = importlib.util.spec_from_file_location("run_public_spine_demo", RUNNER)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def test_runner_file_exists():
    assert RUNNER.is_file(), "public demo runner must ship in the export"


def test_runner_has_no_private_or_network_imports():
    text = RUNNER.read_text(encoding="utf-8")
    forbidden = [
        "aurion.mission", "aurion.brain", "aurion.core", "aurion.router", "aurion.mods",
        "aurion.tools", "aurion.mission_loop", "scripts.demo.public_spine_demo_loop_001",
        "import requests", "import urllib", "import http.client", "import socket",
        "openai", "anthropic", "ollama",
    ]
    for f in forbidden:
        assert f not in text, f"runner must not reference {f!r}"


def test_validate_mode_succeeds():
    mod = _load_runner()
    assert mod.validate() == 0


def test_generate_mode_writes_bounded_receipt(tmp_path):
    mod = _load_runner()
    out = tmp_path / "gen.json"
    rc = mod.generate(out)
    assert rc == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    # Honest, bounded receipt
    assert data["is_replay_of_canonical"] is False
    assert data["generated_mode"] == "newly_generated_bounded_demo_receipt"
    assert data["public_alpha_ready"] is False
    assert data["public_alpha_ready_claimed"] is False
    assert data["receipt_classification"] == "dry_run"
    assert "no live autonomy" in [b.lower() for b in data["boundaries"]] or \
        any("no live autonomy" in b.lower() for b in data["boundaries"])


def test_canonical_demo_receipt_is_honest():
    demo = json.loads(DEMO_JSON.read_text(encoding="utf-8"))
    assert demo["mission_id"] == "demo-PUBLIC-SPINE-DEMO-LOOP-001"
    assert demo["status"] == "completed"
    assert demo.get("public_alpha_ready_claimed") in (False, None)
    assert len(demo.get("spine_walkthrough") or []) >= 1
    assert len(demo.get("permission_checks") or []) >= 1


def test_exported_evidence_files_present():
    # The runner relies on these exported, fixture-backed evidence files.
    audit = REPO_ROOT / "artifacts" / "demo" / "PUBLIC_SPINE_DEMO_LOOP_001.audit.jsonl"
    bb_dir = REPO_ROOT / "artifacts" / "demo" / "PUBLIC_SPINE_DEMO_LOOP_001.blackbox"
    assert audit.is_file(), "AuditLedger fixture must be present"
    bb = list(bb_dir.rglob("*.json"))
    assert len(bb) >= 1, "at least one BlackBox trace fixture must be present"


def test_runner_main_validate_returns_zero():
    mod = _load_runner()
    assert mod.main(["--mode", "validate"]) == 0
