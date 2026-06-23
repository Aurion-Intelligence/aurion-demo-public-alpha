# Aurion

Aurion is a local-first governed AI mission system.

Aurion turns user goals into governed AI missions. The project category is
AI-governed mission control: early, local-first software for turning an intent
into a plan, checking permissions, taking only bounded safe actions, and leaving
a receipt that a human can inspect.

This repository is not a finished launch package. It currently presents a
truthful Demo Public Alpha surface around one verified public spine.

## What Aurion Is

Aurion is a mission-control project for AI work that should be understandable
after the fact. A mission starts with a user goal, becomes explicit microsteps,
passes through governance checks, and produces a Mission Receipt instead of a
bare "done" message.

The current public story is intentionally narrow:

- local-first by default, with local model routing as the preferred path
- governance-first, with permission and approval concepts at the center
- human-inspectable, through Mission Receipts, AuditLedger refs, Decision Trace
  refs, and Command Center status views
- early developer-alpha software, not production-ready and not a full public
  alpha release yet

## The Core Idea

```text
Mission -> Permission -> Execution/Proposal -> Receipt -> Memory Update
```

In the bounded demo, this means:

1. A user goal is translated into a mission plan.
2. Microsteps describe what Aurion thinks it should do.
3. PermissionGraph / ToolDispatcher checks decide what is allowed, denied, or
   proposed-only.
4. Safe local actions may run; unsafe or unavailable actions stay proposed,
   denied, skipped, or uncollected.
5. AuditLedger and BlackBox evidence are attached when available.
6. A Mission Receipt summarizes the result for review in Command Center.

## Demo Public Alpha Status

Aurion is not production-ready and is not a full public alpha release yet.

This repository currently exposes a bounded Demo Public Alpha package focused
on one thing:

```text
Goal -> Mission Plan -> Permission Check -> AuditLedger -> Mission Receipt -> Command Center
```

The purpose is to show Aurion's governed mission spine, not to claim broad
autonomous capability. This package's status — what it can and cannot do — is in
[`docs/alpha/DEMO_STATUS.md`](docs/alpha/DEMO_STATUS.md). The full-project
readiness matrix is private and not published here.

## Run a real bounded governed mission

This package includes a small, real, cross-platform governed-mission runtime. One command executes a
**fresh** bounded mission and produces new evidence:

```text
Goal → deterministic plan → microsteps → permission evaluation
     → allowed local read → allowed bounded artifact write
     → blocked external-network step
     → fresh AuditLedger events → fresh BlackBox decisions → fresh Mission Receipt
```

Run it (offline, no network, no cloud, no model, no private modules):

| Platform | Command |
|---|---|
| Linux / macOS | `python3 -m aurion_demo run` |
| Windows | `py -m aurion_demo run` |
| Any (script fallback) | `python scripts/demo/run_governed_mission.py` |

The bundled mission: *"Review the included project note, identify three action items, save the result
inside the demo workspace, and do not use the internet."* It reads only the included sample note, writes
only inside the generated-artifacts directory, and the external-research step is **blocked** because no
network permission is granted. Generated files live under `artifacts/demo/generated/` and are
git-ignored (each run is a fresh, real execution — not a replay).

### `run` vs `replay`

- **`run`** — executes a fresh miniature governed mission (real read + write + blocked network + new
  AuditLedger / BlackBox / Mission Receipt).
- **`replay`** (`python3 -m aurion_demo replay`) — validates the historical exported proof artifacts
  ([`PUBLIC_SPINE_DEMO_LOOP_001`](artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.md)) without executing a new
  mission. The standalone replay runner is `python scripts/demo/run_public_spine_demo.py`.
- **Optional model integration** — *not included yet.* The runtime is fully deterministic and offline.

## What Works Today

These areas are implemented in bounded or developer-alpha form:

- Mission Receipts and the read-only Mission Receipts Command Center surface
- the public spine demo described above
- the developer install walkthrough:
  [`docs/alpha/INSTALL_WALKTHROUGH.md`](docs/alpha/INSTALL_WALKTHROUGH.md)
- setup troubleshooting:
  [`docs/alpha/SETUP_TROUBLESHOOTING.md`](docs/alpha/SETUP_TROUBLESHOOTING.md)
- Command Center shell and alpha surfaces for status, missions, receipts, and
  approvals
- ApprovalGate proposal-detail and inbox concepts in the developer-alpha system
- AuditLedger references in receipt and demo-scoped evidence paths
- BlackBox / Decision Trace references when demo-scoped traces are available
- bounded PermissionGraph / ToolDispatcher checks, including explicit deny cases
- local-first model routing in partial developer form

## What Is Not Ready Yet

Aurion should not be read as a completed agent platform. The following are not
ready for public trust or broad use:

- full public alpha
- production use
- unattended live autonomy
- universal side-effect governance
- complete live Foreman/autonomy route path
- autonomous agent-spawning (not in the public demo)
- background watcher/scheduler loops beyond a minimal seed
- real spending adapters
- enterprise platform claims
- general cloud escalation safety
- claims that every tool or action is governed

What this package can and cannot do is described in
[`docs/alpha/DEMO_STATUS.md`](docs/alpha/DEMO_STATUS.md), and public limitations in
[`docs/alpha/KNOWN_LIMITATIONS_PUBLIC.md`](docs/alpha/KNOWN_LIMITATIONS_PUBLIC.md).

## Screenshots

The Demo Public Alpha screenshot proof pack is registered by manifest:

- [`docs/alpha/screenshots/manifest.json`](docs/alpha/screenshots/manifest.json)

These are fixture-backed demo screenshots for the public spine narrative, not a
full-stack production proof and not a full public-alpha launch claim.

## Public Demo Materials

Public-facing Demo Public Alpha presentation pack (controlled demo narrative, not a
public release; not production-ready and not full public alpha). Start at the publish
pack — it is the canonical operator hub and links the rest:

- [`docs/alpha/PUBLISH_PACK.md`](docs/alpha/PUBLISH_PACK.md) — canonical operator hub
- [`docs/alpha/ANNOUNCEMENT_GITHUB.md`](docs/alpha/ANNOUNCEMENT_GITHUB.md) — canonical release announcement
- [`docs/alpha/ANNOUNCEMENT_SOCIAL.md`](docs/alpha/ANNOUNCEMENT_SOCIAL.md) — canonical social copy
- [`docs/alpha/DEMO_SCRIPT.md`](docs/alpha/DEMO_SCRIPT.md)
- [`docs/alpha/SCREENSHOT_GALLERY.md`](docs/alpha/SCREENSHOT_GALLERY.md)
- [`docs/alpha/KNOWN_LIMITATIONS_PUBLIC.md`](docs/alpha/KNOWN_LIMITATIONS_PUBLIC.md)
- [`docs/alpha/FAQ_DEMO_PUBLIC_ALPHA.md`](docs/alpha/FAQ_DEMO_PUBLIC_ALPHA.md) — supplemental
- [`docs/alpha/ANNOUNCEMENT_DRAFT.md`](docs/alpha/ANNOUNCEMENT_DRAFT.md) — deprecated (superseded by the announcements above)

## Quick Start

Start with the alpha walkthrough:

1. Read [`docs/alpha/INSTALL_WALKTHROUGH.md`](docs/alpha/INSTALL_WALKTHROUGH.md).
2. Use [`docs/alpha/SETUP_TROUBLESHOOTING.md`](docs/alpha/SETUP_TROUBLESHOOTING.md)
   if setup fails.
3. Run the backend and Command Center as described in the walkthrough.
4. Open Command Center and inspect `/mission-receipts`.
5. Run the public spine demo if you want a fresh receipt.

## Run / Inspect the Demo

```bash
python3 -m aurion_demo run        # fresh bounded governed mission (real run)
python3 -m aurion_demo replay     # validate the historical exported proof artifacts
```

Then inspect:

- a fresh run's evidence under `artifacts/demo/generated/<run-id>/` (audit.jsonl, blackbox/,
  mission_receipt.json) — git-ignored
- the historical proof report:
  [`artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.md`](artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.md)
  and data [`artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.json`](artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.json)
- this package's status:
  [`docs/alpha/DEMO_STATUS.md`](docs/alpha/DEMO_STATUS.md)

## Architecture

The public-facing architecture should be understood as a governed mission spine,
not as an all-purpose AI operating system:

- mission planning and microsteps
- permission checks and approval boundaries
- safe local execution or proposed-only outputs
- AuditLedger and Decision Trace references
- Mission Receipts
- Command Center read-only inspection surfaces
- memory handoff/update paths after verified work

Some older modules and developer labs still exist in the repository. They are
not automatically part of the Demo Public Alpha surface.

## Governance Model

Aurion's governance model is intentionally layered:

- PermissionGraph / ToolDispatcher checks for bounded tool decisions
- ApprovalGate for human review before sensitive changes
- AuditLedger for event references
- BlackBox / Decision Trace refs for demo-scoped decision evidence
- Mission Receipts for the human-readable summary

This is not universal yet. The demo proves a governed path, not every path.

## Mission Receipts

A Mission Receipt is the public proof object for a governed mission. It should
show what Aurion understood, planned, completed, refused, skipped, or could not
collect. Missing evidence should appear as missing or unavailable, never as fake
green.

The current demo receipt is visible through the Mission Receipts loader and the
Command Center read-only receipt view.

## Local-First, Not Local-Only

Aurion is designed to work from a local-first posture: local repo, local
artifacts, local Command Center, and local model routing where possible.

That does not mean the project will never use external services. It means
external model calls, cloud escalation, network actions, spending, posting, and
account-affecting work must stay inside explicit governance boundaries before
they can be trusted.

## Safety / Trust Boundaries

The Demo Public Alpha package is safe to describe as a bounded governance demo.
It should not be described as safe unattended autonomy.

Trust boundaries to keep visible:

- No public-alpha readiness claim while generated status says no.
- No production claim.
- No broad live-autonomy claim.
- No universal governance claim.
- No spending, posting, browser, cloud, or account action claim unless a future
  receipt-backed lane verifies it.
- No protected private configuration, secrets, or personal paths should be
  published.

## Roadmap

Near-term public-demo hardening:

- keep the screenshot proof pack and manifest current
- keep install and troubleshooting docs honest
- improve receipt source linking from summaries to safe detail views
- surface generated alpha status inside Command Center
- continue reducing broad frontend test debt
- keep expanding governed tool/action coverage through receipt-backed lanes

## Contributing

The best contributions are narrow and evidence-backed:

- Command Center polish for alpha surfaces
- Mission Receipt source-linking and safe detail views
- setup and install documentation
- tests that prevent fake-green claims
- local-first model routing hardening
- governed browser/tool-action design that stays human-in-the-loop

Before making changes, read [`CONTRIBUTING.md`](CONTRIBUTING.md) and
[`docs/alpha/DEMO_STATUS.md`](docs/alpha/DEMO_STATUS.md) to understand what this bounded package does
and does not include.

## License / Project Status

**Aurion Demo Public Alpha is open source under [GNU AGPL-3.0-only](LICENSE) (`AGPL-3.0-only`).**

You may **use, modify, redistribute, and commercially use** Aurion under the terms of AGPL-3.0-only.
Modularity and community-built limbs/plugins are part of the project's purpose.

What AGPL-3.0-only means in practice:

- **Strong copyleft.** If you distribute a modified version of Aurion, you must make your modified
  source available under AGPL-3.0-only.
- **Network use (§13).** If you run a **modified** version that users interact with over a network, you
  must offer those users the corresponding modified source. Running an **unmodified** copy as a service
  does not by itself trigger a new source-offer obligation beyond providing the existing source.
- **Commercial use is allowed** under AGPL — using Aurion commercially does **not** automatically mean
  you owe anyone payment, as long as you comply with AGPL.
- **No paid commercial license exists today.** Alternative commercial licensing (for organizations that
  prefer not to comply with AGPL obligations) **may be developed later, subject to legal review**. It is
  not offered now, and nothing here should be read as such an offer.

**Plugins / limbs:** the licensing boundary for plugins/limbs is **still under review**. We do **not**
promise that every independent plugin may remain proprietary — whether a plugin is a derivative work
under AGPL is fact-specific and not yet settled for Aurion.

This repository contains the bounded Demo Public Alpha package only. Advanced governance policies,
evaluation sets, premium templates, spending adapters, cloud escalation logic, and personal/private
configuration are **not** part of this public package and are kept in a separate private repository.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to give feedback (welcome now) and the status of code
contributions (paused pending a contributor-rights process).

## Status Disclaimer

Aurion is early. Aurion is local-first and governed. Aurion's current public
proof is a bounded demo spine with Mission Receipts and governance surfaces.
Aurion is not production-ready, not full public alpha, and not live-autonomy complete.
