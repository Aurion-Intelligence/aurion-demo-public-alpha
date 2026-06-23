"""
Tests for Alpha Install Walkthrough doc honesty — [alpha-install-walkthrough-001]

Validates:
  - Required files exist
  - Required sections are present
  - No fake readiness claims (no "public alpha ready: yes" / "production ready")
  - No live autonomy claims
  - No obvious secret placeholders with real-looking keys
  - References the public spine demo command
  - References SETUP_TROUBLESHOOTING.md
  - Does not claim screenshots are present
  - Honest "not ready" language preserved

All tests are offline and deterministic — no backend, no model, no network.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
WALKTHROUGH = REPO_ROOT / "docs" / "alpha" / "INSTALL_WALKTHROUGH.md"
TROUBLESHOOTING = REPO_ROOT / "docs" / "alpha" / "SETUP_TROUBLESHOOTING.md"
ALPHA_STATUS = REPO_ROOT / "docs" / "alpha" / "ALPHA_STATUS.md"
KNOWN_ISSUES = REPO_ROOT / "docs" / "alpha" / "KNOWN_ISSUES.md"

# Secret-looking patterns that must NOT appear literally in walkthrough
_REAL_KEY_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_\-]{16,}"),   # Real Anthropic key
    re.compile(r"sk-[A-Za-z0-9]{32,}"),            # Real OpenAI key
    re.compile(r"ghp_[A-Za-z0-9]{36,}"),           # Real GitHub PAT
    re.compile(r"AKIA[0-9A-Z]{16}"),               # Real AWS key
]

# Required sections (exact headings) in the walkthrough
REQUIRED_SECTIONS = [
    "## Status",
    "## What This Setup Gives You",
    "## What This Setup Does Not Enable",
    "## Requirements",
    "## Clone Repo",
    "## Python Backend Setup",
    "## Environment Variables",
    "## Local Model Setup",
    "## Start Backend",
    "## Command Center Setup",
    "## Start Command Center",
    "## Health Checks",
    "## Run / Inspect Public Spine Demo",
    "## Open Mission Receipt",
    "## Troubleshooting",
    "## Known Limitations",
    "## Safe Cleanup",
    "## Next Steps",
]

# Phrases that must NOT appear (fake-green claims)
# Note: "not production-ready" / "not production ready" are honest and acceptable;
# only the unqualified positive claim is forbidden.
FAKE_POSITIVE_PHRASES = [
    "public alpha ready: yes",
    "public alpha ready: **yes**",
    "public_alpha_ready: yes",
    "live autonomy available",
    "live workers enabled",
    "autonomous execution enabled",
    "fully autonomous",
    "fully tested on clean machine",
    "guaranteed safe",
]

# Phrases that MUST appear (honest limits)
REQUIRED_HONESTY_PHRASES = [
    "not ready",          # public alpha not ready
    "not enable",         # what this does not enable
    "governed restraint", # honest about skipped steps
    "not a failure",      # governed skip is not a bug
]


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

class TestFilesExist:
    def test_install_walkthrough_exists(self):
        assert WALKTHROUGH.exists(), f"Missing: {WALKTHROUGH}"

    def test_setup_troubleshooting_exists(self):
        assert TROUBLESHOOTING.exists(), f"Missing: {TROUBLESHOOTING}"


# ---------------------------------------------------------------------------
# Required sections in walkthrough
# ---------------------------------------------------------------------------

class TestWalkthroughSections:
    @pytest.fixture(autouse=True)
    def content(self):
        if not WALKTHROUGH.exists():
            pytest.skip("Walkthrough not yet generated")
        self._content = WALKTHROUGH.read_text(encoding="utf-8")

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_required_section_present(self, section):
        assert section in self._content, (
            f"Walkthrough missing required section: {section!r}"
        )

    def test_has_status_section_with_no_claim(self):
        # Status section must not claim public alpha ready: yes
        status_idx = self._content.find("## Status")
        # Find end of status section (next ##)
        next_h2 = self._content.find("\n## ", status_idx + 1)
        status_block = self._content[status_idx:next_h2] if next_h2 > 0 else self._content[status_idx:]
        assert "No" in status_block or "no" in status_block, (
            "Status section must say public alpha is not ready"
        )


# ---------------------------------------------------------------------------
# No fake readiness claims
# ---------------------------------------------------------------------------

class TestNoFakeReadinessClaims:
    @pytest.fixture(autouse=True)
    def content(self):
        if not WALKTHROUGH.exists():
            pytest.skip("Walkthrough not yet generated")
        self._content = WALKTHROUGH.read_text(encoding="utf-8").lower()

    @pytest.mark.parametrize("phrase", FAKE_POSITIVE_PHRASES)
    def test_no_fake_positive_phrase(self, phrase):
        assert phrase.lower() not in self._content, (
            f"Walkthrough contains forbidden fake-positive phrase: {phrase!r}"
        )

    def test_does_not_positively_claim_production_ready(self):
        """'production-ready' in a denial is fine.
        Lines inside blockquote denial lists ('> -') are excluded — the whole
        'What This Setup Does Not Enable' block is a denial context.
        Only a bare positive claim outside denial context is forbidden.
        """
        for line in self._content.splitlines():
            ll = line.lower().strip()
            # Skip blockquote denial bullets — whole block is a denial context
            if ll.startswith("> -"):
                continue
            if "production ready" in ll or "production-ready" in ll:
                assert "not" in ll or "is not" in ll or "never" in ll, (
                    f"Line appears to positively claim production readiness: {line!r}"
                )

    def test_does_not_claim_screenshots_available(self):
        # Screenshots are a known blocker — walkthrough must not say they exist
        assert "screenshots: ✅" not in self._content
        assert "screenshots: pass" not in self._content


# ---------------------------------------------------------------------------
# Required honesty phrases
# ---------------------------------------------------------------------------

class TestHonestyPhrases:
    @pytest.fixture(autouse=True)
    def content(self):
        if not WALKTHROUGH.exists():
            pytest.skip("Walkthrough not yet generated")
        self._content = WALKTHROUGH.read_text(encoding="utf-8").lower()

    @pytest.mark.parametrize("phrase", REQUIRED_HONESTY_PHRASES)
    def test_required_honesty_phrase_present(self, phrase):
        assert phrase.lower() in self._content, (
            f"Walkthrough missing required honest phrase: {phrase!r}"
        )

    def test_mentions_what_it_does_not_enable(self):
        assert "does not enable" in self._content or "not enable" in self._content

    def test_mentions_governed_restraint(self):
        assert "governed restraint" in self._content

    def test_mentions_public_alpha_not_ready(self):
        # Must say public alpha is not ready somewhere
        assert "not ready" in self._content


# ---------------------------------------------------------------------------
# No secret placeholders with real-looking keys
# ---------------------------------------------------------------------------

class TestNoRealLookingSecrets:
    @pytest.fixture(autouse=True)
    def content(self):
        if not WALKTHROUGH.exists():
            pytest.skip("Walkthrough not yet generated")
        self._content = WALKTHROUGH.read_text(encoding="utf-8")

    @pytest.mark.parametrize("pattern", _REAL_KEY_PATTERNS)
    def test_no_real_looking_key(self, pattern):
        match = pattern.search(self._content)
        assert match is None, (
            f"Walkthrough contains a real-looking secret key matching {pattern.pattern!r}: "
            f"{match.group()!r}"
        )

    def test_placeholder_keys_are_obviously_fake(self):
        """If API key examples exist, they must use obvious placeholders."""
        # Fake placeholder markers that are acceptable
        acceptable = ["your_", "...", "sk-ant-...", "sk-...", "<your-", "example"]
        # Look for any line with API_KEY that might have a value
        for line in self._content.splitlines():
            if "API_KEY" in line and "=" in line:
                value_part = line.split("=", 1)[1].strip()
                if value_part and not value_part.startswith("#"):
                    # Ensure it looks like a placeholder, not a real key
                    is_placeholder = any(p in value_part for p in acceptable)
                    assert is_placeholder or len(value_part) < 12, (
                        f"API_KEY line may contain a real value: {line!r}"
                    )


# ---------------------------------------------------------------------------
# References to key resources
# ---------------------------------------------------------------------------

class TestRequiredReferences:
    @pytest.fixture(autouse=True)
    def content(self):
        if not WALKTHROUGH.exists():
            pytest.skip("Walkthrough not yet generated")
        self._content = WALKTHROUGH.read_text(encoding="utf-8")

    def test_references_public_spine_demo_command(self):
        assert "run_public_spine_demo.py" in self._content, (
            "Walkthrough must reference the self-contained public spine demo runner"
        )

    def test_references_setup_troubleshooting(self):
        assert "SETUP_TROUBLESHOOTING.md" in self._content, (
            "Walkthrough must link to SETUP_TROUBLESHOOTING.md"
        )

    def test_references_alpha_status(self):
        assert "ALPHA_STATUS.md" in self._content, (
            "Walkthrough must reference ALPHA_STATUS.md"
        )

    def test_references_mission_receipt(self):
        assert "Mission Receipt" in self._content or "mission receipt" in self._content.lower()

    def test_references_command_center(self):
        assert "Command Center" in self._content

    def test_references_ollama(self):
        assert "ollama" in self._content.lower() or "Ollama" in self._content

    def test_references_env_example(self):
        assert ".env.example" in self._content, (
            "Walkthrough must reference .env.example"
        )

    def test_references_uvicorn_start_command(self):
        assert "uvicorn main:app" in self._content, (
            "Walkthrough must include the verified backend start command"
        )

    def test_references_health_check(self):
        assert "health" in self._content.lower(), (
            "Walkthrough must include a health check step"
        )


# ---------------------------------------------------------------------------
# Troubleshooting doc sections
# ---------------------------------------------------------------------------

class TestTroubleshootingDoc:
    @pytest.fixture(autouse=True)
    def content(self):
        if not TROUBLESHOOTING.exists():
            pytest.skip("Troubleshooting doc not yet generated")
        self._content = TROUBLESHOOTING.read_text(encoding="utf-8")

    def test_covers_python_venv_issues(self):
        assert "venv" in self._content.lower() or "virtual" in self._content.lower()

    def test_covers_backend_issues(self):
        assert "uvicorn" in self._content.lower() or "backend" in self._content.lower()

    def test_covers_ollama_issues(self):
        assert "ollama" in self._content.lower()

    def test_covers_command_center_issues(self):
        assert "command center" in self._content.lower() or "npm" in self._content.lower()

    def test_does_not_claim_production_ready(self):
        assert "production ready" not in self._content.lower()


# ---------------------------------------------------------------------------
# Alpha status gate — walkthrough detection wires correctly
# ---------------------------------------------------------------------------

class TestAlphaStatusWiring:
    def test_install_walkthrough_at_expected_generator_path(self):
        """The alpha status generator checks for docs/alpha/INSTALL_WALKTHROUGH.md.
        Verify the file is at that path so the gate will pass after regeneration."""
        expected = REPO_ROOT / "docs" / "alpha" / "INSTALL_WALKTHROUGH.md"
        assert expected.exists(), (
            f"INSTALL_WALKTHROUGH.md must be at {expected} for the alpha status gate to detect it"
        )

    def test_generate_alpha_status_script_exists(self):
        script = REPO_ROOT / "scripts" / "alpha" / "generate_alpha_status.py"
        assert script.exists(), "Alpha status generator script must exist"

    def test_alpha_status_generator_detects_walkthrough_path(self):
        """The logic is in aurion/alpha/status.py (the compute_gates function).
        Verify it checks for INSTALL_WALKTHROUGH.md."""
        status_module = REPO_ROOT / "aurion" / "alpha" / "status.py"
        if not status_module.exists():
            pytest.skip("aurion/alpha/status.py not found")
        src = status_module.read_text(encoding="utf-8")
        assert "INSTALL_WALKTHROUGH.md" in src, (
            "aurion/alpha/status.py must check for docs/alpha/INSTALL_WALKTHROUGH.md "
            "so the install_walkthrough gate will pass after the doc is created"
        )
