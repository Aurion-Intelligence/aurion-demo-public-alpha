# Public Spine Demo Loop - 001

## Goal

Check Aurion's current alpha readiness and produce a governed mission receipt with evidence, warnings, and next steps.

## What This Demo Proves

- Aurion can show one deterministic governed proof loop using verified local islands.
- The loop includes plan, microsteps, PermissionGraph checks, AuditLedger refs, Black Box refs when available, and a canonical Mission Receipt.
- The generated receipt is visible through the existing Mission Receipts loader and Command Center surface.

## What This Demo Does Not Prove

- It does not prove live autonomous mission execution.
- It does not prove worker spawning, background watcher loops, agent spawning, spending, cloud escalation, or production readiness.
- It does not make public_alpha_ready true; install walkthrough and screenshots remain required.

## Spine Walkthrough

| Stage | Evidence |
| --- | --- |
| User goal | `scenario.user_goal` |
| Mission plan | `MissionHarnessPlan + MissionLoopPlan advisory planners` |
| Microsteps | `receipt.microsteps_summary` |
| Permission check | `PermissionGraph fs.read allowed; net.request and fs.write denied` |
| Safe action | `local alpha artifacts read` |
| Proposed-only action | `next recommendations and memory candidate not written` |
| AuditLedger | `artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.audit.jsonl` |
| Black Box | `artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.blackbox/decisions/2026-06-20/bb_public_spine_demo_001_20260620_154730_permission_boundary.json` |
| Mission Receipt | `{'json': 'artifacts/mission_receipts/20260620_154731_demo-PUBLIC-SPINE-DEMO-LOOP-001.json', 'markdown': 'artifacts/mission_receipts/20260620_154731_demo-PUBLIC-SPINE-DEMO-LOOP-001.md'}` |
| Command Center | `/mission-receipts read-only view` |

## Artifacts Produced

- Scenario: `artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.scenario.json`
- Demo JSON: `artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.json`
- Demo Markdown: `artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.md`
- AuditLedger JSONL: `artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.audit.jsonl`
- Black Box trace: `artifacts/demo/PUBLIC_SPINE_DEMO_LOOP_001.blackbox/decisions/2026-06-20/bb_public_spine_demo_001_20260620_154730_permission_boundary.json`
- Receipt JSON: `artifacts/mission_receipts/20260620_154731_demo-PUBLIC-SPINE-DEMO-LOOP-001.json`
- Receipt Markdown: `artifacts/mission_receipts/20260620_154731_demo-PUBLIC-SPINE-DEMO-LOOP-001.md`

## Receipt Link / ID

- Receipt ID: `rcpt-demo-PUBLIC-SPINE-DEMO-LOOP-001`
- Mission ID: `demo-PUBLIC-SPINE-DEMO-LOOP-001`
- Command Center route: `/mission-receipts`
- API detail: `/api/mission-receipts/rcpt-demo-PUBLIC-SPINE-DEMO-LOOP-001`

## Audit / BlackBox Evidence

- Audit refs: `6`
- Black Box refs: `1`

## Permission Checks

| Capability | Target | Result | Reason |
| --- | --- | --- | --- |
| `fs.read` | `docs/alpha/DEMO_STATUS.md` | allowed | `allowed` |
| `net.request` | `https://example.com` | denied | `net_denied_no_allowlist` |
| `fs.write` | `TODO.md` | denied | `fs_write_denied` |

## Known Limitations

- Deterministic script, not live autonomous execution.
- No network data collected; denied by PermissionGraph.
- No TODO, approval, worker, or autonomy mutation.
- Command Center visibility uses the existing Mission Receipts view; no new run/approval controls were added.

## How To Re-run (public export — offline, self-contained)

```bash
python scripts/demo/run_public_spine_demo.py                 # validate / replay
python scripts/demo/run_public_spine_demo.py --mode generate # generate a fresh bounded receipt
```

> The original private run used `scripts/demo/public_spine_demo_loop_001.py`, which is **not** part of
> this public package. The evidence above is shipped fixture-backed; the public runner replays it.

## Validation

- python -m pytest tests/test_public_spine_demo_runner_001.py --tb=short -q
- python -m pytest tests/ --tb=short -q
