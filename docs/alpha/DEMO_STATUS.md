# Aurion Demo Public Alpha — Status

> Status for **this exported Demo Public Alpha package only.** This is a bounded technical proof
> package — not the full Aurion runtime, and not a readiness report for the whole project.

## Summary

```text
demo_public_alpha_ready: true     # this bounded demo package is ready
public_alpha_ready:      false    # full public alpha is NOT ready
publication_executed:    false
license:                 AGPL-3.0-only
```

- **The Demo Public Alpha package is ready** — bounded, offline, fixture-backed, and self-contained.
- **Full Public Alpha is not ready.**
- **The full Aurion runtime is not included** in this repository.
- This is a **bounded technical proof package**: it demonstrates one governed mission spine through
  shipped evidence and a small offline runner. It is not a finished product.

## What this package verifiably contains

These are the only things this repository attests to — each is present and checkable here:

| Capability | Status | How to check |
|---|---|---|
| **Real bounded governed-mission runtime** | works | `python3 -m aurion_demo run` (`py -m aurion_demo run` on Windows) |
| Fresh AuditLedger / BlackBox / Mission Receipt per run | works | `artifacts/demo/generated/<run-id>/` after a run |
| Blocked external-network step | enforced | the `net.request` step is denied (`NETWORK_NOT_PERMITTED`) |
| Replay of historical proof artifacts | works | `python3 -m aurion_demo replay` |
| Exported AuditLedger evidence (historical) | present (fixture-backed) | `artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.audit.jsonl` |
| Exported BlackBox decision traces (historical) | present (4 traces) | `artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.blackbox/` |
| Screenshots | 5 present | `docs/alpha/screenshots/` (+ `manifest.json`) |
| Installation / demo instructions | present | [`INSTALL_WALKTHROUGH.md`](INSTALL_WALKTHROUGH.md), [`SETUP_TROUBLESHOOTING.md`](SETUP_TROUBLESHOOTING.md) |
| Cross-platform CI (Linux/Windows/macOS) | configured | `.github/workflows/ci.yml` runs the mission + tests, no secrets |
| License | AGPL-3.0-only | [`../../LICENSE`](../../LICENSE) |
| Privacy / secret scan | clean | no secrets, credentials, personal paths, or private-repo references |
| Exported tests | pass | `python -m pytest tests/` |

**`run` vs `replay`:**

- **`run`** executes a *fresh* miniature governed mission: it reads only the bundled sample note, writes
  only inside the generated-artifacts directory, blocks the external-network step, and emits **new**
  AuditLedger events, BlackBox decisions, and a Mission Receipt under `artifacts/demo/generated/`
  (git-ignored). This is a real execution, not a replay.
- **`replay`** validates the *historical* exported proof artifacts (`PUBLIC_SPINE_DEMO_LOOP_001`), whose
  AuditLedger/BlackBox evidence is real and shipped fixture-backed. Nothing is fabricated.
- **Optional model integration is not included yet** — the runtime is deterministic and offline.

## What you CAN do with this release

- **Run a real bounded governed mission** with one command (`python3 -m aurion_demo run`) on Linux,
  macOS, or Windows — it produces a fresh Mission Receipt plus new AuditLedger and BlackBox evidence.
- Replay/validate the historical exported proof artifacts (`python3 -m aurion_demo replay`).
- Inspect the exported AuditLedger and BlackBox decision-trace evidence.
- View the Command Center screenshots and read the demo walkthrough.
- Read, run, modify, redistribute, and commercially use the code under **AGPL-3.0-only**
  (see [`../../LICENSE`](../../LICENSE) and [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md)).
- Run the exported test suite to verify the package locally.

## What you CANNOT do with this release

- Run the full Aurion runtime, Command Center backend, or live mission execution — **not included**.
- Treat this as a full public alpha, a production release, or an enterprise-ready system — it is none of
  these.
- Rely on live autonomy, cloud model routing, real spending, or unattended operation — **not included**
  and **not demonstrated**.
- Reproduce the original private mission loop end-to-end — the loop's full source and the broader
  project live in a **separate private repository** that is not part of this export.

## Honest boundaries

See [`KNOWN_LIMITATIONS_PUBLIC.md`](KNOWN_LIMITATIONS_PUBLIC.md) for the public limitations list. The
broader full-project readiness matrix is intentionally **not** published here — it describes private
work that is not part of this bounded demo package.
