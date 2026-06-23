# Aurion Demo Public Alpha

> Reusable GitHub repository announcement text for Aurion's **Demo Public Alpha**.
> Repository: https://github.com/Aurion-Intelligence/aurion-demo-public-alpha
> Edit freely before posting. Nothing here is published until the operator explicitly approves it.

## What Aurion Is

Aurion is a local-first, permission-governed AI mission system.

Instead of giving an agent unrestricted power and hoping for the best, Aurion turns goals into governed
missions, checks permissions before action, records evidence and decisions, and produces a Mission
Receipt showing what happened.

The category is **AI-governed mission control** — a local-first, permission-governed second brain.

## What This Demo Includes

This **Demo Public Alpha** lets you run a small, **real** governed mission on Linux, macOS, or Windows —
offline, with the Python standard library only (no model, no network, no cloud). You watch which actions
are **allowed** and which are **blocked**, then inspect fresh **AuditLedger** events, **BlackBox**
decisions, and a **Mission Receipt** the run produces.

The bounded mission: *"Review the included project note, identify three action items, save the result
inside the demo workspace, and do not use the internet."* During the run:

```text
Goal → deterministic plan → microsteps → permission evaluation
     → allowed local read (only inside the bundled workspace)
     → allowed bounded write (only inside the generated-artifacts directory)
     → blocked external-network step (no network permission granted)
     → fresh AuditLedger events → fresh BlackBox decisions → fresh Mission Receipt
```

It is a **bounded** runtime: a small public implementation of the governed spine. It is **not** the full
Aurion runtime — there is no Command Center backend, live autonomy, cloud routing, or spending here.

## Why Governance Matters

Most AI systems focus on giving agents more power. Aurion focuses on **governing** that power.

A governed mission checks "should this be allowed?" before it acts, records what it decided and why,
and leaves a durable receipt. The point isn't that the agent can do more — it's that what it does is
bounded, inspectable, and auditable after the fact.

## Demo Screenshots

See the [Screenshot Gallery](SCREENSHOT_GALLERY.md). The five screenshots are deterministic
fixture-backed captures rendered through the real production-built Command Center UI using genuine demo
Mission Receipt data:

- `01-command-center-shell.png` — the Command Center cockpit
- `02-mission-receipts-list.png` — read-only Mission Receipts list
- `03-public-spine-demo-receipt-detail.png` — Mission Receipt detail
- `04-demo-governance-evidence.png` — permissions / audit / decision-trace evidence
- `05-alpha-status.png` — honest readiness status surface

## Try the Demo

1. Read the [Install Walkthrough](INSTALL_WALKTHROUGH.md).
2. Use the [Setup / Troubleshooting](SETUP_TROUBLESHOOTING.md) guide if you hit environment issues.
3. Run a **real** bounded governed mission locally (Linux/macOS/Windows, offline, no model):
   ```bash
   python3 -m aurion_demo run     # fresh governed mission (real read+write, blocked network, new receipt)
   py -m aurion_demo run          # (Windows)
   python3 -m aurion_demo replay  # validate the historical exported proof artifacts
   ```
4. Inspect a fresh run's evidence under `artifacts/demo/generated/<run-id>/` (git-ignored), or the
   historical proof under [`artifacts/demo/`](../../artifacts/demo/). Everything is offline and uses only
   files in this repository — no network, no cloud models, no spend, no live autonomy.

Follow the narrated [Demo Script](DEMO_SCRIPT.md) for a guided 3–5 minute walkthrough.

## Current Limitations

See [Known Limitations (Public)](KNOWN_LIMITATIONS_PUBLIC.md) for the full list. The headlines:

- This is the **bounded demo runtime**, not the full Aurion runtime (no Command Center backend, no live
  mission execution).
- **Full public alpha is not ready.** This package proves one governed spine, not the whole product.
- Live autonomy is **not** demonstrated; the runtime is deterministic, offline, and dry-run only.
- Governance here is a small, deliberately bounded public PermissionGraph contract — **not** the full
  private implementation, and not proof that every possible side-effect path is governed.
- No cloud routing, no live spending, no model required — and none demonstrated.

## Project Status

```text
demo_public_alpha_ready: true
public_alpha_ready:      false
repository_public:       true
announcement_published:  false
github_release_created:  false
```

The export-scoped status lives in [`DEMO_STATUS.md`](DEMO_STATUS.md).

> **Disclaimer:** This is a controlled Demo Public Alpha of Aurion's governed mission spine. It is not a
> production release, full public alpha, enterprise platform, or claim of complete unattended autonomy.

To be explicit: this is **not production-ready**, **not full public alpha**, and **not enterprise-ready**.

## License

Open source under **GNU AGPL-3.0-only** — see [`../../LICENSE`](../../LICENSE). You may use, modify,
redistribute, and commercially use Aurion under AGPL-3.0-only. AGPL is strong copyleft: distributing a
modified version requires sharing the modified source under AGPL-3.0-only, and running a modified
network-accessible version may trigger AGPL §13's source-offer obligation. Commercial use under AGPL is
allowed and does not automatically require payment. No paid commercial license exists today; an
alternative commercial license may be developed later, subject to legal review. The plugin/limb
licensing boundary is still under review. See [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md) for
contribution status.

## Feedback

This is an early, governance-first project and feedback from technical testers is welcome. Open an issue
with what you tried, what you expected, and what you saw. If something looks "fake-green," say so — honest
readiness is a design goal, not a marketing one.
