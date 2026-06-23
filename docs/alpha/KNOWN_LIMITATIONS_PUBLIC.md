# Aurion Demo Public Alpha — Known Limitations (Public)

> Public-safe limitations for Aurion's **controlled Demo Public Alpha**. This document is intentionally
> honest. Aurion is **not production-ready**, **not a full public alpha**, and **not enterprise-ready**.
> The export-scoped status lives in [`DEMO_STATUS.md`](DEMO_STATUS.md).

Canonical status:

```text
demo_public_alpha_ready: true   (ready_with_minor_caveats)
public_alpha_ready:      false
overall:                 yellow
full-public-alpha blocker: broad_frontend_tests = fail
```

---

## Release maturity

- This is a **Demo Public Alpha**, not a full public alpha. Do not read it as "Public Alpha."
- It is **developer-oriented**: aimed at developers, local-first builders, and early technical testers,
  not at general consumers expecting a polished installer.
- Setup is **rough** and assumes comfort with a terminal, Python, and Node tooling.
- The supported path is **limited** — one bounded, governed mission spine, not the whole product.

## Autonomy

- The **live autonomy** route is **not currently presented as complete**.
- Controls that are not ready remain **visibly unavailable** in the UI — they are not faked green.
- There is **no claim of safe unattended autonomy**. The demo is a dry run, not live execution.

## Frontend

- The **broad frontend test suite still has failures**.
- These failures **block full public-alpha readiness** — this is the current gating issue.
- The **bounded demo surfaces pass their focused tests**; the failures are in wider lab/dev modules
  that are not part of the Demo Public Alpha surface.

## Governance scope

- Governance is **strong on the demonstrated spine**: plan → permission check → audit → receipt.
- It is **not yet proven universal** across every possible side-effect path.
- **Recovery mutations and broader routes still require audit** before any universal-governance claim.

## Platform support

- The **installation path may be environment-sensitive** (OS, Python/Node versions, build tooling).
- There is **no polished cross-platform installer** claim. Expect manual setup steps.

## External tools

- There is **no claim of complete cloud / provider integration**.
- There is **no silent cloud escalation** — external models require explicit approval.
- **No live spending is demonstrated**. Cost governance shown in the demo is advisory and read-only.

## Enterprise

- The architecture is **relevant to enterprise governance** concerns (permissions, audit, receipts).
- This release is **not enterprise-ready or certified**, and makes no compliance claims.

---

## What this release is honestly *not*

- not production-ready
- not a full public alpha
- not enterprise-ready
- not a proof of complete unattended autonomy
- not a claim that every side effect is universally governed
- not a claim of complete cloud / tool / provider support

## Where the machine-checked truth lives

- [`DEMO_STATUS.md`](DEMO_STATUS.md) — export-scoped status (what this package can and cannot do).
- [`../../artifacts/alpha/alpha_status.json`](../../artifacts/alpha/alpha_status.json) — machine status.
