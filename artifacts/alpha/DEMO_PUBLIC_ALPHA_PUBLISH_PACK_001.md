# Demo Public Alpha Publish Pack — 001

**Mission ID:** `DEMO-PUBLIC-ALPHA-PUBLISH-PACK-001`
**Date:** 2026-06-21 (reconciled to brief)
**Status:** complete — publication materials ready for operator review

## Executive Summary

Created/reconciled the public-facing **Demo Public Alpha** presentation pack for Aurion's governed
mission spine to match the canonical mission brief deliverable list. A prior run produced an adjacent set
of files (`ANNOUNCEMENT_DRAFT.md`, `FAQ_DEMO_PUBLIC_ALPHA.md`); this run adds the brief-named
deliverables (`KNOWN_LIMITATIONS_PUBLIC.md`, `ANNOUNCEMENT_GITHUB.md`, `ANNOUNCEMENT_SOCIAL.md`),
restructures `PUBLISH_PACK.md` to the full canonical section set (incl. pre-publish checklist with
explicit operator approval, post-publish verification, and rollback procedure), and rebuilds the
`DEMO_SCRIPT.md` into the seven-scene structure. The legacy files are kept and remain honesty-scanned.
Nothing is published; no release is created; no commit is made. All materials preserve the honest split:
**`demo_public_alpha_ready: true`, `public_alpha_ready: false`, overall yellow**, and make none of the
forbidden over-claims.

## Files Created / Reconciled

| File | Purpose |
|---|---|
| `docs/alpha/PUBLISH_PACK.md` | Canonical operator publish checklist — full brief section set, pre/post-publish checklists, rollback |
| `docs/alpha/DEMO_SCRIPT.md` | Seven-scene narrated walkthrough (narrator + on-screen actions), 3–5 min |
| `docs/alpha/KNOWN_LIMITATIONS_PUBLIC.md` | Public-safe limitation list (maturity/autonomy/frontend/governance/platform/external/enterprise) |
| `docs/alpha/SCREENSHOT_GALLERY.md` | Per-screenshot title/caption/proves/does-not-prove/safe note, manifest-referenced |
| `docs/alpha/ANNOUNCEMENT_GITHUB.md` | Reusable GitHub release announcement with required disclaimer |
| `docs/alpha/ANNOUNCEMENT_SOCIAL.md` | Short (290 chars) / medium / technical variants, bounded, no hype |
| `docs/alpha/ANNOUNCEMENT_DRAFT.md` | Legacy draft variants (kept, still scanned) |
| `docs/alpha/FAQ_DEMO_PUBLIC_ALPHA.md` | Legacy honest FAQ (kept, still scanned) |
| `tests/test_demo_public_alpha_publish_pack_001.py` | Honesty tests (existence, label, disclaimers, spine, screenshots, social, approval) |
| `artifacts/alpha/DEMO_PUBLIC_ALPHA_PUBLISH_PACK_001.{md,json}` | This artifact |

**Modified:** `README.md` — "Public Demo Materials" section linking the publish docs (conditional per the
README positioning test).

## Claim Boundaries

**Allowed:** controlled Demo Public Alpha · governed mission spine · local-first · permission-governed ·
Mission Receipts · AuditLedger evidence · BlackBox trace reference · Command Center inspection · not
production-ready · not full public alpha.

**Forbidden (and absent / only negated):** production-ready · full public alpha · enterprise-ready ·
universal governance complete · safe unattended autonomy · live autonomy complete · all side effects
governed · cloud escalation production-ready · real spending adapters live · agent-spawning exists ·
background watcher loops complete.

The honesty test asserts forbidden terms appear only inside explicit negations, "we do NOT claim …"
disclaimers, question headings, or "Do NOT say" prohibition lists — never as positive assertions.

## Public Narrative

> Aurion is a local-first governed AI mission system. It turns user goals into governed AI missions.
> This controlled Demo Public Alpha shows one spine:
> Goal → Mission Plan → Permission Check → AuditLedger → Mission Receipt → Command Center.
> It is not production-ready and not full public alpha. The governance-first principle: agents should
> not just act; they should leave receipts.

## Screenshot References

Backed by `docs/alpha/screenshots/manifest.json` (`release_context: demo_public_alpha`):
`01-command-center-shell.png`, `02-mission-receipts-list.png`,
`03-public-spine-demo-receipt-detail.png`, `04-demo-governance-evidence.png`, `05-alpha-status.png`.
Each gallery entry states what it proves and what it does not prove.

## FAQ Summary

Production-ready: no. Full public alpha: no. Live autonomy: not complete. Cloud: local-first, gated.
Spending: advisory/read-only only. External tools: permission-checked, not universally governed.
Mission Receipt: defined. Local-first not local-only: explained. Missing: broad frontend suite + dev/lab
modules. Next milestone: green the broad frontend suite. License: **open source under AGPL-3.0-only**
(strong copyleft; modified network use may trigger AGPL §13 source-offer; no paid commercial license
exists yet; plugin/limb boundary under review).

## Validation

```text
pytest tests/test_demo_public_alpha_publish_pack_001.py                 → pass
pytest (full exported suite)                                            → 107 passed, 1 skipped
python scripts/demo/run_public_spine_demo.py                           → demo_public_alpha_ready=true,
                                                                          public_alpha_ready=false
```

## Git Tracking Notes

New publish docs + test are untracked; `README.md` is tracked + modified. Protect with this explicit
pathspec command (audit-only — **not executed**, no commit, no blanket add):

```bash
git add -- \
  docs/alpha/PUBLISH_PACK.md \
  docs/alpha/DEMO_SCRIPT.md \
  docs/alpha/KNOWN_LIMITATIONS_PUBLIC.md \
  docs/alpha/SCREENSHOT_GALLERY.md \
  docs/alpha/ANNOUNCEMENT_GITHUB.md \
  docs/alpha/ANNOUNCEMENT_SOCIAL.md \
  docs/alpha/ANNOUNCEMENT_DRAFT.md \
  docs/alpha/FAQ_DEMO_PUBLIC_ALPHA.md \
  tests/test_demo_public_alpha_publish_pack_001.py \
  artifacts/alpha/DEMO_PUBLIC_ALPHA_PUBLISH_PACK_001.md \
  artifacts/alpha/DEMO_PUBLIC_ALPHA_PUBLISH_PACK_001.json \
  README.md
```

## Remaining Caveats

- Full public alpha remains blocked by the broad frontend (npm) test suite (unchanged; out of scope).
- These materials are drafts for operator review — nothing is published and no release is created.
- License: open source under AGPL-3.0-only (strong copyleft; modified network use may trigger AGPL §13 source-offer; no paid commercial license exists yet; plugin/limb boundary under review).

## Recommended Next Step

`operator_review_then_publish_or_record_demo` — operator reviews the pack, optionally stages/commits via
the command above, then records the demo or publishes the announcement when ready.
