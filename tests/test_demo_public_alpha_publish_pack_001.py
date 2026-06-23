"""
Honesty tests for the Demo Public Alpha publish pack

Verifies the public-facing publish materials exist and preserve honest claim boundaries:
Demo Public Alpha, not production-ready, not full public alpha, not enterprise-ready, governed mission
spine, screenshot proof/non-proof framing, explicit operator approval in the pre-publish checklist, and
NO forbidden over-claims. Offline, deterministic — no backend, model, or network.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ALPHA = REPO_ROOT / "docs" / "alpha"

PUBLISH_PACK = ALPHA / "PUBLISH_PACK.md"
DEMO_SCRIPT = ALPHA / "DEMO_SCRIPT.md"
GALLERY = ALPHA / "SCREENSHOT_GALLERY.md"
KNOWN_LIMITATIONS = ALPHA / "KNOWN_LIMITATIONS_PUBLIC.md"
ANNOUNCEMENT_GITHUB = ALPHA / "ANNOUNCEMENT_GITHUB.md"
ANNOUNCEMENT_SOCIAL = ALPHA / "ANNOUNCEMENT_SOCIAL.md"
# Legacy docs from the same lane (kept and still honesty-scanned).
ANNOUNCEMENT_DRAFT = ALPHA / "ANNOUNCEMENT_DRAFT.md"
FAQ = ALPHA / "FAQ_DEMO_PUBLIC_ALPHA.md"

MANIFEST = ALPHA / "screenshots" / "manifest.json"
MANIFEST_REL = "screenshots/manifest.json"
README = REPO_ROOT / "README.md"

ARTIFACT_JSON = REPO_ROOT / "artifacts" / "alpha" / "DEMO_PUBLIC_ALPHA_PUBLISH_PACK_001.json"

# Required brief-named deliverables.
REQUIRED_DOCS = [
    PUBLISH_PACK,
    DEMO_SCRIPT,
    KNOWN_LIMITATIONS,
    GALLERY,
    ANNOUNCEMENT_GITHUB,
    ANNOUNCEMENT_SOCIAL,
]

# Every doc subject to the honesty scan (required + legacy).
ALL_DOCS = REQUIRED_DOCS + [ANNOUNCEMENT_DRAFT, FAQ]

# Spine sequence (allow the arrow form used across the publish pack).
SPINE = "Goal → Mission Plan → Permission Check → AuditLedger → Mission Receipt → Command Center"

CANONICAL_LABEL = "Demo Public Alpha"

# Over-claims that must never appear in the public pack (lowercased substring match).
FORBIDDEN_CLAIMS = [
    "production-ready",
    "production ready",
    "full public alpha release is ready",
    "enterprise-ready",
    "universal governance complete",
    "universal side-effect governance is complete",
    "safe unattended autonomy",
    "live autonomy is complete",
    "live autonomy complete",
    "all side effects governed",
    "all tools/actions are permission-governed",
    "cloud escalation is production-ready",
    "spendingbrain real adapters are live",
    "agentfactory exists",
    "watcherloop is complete",
    # Hype words explicitly banned for social/announcement copy.
    "revolutionary",
    "fully autonomous",
    "unbreakable",
    "perfectly safe",
    # NOTE: `public_alpha_ready: true` is intentionally NOT listed here — a naive substring scan would
    # false-match the legitimate `demo_public_alpha_ready: true`. A separate test checks it precisely
    # with a negative-lookbehind regex instead.
]


def _text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# --- Existence ---------------------------------------------------------------
def test_required_documents_exist():
    for p in REQUIRED_DOCS:
        assert p.is_file(), f"required publish-pack doc missing: {p.relative_to(REPO_ROOT)}"


def test_artifact_json_exists():
    assert ARTIFACT_JSON.is_file()


# --- Canonical label ---------------------------------------------------------
def test_docs_use_canonical_release_label():
    for p in ALL_DOCS:
        assert CANONICAL_LABEL in _text(p), f"{p.name} must say '{CANONICAL_LABEL}'"


# --- Disclaimers -------------------------------------------------------------
def test_full_public_alpha_disclaimers_exist():
    for p in [PUBLISH_PACK, KNOWN_LIMITATIONS, ANNOUNCEMENT_GITHUB, ANNOUNCEMENT_SOCIAL]:
        low = _text(p).lower()
        assert "not full public alpha" in low or "not a full public alpha" in low, \
            f"{p.name} must say it is not full public alpha"


def test_production_and_enterprise_disclaimers_exist():
    for p in [PUBLISH_PACK, KNOWN_LIMITATIONS, ANNOUNCEMENT_GITHUB]:
        low = _text(p).lower()
        assert "not production-ready" in low or "not a production" in low, \
            f"{p.name} must disclaim production readiness"
        assert "not enterprise-ready" in low or "not enterprise" in low, \
            f"{p.name} must disclaim enterprise readiness"


# --- Spine -------------------------------------------------------------------
def test_docs_include_public_spine_sequence():
    assert SPINE in _text(PUBLISH_PACK)
    assert SPINE in _text(DEMO_SCRIPT)
    assert SPINE in _text(ANNOUNCEMENT_GITHUB)


# --- Screenshots -------------------------------------------------------------
def test_screenshot_gallery_references_manifest():
    assert MANIFEST_REL in _text(GALLERY)


def test_screenshot_links_resolve():
    manifest = json.loads(_text(MANIFEST))
    files = [s["file"] for s in manifest["screenshots"]]
    assert len(files) == 5
    gallery = _text(GALLERY)
    for fname in files:
        # image must exist on disk
        assert (ALPHA / "screenshots" / fname).is_file(), f"missing screenshot file: {fname}"
        # and be referenced in the gallery
        assert fname in gallery, f"gallery does not reference screenshot: {fname}"


def test_screenshot_gallery_explains_proof_and_non_proof():
    low = _text(GALLERY).lower()
    assert "what it proves" in low or "what this demonstrates" in low
    assert ("does not prove" in low) or ("does not demonstrate" in low)


# --- GitHub announcement -----------------------------------------------------
def test_github_announcement_contains_known_limitations():
    low = _text(ANNOUNCEMENT_GITHUB).lower()
    assert "limitation" in low, "GitHub announcement must surface current limitations"
    assert "broad frontend" in low, "GitHub announcement must name the frontend blocker"


# --- Social variants ---------------------------------------------------------
def test_social_variants_present_and_bounded():
    text = _text(ANNOUNCEMENT_SOCIAL)
    low = text.lower()
    for variant in ["short", "medium", "technical"]:
        assert variant.lower() in low, f"social announcement missing '{variant}' variant"
    # Required vocabulary present somewhere in the social copy.
    for token in ["local-first", "permission-governed", "mission", "mission receipt", "demo public alpha"]:
        assert token in low, f"social announcement missing required token: {token!r}"
    # No banned hype. (production/enterprise readiness is negation-checked in test_no_forbidden_claims;
    # here we ban only words that have no honest negated form in this copy.)
    for hype in ["revolutionary", "fully autonomous", "unbreakable", "perfectly safe"]:
        assert hype not in low, f"social announcement uses banned hype: {hype!r}"
    # "AGI" as a standalone token (not a substring of another word).
    assert not re.search(r"\bagi\b", low), "social announcement uses banned hype: 'AGI'"


# --- Pre-publish checklist requires explicit operator approval ---------------
def test_publish_checklist_requires_operator_approval():
    low = _text(PUBLISH_PACK).lower()
    assert "operator explicitly approves publication" in low, \
        "pre-publish checklist must require explicit operator approval"


# --- No absolute /home paths -------------------------------------------------
def test_no_absolute_home_paths():
    for p in ALL_DOCS + [PUBLISH_PACK]:
        assert "/home/" not in _text(p), f"{p.name} contains an absolute /home/ path"


# --- No IDE-only line links --------------------------------------------------
def test_no_ide_only_line_links():
    # IDE-only links look like (path#L42) — github-relative line anchors that don't render publicly.
    line_link = re.compile(r"\]\([^)]*#L\d+")
    for p in ALL_DOCS:
        assert not line_link.search(_text(p)), f"{p.name} contains an IDE-only #L line link"


# --- Forbidden claims --------------------------------------------------------
def test_no_forbidden_claims():
    for p in ALL_DOCS:
        low = _text(p).lower()
        for phrase in FORBIDDEN_CLAIMS:
            idx = 0
            while True:
                idx = low.find(phrase, idx)
                if idx == -1:
                    break
                # A forbidden term is a violation only when asserted positively. It is allowed inside
                # honest contexts: an explicit negation on the same line ("not production-ready", incl.
                # markdown-bold "**not**"), a "we do NOT claim ..." disclaimer, a question heading
                # ("### Is Aurion production-ready?"), or a "Do NOT say"/quoted-prohibition list.
                line_start = low.rfind("\n", 0, idx) + 1
                line_end = low.find("\n", idx)
                line = low[line_start: line_end if line_end != -1 else len(low)]
                window = low[line_start: idx].replace("*", "").replace("_", "")
                preceding = low[:idx]
                last_heading = preceding.rfind("\n#")
                heading_line = preceding[last_heading: preceding.find("\n", last_heading + 1)] if last_heading != -1 else ""
                negated = (
                    any(neg in window for neg in ["not ", "no ", "never ", "do not", "does not", "without "])
                    or "?" in line                       # question heading, answer follows
                    or "do not say" in heading_line      # explicit prohibition list
                    or "do not claim" in heading_line
                    or "banned" in line or "avoid" in line or "no hype" in line
                )
                assert negated, f"{p.name} positively asserts forbidden claim {phrase!r} in line: {line.strip()!r}"
                idx += len(phrase)


# --- public_alpha_ready must not be claimed true -----------------------------
def test_docs_do_not_claim_public_alpha_ready_true():
    # Match `public_alpha_ready: true` but NOT `demo_public_alpha_ready: true` (the demo flag is
    # legitimately true). Negative lookbehind for the `demo_` prefix.
    bad = re.compile(r"(?<!demo_)public_alpha_ready\s*[:=]\s*true")
    for p in ALL_DOCS:
        low = _text(p).lower()
        assert not bad.search(low), f"{p.name} must not claim public_alpha_ready true"
    pack = _text(PUBLISH_PACK).lower()
    assert "public_alpha_ready" in pack
    assert re.search(r"(?<!demo_)public_alpha_ready[^\n]*false", pack), \
        "Publish pack must state public_alpha_ready is false"


# --- Machine artifact: honest publication-state flags ------------------------
def test_artifact_publication_state_is_honest():
    data = json.loads(_text(ARTIFACT_JSON))
    # The legacy `publication_executed` flag has been replaced with explicit, honest publication state.
    assert "publication_executed" not in data, \
        "publication_executed must be replaced by explicit repository_public / announcement_published / github_release_created"
    assert data.get("announcement_published") is False, "no announcement published by this work"
    assert data.get("github_release_created") is False, "no GitHub release created by this work"
    # Readiness split is unchanged.
    assert data.get("public_alpha_ready") is False
    assert data.get("demo_public_alpha_ready") is True


# --- README links resolve (conditional on README referencing the pack) -------
def test_readme_links_publish_pack_if_referenced():
    text = _text(README)
    if "docs/alpha/PUBLISH_PACK.md" in text:
        for link in [
            "docs/alpha/PUBLISH_PACK.md",
            "docs/alpha/DEMO_SCRIPT.md",
            "docs/alpha/SCREENSHOT_GALLERY.md",
        ]:
            assert link in text, f"README references publish pack but is missing link: {link}"
