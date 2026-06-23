"""
Tests for the Alpha Screenshot Capture demo-public-alpha proof pack —
[alpha-screenshot-capture-001]

Validates (offline, deterministic — no backend, no model, no network):
  1.  screenshot directory exists
  2.  minimum screenshot files exist
  3.  screenshot files are non-empty
  4.  screenshot manifest exists
  5.  manifest includes captions
  6.  manifest marks screenshots as demo-public-alpha, not production
  7.  docs reference screenshots
  8.  generated alpha status recognizes the screenshot gate (status == pass)
  9.  screenshots do not use forbidden placeholder names (fake/mock/todo/placeholder)
  10. no obvious secret-looking strings appear in screenshot metadata or manifest
  +   this lane alone does NOT flip FULL public alpha green (brief check #14)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SHOTS_DIR = REPO_ROOT / "docs" / "alpha" / "screenshots"
MANIFEST = SHOTS_DIR / "manifest.json"
README_ALPHA = REPO_ROOT / "docs" / "alpha" / "README_ALPHA.md"

REQUIRED_SCREENSHOTS = [
    "01-command-center-shell.png",
    "02-mission-receipts-list.png",
    "03-public-spine-demo-receipt-detail.png",
    "04-demo-governance-evidence.png",
    "05-alpha-status.png",
]

FORBIDDEN_NAME_TOKENS = ["fake", "mock", "todo", "placeholder"]

# Secret-looking patterns that must NOT appear in the manifest/metadata.
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{8,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]+", re.IGNORECASE),
    re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]


@pytest.fixture(scope="module")
def manifest() -> dict:
    assert MANIFEST.is_file(), "Screenshot manifest is missing."
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


# 1
def test_screenshot_directory_exists():
    assert SHOTS_DIR.is_dir(), "docs/alpha/screenshots/ directory must exist."


# 2 + 3
@pytest.mark.parametrize("name", REQUIRED_SCREENSHOTS)
def test_required_screenshot_exists_and_non_empty(name: str):
    p = SHOTS_DIR / name
    assert p.is_file(), f"Required screenshot missing: {name}"
    assert p.stat().st_size > 0, f"Screenshot is empty: {name}"


# 4
def test_manifest_exists(manifest: dict):
    assert manifest.get("screenshot_set") == "ALPHA-SCREENSHOT-CAPTURE-001"


# 5
def test_manifest_entries_have_captions(manifest: dict):
    entries = manifest.get("screenshots") or []
    assert entries, "Manifest must list screenshots."
    for e in entries:
        assert str(e.get("caption", "")).strip(), f"Missing caption for {e.get('file')}"
        assert str(e.get("title", "")).strip(), f"Missing title for {e.get('file')}"


def test_manifest_lists_required_set(manifest: dict):
    listed = {str(e.get("file", "")) for e in (manifest.get("screenshots") or [])}
    missing = [f for f in REQUIRED_SCREENSHOTS if f not in listed]
    assert not missing, f"Manifest missing required screenshots: {missing}"


# 6
def test_manifest_marks_demo_public_alpha_not_production(manifest: dict):
    assert manifest.get("release_context") == "demo_public_alpha"
    not_a_claim = [str(x).lower() for x in (manifest.get("not_a_claim") or [])]
    for forbidden in ["production ready", "full public alpha"]:
        assert forbidden in not_a_claim, f"Manifest must disclaim '{forbidden}'."


# 7
def test_docs_reference_screenshots():
    assert README_ALPHA.is_file(), "docs/alpha/README_ALPHA.md must exist."
    text = README_ALPHA.read_text(encoding="utf-8")
    assert "screenshots/" in text, "README_ALPHA.md must reference the screenshots directory."


# 8 + #14: generated alpha status recognizes the screenshot gate AND this lane
# does not flip FULL public alpha green on its own.
def test_alpha_status_recognizes_screenshot_gate_without_full_public_green():
    from aurion.alpha.status import build_status

    status = build_status()
    assert status["gates"]["screenshots"]["status"] == "pass", \
        "Screenshots gate must pass once the manifest + PNGs are present."
    # The demo package is ready...
    assert status.get("demo_public_alpha_ready") is True, \
        "Demo public alpha package should be ready when its gates pass."
    # ...but FULL public alpha must NOT be claimed while broad frontend tests fail.
    if status["gates"].get("broad_frontend_tests", {}).get("status") != "pass":
        assert status["public_alpha_ready"] is False, \
            "Screenshots alone must not flip FULL public alpha green."


# 9
def test_no_forbidden_placeholder_names(manifest: dict):
    for p in SHOTS_DIR.glob("*.png"):
        low = p.name.lower()
        for token in FORBIDDEN_NAME_TOKENS:
            assert token not in low, f"Forbidden token '{token}' in screenshot name: {p.name}"
    blob = json.dumps(manifest).lower()
    # Allow the literal disclaimers; only the explicit placeholder tokens are forbidden.
    for token in FORBIDDEN_NAME_TOKENS:
        assert token not in {e.get("file", "").lower() for e in (manifest.get("screenshots") or [])}, \
            f"Forbidden token '{token}' referenced as a screenshot file."


# 10
def test_no_secret_looking_strings_in_manifest():
    blob = MANIFEST.read_text(encoding="utf-8")
    for pat in SECRET_PATTERNS:
        assert not pat.search(blob), f"Secret-looking string matched {pat.pattern} in manifest."
