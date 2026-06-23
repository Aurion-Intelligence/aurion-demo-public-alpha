# Aurion Demo Public Alpha — Publish Pack

> Canonical operator publication checklist for Aurion's **controlled Demo Public Alpha**. This is **not**
> a public release announcement and makes **no** claim of full public alpha or production readiness.
> Nothing here is published until the operator explicitly approves it.

## Release Identity

- **Release name:** Aurion Demo Public Alpha (do not shorten to "Public Alpha").
- **Release category:** controlled public demo / dev-alpha narrative.
- **`demo_public_alpha_ready`:** true (`ready_with_minor_caveats`).
- **`public_alpha_ready`:** false.
- **Overall:** yellow.
- **Full-public-alpha blocker:** broad frontend (npm) test suite still fails.
- **License:** open source under **AGPL-3.0-only** (see [`../../LICENSE`](../../LICENSE)).

Aurion is **not production-ready** and is **not a full public alpha release yet**. It **is** open source
under AGPL-3.0-only — you may use, modify, redistribute, and commercially use it under AGPL terms.
Modified network-accessible versions may trigger AGPL §13 source-offer obligations. No paid commercial
license exists today (one may be developed later, subject to legal review). The plugin/limb licensing
boundary is still under review.

## One-Sentence Description

Aurion is a local-first, permission-governed AI mission system that turns user goals into governed
missions and records what happened through receipts, evidence, and audit trails.

## Thirty-Second Explanation

Most AI systems focus on giving agents more power. Aurion focuses on governing that power. Aurion turns
goals into structured missions, checks permissions before action, records decisions and evidence, and
produces a Mission Receipt showing what happened. This controlled Demo Public Alpha shows one governed
spine end to end through the real Command Center UI. It is not production-ready and not a full public
alpha — the point is the governance-first direction: agents should not just act; they should leave
receipts.

## What the Demo Shows

The bounded public spine demo (`PUBLIC-SPINE-DEMO-LOOP-001`) demonstrates:

- a deterministic, local-first governed mission (a repo/alpha health check),
- a Mission Plan with microsteps, classified proposed-only / dry-run,
- PermissionGraph checks (local read allowed; external network / writes denied),
- AuditLedger event references,
- a BlackBox decision-trace reference,
- advisory, read-only cost-governance evidence,
- a canonical **Mission Receipt** visible in the Command Center,
- honest **unavailable** markers where data is missing — never fake-green.

It does **not** show production readiness, full public alpha, enterprise readiness, safe unattended /
live autonomy, universal side-effect governance, real spending, or a production-grade cloud escalation
path.

## Governed Mission Spine

```text
Goal
→ Mission Plan
→ Microsteps
→ Permission Check
→ Governed Execution / Dry Run
→ AuditLedger
→ BlackBox Trace
→ Mission Receipt
→ Command Center
```

In one line, the demonstrated spine is:

`Goal → Mission Plan → Permission Check → AuditLedger → Mission Receipt → Command Center`

## Screenshot Gallery

See [`SCREENSHOT_GALLERY.md`](SCREENSHOT_GALLERY.md), backed by the manifest at
[`screenshots/manifest.json`](screenshots/manifest.json). The screenshots are deterministic
fixture-backed captures rendered through the real production-built Command Center UI using genuine demo
Mission Receipt data — not full-stack production screenshots.

## Demo Walkthrough

See [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) for the narrated 3–5 minute walkthrough (scene-by-scene, with
narrator text and on-screen actions) usable for a recording, live demo, or written GitHub walkthrough.

## Installation

See [`INSTALL_WALKTHROUGH.md`](INSTALL_WALKTHROUGH.md) and
[`SETUP_TROUBLESHOOTING.md`](SETUP_TROUBLESHOOTING.md). The self-contained, offline demo runs locally
with `python scripts/demo/run_public_spine_demo.py` (validate/replay) or
`python scripts/demo/run_public_spine_demo.py --mode generate` (generate a fresh bounded receipt). The
demo artifacts live under [`../../artifacts/demo/`](../../artifacts/demo/).

## Known Limitations

See [`KNOWN_LIMITATIONS_PUBLIC.md`](KNOWN_LIMITATIONS_PUBLIC.md) for the public-safe limitation list, and
[`ALPHA_STATUS.md`](ALPHA_STATUS.md) / [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) for the generated,
evidence-derived truth. Headline: full public alpha is blocked by the broad frontend test suite.

## What This Release Is Not

- not production-ready
- not a full public alpha
- not enterprise-ready
- not a proof of complete unattended / live autonomy
- not a claim that every side effect is universally governed
- not a claim of complete cloud / tool / provider support

We do **not** claim any of these:

- not production-ready
- not full public alpha
- not enterprise-ready
- not universal governance complete
- not safe unattended autonomy
- not live autonomy complete
- not all side effects governed
- not a production-grade cloud escalation path
- not live real-spending adapters

## Suggested GitHub Release Text

See [`ANNOUNCEMENT_GITHUB.md`](ANNOUNCEMENT_GITHUB.md) for the full reusable GitHub release / repository
announcement, including the required disclaimer:

> This is a controlled Demo Public Alpha of Aurion's governed mission spine. It is not a production
> release, full public alpha, enterprise platform, or claim of complete unattended autonomy.

## Suggested Social Announcement

See [`ANNOUNCEMENT_SOCIAL.md`](ANNOUNCEMENT_SOCIAL.md) for short, medium, and technical variants. Example
short post:

> Aurion: a local-first, permission-governed AI mission system. It turns goals into governed,
> mission-based runs, checks permissions before acting, and produces Mission Receipts you can inspect.
> This is a controlled Demo Public Alpha — not production, not full public alpha. Feedback welcome.

## Pre-Publish Checklist

```text
[ ] Canonical demo files are committed
[ ] Git working tree reviewed
[ ] README links resolve
[ ] Screenshot manifest passes
[ ] Demo receipt renders
[ ] Install walkthrough passes
[ ] No secrets or local paths found
[ ] demo_public_alpha_ready is true
[ ] public_alpha_ready remains false
[ ] No production, enterprise, or live-autonomy claims
[ ] Operator explicitly approves publication
```

The final item — explicit operator approval — is mandatory. No publication step (GitHub release, push,
social post) may be executed until the operator approves.

## Post-Publish Verification

After the operator approves and publishes:

```text
[ ] Published release renders correctly (screenshots, links, disclaimers)
[ ] All relative links resolve from the published page
[ ] No absolute local filesystem paths leaked (e.g. user-home directory paths)
[ ] Disclaimer ("not production / not full public alpha / not enterprise / not unattended autonomy") visible
[ ] demo_public_alpha_ready still true; public_alpha_ready still false
[ ] Re-run focused honesty tests pass post-publish
```

## Rollback / Correction Procedure

If an over-claim, broken link, or leaked path is found after publishing:

1. **Do not panic-delete** — capture what was published first (links may be cached/indexed).
2. **Correct in-repo** — fix the source document(s) and re-run the honesty tests.
3. **Edit or unpublish the release** — edit the GitHub release / social post text, or mark it as draft
   if the issue is material.
4. **Re-verify** — run the Post-Publish Verification checklist again.
5. **Record** — note the correction in `agents_memory/` and `TODO.md` so the next agent has context.

## Links

- [Demo script](DEMO_SCRIPT.md)
- [Screenshot gallery](SCREENSHOT_GALLERY.md)
- [Known limitations (public)](KNOWN_LIMITATIONS_PUBLIC.md)
- [GitHub announcement](ANNOUNCEMENT_GITHUB.md) · [Social announcements](ANNOUNCEMENT_SOCIAL.md)
- [Demo Public Alpha FAQ](FAQ_DEMO_PUBLIC_ALPHA.md) · [Announcement draft](ANNOUNCEMENT_DRAFT.md)
- [Install walkthrough](INSTALL_WALKTHROUGH.md) · [Troubleshooting](SETUP_TROUBLESHOOTING.md)
- [Alpha status](ALPHA_STATUS.md) · [Known issues](KNOWN_ISSUES.md)
- [Public spine demo report](../../artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.md)
- [License (AGPL-3.0-only)](../../LICENSE)
