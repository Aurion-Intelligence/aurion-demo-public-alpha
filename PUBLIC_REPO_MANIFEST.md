# Aurion Demo Public Alpha — Public Repo Export Manifest

**Export ID:** PUBLIC-DEMO-REPO-EXPORT-001
**Generated:** 2026-06-22
**Source repository:** the private source repo (PRIVATE — kept private and unchanged)
**Source commit:** `c6e0a03cdfd560a80c4995abdd7b6ad2dda07f67`
**Export root:** `~/aurion-public-export`
**Git history included:** NO (clean export; no `.git`, no prior commits)

This directory is a **clean public-safe export** of the approved Aurion Demo Public Alpha package.
It is **not** a git repository and has **not** been committed, pushed, or published. The private
source repository was not modified.

## What is included (49 files)

- `README.md` — canonical public entrypoint
- `LICENSE` — **GNU AGPL-3.0-only** (canonical official text)
- `CONTRIBUTING.md` — feedback welcome; external code merges paused pending contributor-rights process
- `docs/alpha/**` — publish pack (hub), announcements (GitHub + social), demo script, screenshot
  gallery, public known-limitations, install + troubleshooting, alpha status, known issues, FAQ,
  deprecated announcement draft, README_ALPHA, 5 screenshots + manifest
- `artifacts/alpha/**` — public publish-pack artifact (`.md`/`.json`) + `alpha_status.json`
- `artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.*` — bounded demo proof (report, scenario, audit jsonl,
  BlackBox decision traces, router index)
- `artifacts/mission_receipts/*demo-PUBLIC-SPINE-DEMO-LOOP-001*` — the two demo Mission Receipts only
- `scripts/demo/run_public_spine_demo.py` — **self-contained, offline demo runner** (validate/replay or
  generate a bounded Mission Receipt; no private imports, no network, no spend, no live autonomy)
- `aurion/alpha/status.py`, `scripts/alpha/generate_alpha_status.py` — alpha status tooling (offline,
  self-contained)
- `aurion-command-center/tests/alpha/**` + `tests/fixtures/alpha-screenshots/**` — screenshot capture
  spec + deterministic fixtures (the Playwright spec needs the private toolchain; the PNG fixtures ship)
- `tests/test_*_001.py` (×5) — public-safe honesty/demo tests, incl.
  `test_public_spine_demo_runner_001.py` (exercises only exported code)

A complete per-file list with SHA-256 prefixes and source paths is in
[`PUBLIC_REPO_MANIFEST.json`](PUBLIC_REPO_MANIFEST.json).

## What is deliberately EXCLUDED

- `.git/` and all prior commit history / branches
- `agents_memory/**` — internal mission handoffs
- `artifacts/alpha/DEMO_PUBLIC_ALPHA_READINESS_GATE_*`, `…_TRACKED_READINESS_VERIFY_*` — internal
  readiness audits (the latter contained real `<user-home>/...` paths)
- `artifacts/repo_hygiene/**` — internal repo-hygiene audits
- `artifacts/mission_receipts/20260214_CC-LINUX-LAUNCHER-001.json` — **contained real
  `<user-home>/...` absolute paths** (non-demo receipt)
- All unrelated Aurion modules, private configuration, routing logic, evaluation data, and personal data

## Modified-for-export

- `docs/alpha/README_ALPHA.md` — 3 outbound links to **excluded internal files**
  (`AURION_GOVERNANCE.md`, `docs/demo/mission_receipt_demo.md`, `docs/mission_receipts.md`) were
  repointed to in-export canonical targets so the public export has no dead links. No claims changed.
- **Self-contained demo runner added.** `scripts/demo/run_public_spine_demo.py` (offline, no private
  imports) replaces the private `scripts/demo/public_spine_demo_loop_001.py` for public use. All
  README/docs/publish-pack/artifact "run/rerun/try the demo" instructions now point at it.
- `tests/test_public_spine_demo_loop_001.py` (removed earlier) is **replaced** by
  `tests/test_public_spine_demo_runner_001.py`, which exercises only exported code (the runner + exported
  fixtures). Full export suite: **107 passed, 1 skipped, 0 errors**.
- **Removed non-runnable screenshot tooling:** `scripts/alpha/build_screenshot_fixtures.py` (imports
  private `aurion.mission.receipts`) and `scripts/alpha/capture_screenshots.sh` (needs that script + npm
  + Playwright + a running UI). The screenshot PNG fixtures ship; "regenerate" notes updated to say the
  regeneration toolchain lives in the private repo.
- `docs/alpha/README_ALPHA.md` — 3 outbound links to excluded internal files were repointed to in-export
  canonical targets (no dead links); the demo command was repointed to the public runner. No claims
  changed.
- The `how_to_rerun`/validation blocks in the `PUBLIC_SPINE_DEMO_LOOP_001` and publish-pack artifacts
  were repointed to the public runner + public test; their recorded evidence (decision traces,
  AuditLedger) is unchanged and shipped fixture-backed.

> The `PUBLIC_SPINE_DEMO_LOOP_001` artifacts under `artifacts/demo/` remain a faithful record of the
> original private run (e.g. decision-trace `source_file` provenance still names the private script —
> that is historical fact, not an instruction). The public **runner** replays that fixture-backed
> evidence and can also generate a fresh bounded receipt, so the public repo is now self-contained for
> its bounded demo path.

## Secret / privacy scan (export surface)

| Check | Result |
|---|---|
| Absolute `/home/`, `/Users/`, `C:\Users` paths | **none** (only scanner-string literals in test code) |
| Local username (`armalite`, `migueljuan`) | **none** |
| Real API keys / tokens / private keys | **none** (only regex literals + annotated `sk-ant-...` placeholders) |
| Private repo references (the private source repo, `Aurion-Intelligence`, repo URL) | **none** |
| Personal email | **none** |
| Links to excluded internal files | **none** (after README_ALPHA fix) |
| Relative link integrity | **all resolve within the export** |

## License — AGPL-3.0-only (resolved)

- The export ships a single `LICENSE` = **GNU AGPL-3.0-only** (canonical official text from gnu.org).
  No `LICENSE.txt`, no proprietary/all-rights-reserved/source-visible-only text, and **no `package.json`
  with an MIT field** is present in the export.
- The previous proprietary-vs-MIT conflict is **resolved for the export**: AGPL-3.0-only is the sole
  active software license here. (The private source repo's `aurion-command-center/package.json` MIT
  field is a separate private-repo matter and is **not** part of this export.)
- **Posture:** people may use, modify, redistribute, and commercially use Aurion under AGPL-3.0-only.
  Distributing a modified version requires sharing modified source under AGPL-3.0-only; running a
  modified network-accessible version may trigger AGPL §13's source-offer obligation. Commercial use
  under AGPL is allowed and does **not** automatically require payment.
- **No paid commercial license exists today.** One may be developed later, subject to legal review.
- **Plugin/limb licensing boundary is still under review** — the export does not promise every
  independent plugin may remain proprietary.

Content, privacy, links, and tests are clean (see scan table above).
