# Aurion Demo Public Alpha — Demo Script

> A short, honest, technical walkthrough for a screen recording, live walkthrough, narrated GIF/video,
> or written GitHub walkthrough of Aurion's governed mission spine.
> Tone: early, honest, technical — not hype, not enterprise-salesy, not "AI does everything."

**Release context:** controlled Demo Public Alpha. **Not production-ready. Not full public alpha. Not
live-autonomy complete.**

Target length: **3–5 minutes.**

The spine, in one line:

`Goal → Mission Plan → Permission Check → AuditLedger → Mission Receipt → Command Center`

---

## Scene 1 — What Aurion is

**Narrator:**

> "This is Aurion — a local-first, permission-governed AI mission system. Aurion is **not** being
> presented as a finished autonomous assistant. This demo shows the **governed mission spine**: how a
> goal becomes a governed mission with permissions, evidence, and a receipt. This is an early Demo Public
> Alpha — not production-ready and not a full public alpha."

**On screen:** title card or the repo README; then open the Command Center locally (note: local-first).

## Scene 2 — User goal

**Narrator:**

> "We start with one bounded goal: *check Aurion's current alpha readiness and produce a governed mission
> receipt with evidence, warnings, and next steps.* Aurion converts this goal into a Mission Plan — it
> doesn't just start acting."

**On screen:** show the Mission Control cockpit (`/mission-control`) and the demo goal.
([screenshot 01](screenshots/01-command-center-shell.png))

## Scene 3 — Mission plan and microsteps

**Narrator:**

> "Here's the interpreted goal and the bounded plan: a small number of microsteps. Notice the
> classification — this run is **proposed-only / dry-run**. Nothing here executes live side effects."

**On screen:** open Mission Receipts (read-only — no run/approve/override buttons here), then open the
Public Spine Demo receipt and show the plan / microsteps.
([screenshot 02](screenshots/02-mission-receipts-list.png) →
[screenshot 03](screenshots/03-public-spine-demo-receipt-detail.png))

## Scene 4 — Permission governance

**Narrator:**

> "Before any action, Aurion runs a permission check. The PermissionGraph allowed local reads and denied
> external network and writes for this mission. This is the *should it be allowed to?* gate — it runs
> before action. Cost governance is advisory and read-only: the decision was `allowed`, with estimates
> and stop conditions, and no real spending happened."

**On screen:** show the PermissionGraph result (allowed/denied), whether approval is required, why
execution was allowed/blocked/proposed, and the cost-governance result.

## Scene 5 — Evidence trail

**Narrator:**

> "Every governed mission leaves evidence. Here are the AuditLedger references and a BlackBox
> decision-trace reference. Where evidence is missing, it's shown honestly as **unavailable** — never
> fake-green, and never fabricated."

**On screen:** show AuditLedger refs, the BlackBox decision-trace reference (`bb_public_spine_demo_…`),
and the honestly-labelled unavailable artifact refs.
([screenshot 04](screenshots/04-demo-governance-evidence.png))

## Scene 6 — Mission Receipt

**Narrator:**

> "The Mission Receipt is the durable proof artifact — the thing you can come back to and inspect. It
> carries the mission outcome and classification, the evidence, the permission results, the
> cost-governance decision, any warnings, and the recommended next step."

**On screen:** show the Mission Receipt: outcome, classification (dry run), evidence, permissions, cost
governance, warnings, and next step.

## Scene 7 — Boundaries

**Narrator:**

> "To be clear about scope: this is a controlled Demo Public Alpha. It does **not** demonstrate
> production readiness, full live autonomy, enterprise readiness, or unattended execution. The next
> milestone toward full public alpha is greening the broad frontend test suite. The direction is
> governance-first: agents should not just act; they should leave receipts."

**On screen:** show the honest readiness status surface — overall yellow, `public_alpha_ready` false,
external models require approval, unavailable panels shown as such.
([screenshot 05](screenshots/05-alpha-status.png))

---

## Closing line (say this)

> "That's the spine. Here's what works, here's the receipt, and here's what's honestly not ready yet.
> This is a governance-first direction for AI agents — local-first, permission-governed, and auditable."

## Do NOT say

- "production-ready" / "full public alpha" / "enterprise-ready"
- "fully autonomous" / "safe unattended autonomy" / "live autonomy is complete"
- "all actions are governed" / "it does everything"
- any claim of real cloud spending or live cloud escalation being production-ready
