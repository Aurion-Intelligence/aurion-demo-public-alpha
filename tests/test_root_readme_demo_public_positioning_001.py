from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"


def _readme_text() -> str:
    return README.read_text(encoding="utf-8")


def test_root_readme_exists() -> None:
    assert README.is_file()


def test_root_readme_contains_core_public_positioning() -> None:
    text = _readme_text()

    assert "local-first governed AI mission system" in text
    assert "Demo Public Alpha" in text
    assert "not production-ready" in text
    assert "Mission -> Permission -> Execution/Proposal -> Receipt -> Memory Update" in text


def test_root_readme_links_verified_public_spine_docs() -> None:
    text = _readme_text()

    required_links = [
        "docs/alpha/INSTALL_WALKTHROUGH.md",
        "docs/alpha/SETUP_TROUBLESHOOTING.md",
        "artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.md",
        "artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.json",
        "docs/alpha/DEMO_STATUS.md",
    ]
    for link in required_links:
        assert (REPO_ROOT / link).exists(), f"README links missing repo file: {link}"
        assert link in text


def test_root_readme_links_screenshots_manifest_only_if_present() -> None:
    text = _readme_text()
    manifest_link = "docs/alpha/screenshots/manifest.json"

    if (REPO_ROOT / manifest_link).exists():
        assert manifest_link in text
    else:
        assert manifest_link not in text
        assert "screenshots as a public-alpha blocker" in text


def test_root_readme_does_not_claim_public_alpha_ready() -> None:
    text = _readme_text().lower()

    forbidden_ready_claims = [
        "public alpha is fully ready",
        "public alpha ready: yes",
        "public_alpha_ready: true",
        "public alpha release is ready",
    ]
    for phrase in forbidden_ready_claims:
        assert phrase not in text

    assert "not a full public alpha release yet" in text


def test_root_readme_does_not_make_forbidden_platform_claims() -> None:
    text = _readme_text().lower()

    forbidden_claims = [
        "personal chatgpt clone",
        "odysseus clone",
        "generic ai workspace",
        "ai os that does everything",
        "fully autonomous second brain",
        "enterprise-ready agent platform",
        "production-ready ai agent runtime",
        "universal side-effect governance is complete",
        "live autonomy is complete",
        "agentfactory exists",
        "watcherloop is complete",
        "spendingbrain real adapters are live",
        "cloud escalation is generally safe",
        "all tools/actions are permission-governed",
    ]
    for phrase in forbidden_claims:
        assert phrase not in text


def test_root_readme_status_disclaimer_exists() -> None:
    text = _readme_text()

    assert "## Status Disclaimer" in text
    assert "not production-ready, not full public alpha, and not live-autonomy complete" in text


def test_legacy_case_readme_points_to_canonical_readme() -> None:
    # The lowercase `Readme.md` is only a case-compatibility stub used in the private monorepo. The
    # public export ships a single canonical `README.md`, so the stub is intentionally absent here. When
    # the stub is present it must point at the canonical README; when it is absent there is nothing to
    # check.
    import pytest

    legacy = REPO_ROOT / "Readme.md"
    if not legacy.is_file():
        pytest.skip("no legacy lowercase Readme.md stub in this repo (single canonical README.md)")
    text = legacy.read_text(encoding="utf-8")
    assert "[`README.md`](README.md)" in text
    assert "local-first governed AI mission system" in text
