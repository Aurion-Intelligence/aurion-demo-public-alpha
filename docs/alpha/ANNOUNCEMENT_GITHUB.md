# Aurion Demo Public Alpha

> Reusable GitHub release / repository announcement text for Aurion's **controlled Demo Public Alpha**.
> Edit freely before posting. Nothing here is published until the operator explicitly approves it.

## What Aurion Is

Aurion is a local-first, permission-governed AI mission system.

Instead of giving an agent unrestricted power and hoping for the best, Aurion turns goals into governed
missions, checks permissions before action, records evidence and decisions, and produces a Mission
Receipt showing what happened.

The category is **AI-governed mission control** — a local-first, permission-governed second brain.

## What This Demo Includes

This Demo Public Alpha shows one governed mission spine, end to end:

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

The demonstrated path, in one line:

`Goal → Mission Plan → Permission Check → AuditLedger → Mission Receipt → Command Center`

Concretely, the bounded public spine demo (`PUBLIC-SPINE-DEMO-LOOP-001`):

- takes a bounded local goal ("check Aurion's current alpha readiness and produce a governed mission
  receipt with evidence, warnings, and next steps"),
- builds a Mission Plan with microsteps, classified as proposed-only / dry-run,
- runs PermissionGraph checks (local read allowed; external network and writes denied),
- records AuditLedger references and a BlackBox decision-trace reference,
- attaches advisory, read-only cost-governance evidence,
- produces a canonical **Mission Receipt** you can inspect in the real Command Center UI,
- shows missing data honestly as **unavailable** — never fake-green.

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
3. Run the self-contained, offline demo locally:
   ```bash
   python scripts/demo/run_public_spine_demo.py            # validate / replay (default)
   python scripts/demo/run_public_spine_demo.py --mode generate   # generate a fresh bounded receipt
   ```
4. Inspect the artifacts under [`artifacts/demo/`](../../artifacts/demo/). The runner is offline and
   uses only files in this repository — no network, no cloud models, no spend, no live autonomy.

Follow the narrated [Demo Script](DEMO_SCRIPT.md) for a guided 3–5 minute walkthrough.

## Current Limitations

See [Known Limitations (Public)](KNOWN_LIMITATIONS_PUBLIC.md) for the full list. The headlines:

- Full public alpha is **blocked by the broad frontend test suite**, which still has failures.
- Live autonomy is **not presented as complete**; unavailable controls remain visibly unavailable.
- Governance is strong on the demonstrated spine but **not yet proven universal** across all side-effect
  paths.
- Setup is rough and environment-sensitive — **no polished cross-platform installer**.
- No silent cloud escalation, no live spending, no complete provider integration claim.

## Project Status

```text
demo_public_alpha_ready: true   (ready_with_minor_caveats)
public_alpha_ready:      false
overall:                 yellow
```

The generated, evidence-derived truth lives in [`ALPHA_STATUS.md`](ALPHA_STATUS.md) and
[`KNOWN_ISSUES.md`](KNOWN_ISSUES.md).

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
