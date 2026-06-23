# Mission Receipt — Public Spine Demo Loop 001

- **Receipt ID:** `rcpt-demo-PUBLIC-SPINE-DEMO-LOOP-001`
- **Mission ID:** `demo-PUBLIC-SPINE-DEMO-LOOP-001`
- **Status:** `completed`
- **Risk level:** `low`
- **Created:** 2026-06-20T04:38:41.771795+00:00
- **Redaction applied:** True
- **Schema:** `mission_receipt_v1` (V1 foundation — some subsystems may be unwired)

> Read-only summary. AuditLedger + Black Box remain the source of truth; this receipt references audit/trace IDs, not raw logs.

## Receipt Classification

- Kind: demo
- Dry Run: true
- Execution Mode: dry_run

## Cost Governance

> Advisory, offline cost governance evidence. No spending occurred; no cloud call was made; no approval was granted. Required approvals describe what the governor *would* require before promotion.

- Decision: allowed
- Estimated Cost: $0.0–$0.0 (estimate; not billed), confidence: high
- Required Approvals: None recorded
- Block Reasons: None recorded
- Warnings: None recorded
- Budget Policy: max_cycles≤3, max_runtime≤15m, cloud→approval, spend→approval
- Stop Conditions: objective_reached, max_cycles_reached, max_runtime_reached, budget_exceeded

## User goal

Check Aurion's current alpha readiness and produce a governed mission receipt with evidence, warnings, and next steps.

## What Aurion understood

Run a deterministic local repo health check for Aurion's public spine: read alpha-readiness artifacts, exercise a PermissionGraph allow/deny boundary, record demo-scoped audit and decision evidence, and produce a canonical mission_receipt_…

## Plan / microsteps

- Interpret the public-spine demo goal.
- Build an advisory Mission Harness Plan and Mission Loop Plan.
- Run PermissionGraph checks for local read, external network, and TODO write.
- Read alpha readiness artifacts locally.
- Record demo-scoped AuditLedger entries.
- Write or honestly report Black Box decision trace availability.
- Generate a canonical Mission Receipt visible in Command Center.
- Propose next steps only; do not mutate TODO, approvals, workers, or live autonomy.

## Tools / models / plugins

- MissionHarnessPlan advisory planner
- MissionLoopPlan advisory planner
- PermissionGraph.check_fs
- PermissionGraph.check_net
- AuditLedger.append (demo-scoped JSONL)
- BlackBoxDecisionTrace writer (demo-scoped, when available)
- MissionReceiptBuilder
- local file read (no model call)
- local model routing not called

## Permission checks

fs.read docs/alpha/DEMO_STATUS.md -> allowed (allowed); net.request https://example.com -> denied (net_denied_no_allowlist); fs.write TODO.md -> denied (fs_write_denied)

## Mission Harness Plan

**Job Type:** reviewer
**Risk Level:** low
**Advisory Only:** yes
**Permission Scope:** read_only
**External Access Policy:** local_only
**Model Role:** reviewer

> This harness plan is advisory. It describes the intended mission boundary but does not enforce permissions by itself.

### Allowed Tools / Categories
- local_read
- source_extraction

### Blocked Tools / Categories
- spending
- account_actions
- account_login
- destructive_filesystem
- email_sending
- shell_write_actions
- purchase
- form_submit

### Memory Scope
- allowed: local_rag
- allowed: source_of_truth_read
- blocked: user_private_credentials

### Proof Requirements
- file_refs
- audit_refs
- mission_receipt

### Approval Checkpoints
_(none)_

### Minimality Rationale
Reviewer work is read-only over local context; it needs no external access, spending, or write permissions.

### Warnings / Missing Information
_(none)_

## Approvals requested

_(none recorded)_

## Approvals granted

_(none recorded)_

## Approvals denied

_(none recorded)_

## Sandbox / eval / alignment

local_demo_completed; permission_boundary_checked; no live autonomy, no cloud, no spending

## Actions executed

- Read docs/alpha/DEMO_STATUS.md (3065 bytes)
- Read docs/alpha/DEMO_STATUS.md (1780 bytes)
- Read artifacts/architecture_review/ARCHITECTURE_REVIEW_COMPLETION_AUDIT_001.md (12000 bytes)
- Built advisory harness and loop plans.
- Recorded demo-scoped AuditLedger events.
- Generated canonical mission_receipt_v1 artifact.

## Actions blocked or refused

- External network request denied by PermissionGraph (not attempted).
- TODO.md write denied by PermissionGraph (proposed-only; not attempted).
- Live autonomy controls intentionally not invoked.

## Memory updates

_(none recorded)_

## Proposed memory updates (write-back: not_attempted)

- [decision] Public spine demo loop exists and remains read-only/proposed-only. (conf: high)

## Warnings

- This demo does not prove production readiness.
- This demo does not make public_alpha_ready true by itself.
- Live autonomy controls are intentionally outside this proof loop.
- Install walkthrough and screenshots remain separate public-alpha gates.

## Failures

_(none recorded)_

## Audit References

| Time | Event Type | Action | Outcome | Ref |
|---|---|---|---|---|
| 2026-06-20T04:38:41.758981+00:00 | mission.plan.created | mission.plan.created | completed | `audit:audit_public_spine_demo_001_20260620_043841_mission_planned` |
| 2026-06-20T04:38:41.759081+00:00 | permission.fs.read | permission.fs.read | allowed | `audit:audit_public_spine_demo_001_20260620_043841_permission_1` |
| 2026-06-20T04:38:41.759152+00:00 | permission.net.request | permission.net.request | denied | `audit:audit_public_spine_demo_001_20260620_043841_permission_2` |
| 2026-06-20T04:38:41.759244+00:00 | permission.fs.write | permission.fs.write | denied | `audit:audit_public_spine_demo_001_20260620_043841_permission_3` |
| 2026-06-20T04:38:41.759309+00:00 | artifact.local_read.completed | artifact.local_read.completed | completed | `audit:audit_public_spine_demo_001_20260620_043841_local_read` |
| 2026-06-20T04:38:41.759371+00:00 | mission_receipt.generated | mission_receipt.generated | completed | `audit:audit_public_spine_demo_001_20260620_043841_receipt_generated` |

## Audit event references

- audit_public_spine_demo_001_20260620_043841_mission_planned
- audit_public_spine_demo_001_20260620_043841_permission_1
- audit_public_spine_demo_001_20260620_043841_permission_2
- audit_public_spine_demo_001_20260620_043841_permission_3
- audit_public_spine_demo_001_20260620_043841_local_read
- audit_public_spine_demo_001_20260620_043841_receipt_generated

## Black Box References

| Time | Component | Decision Type | Model Role | Outcome | Ref |
|---|---|---|---|---|---|
| 2026-06-20T04:38:41.761311+00:00 | scripts/demo/public_spine_demo_loop_001.py | policy | not_called_deterministic_script | read alpha status locally; deny external network and TODO write | `blackbox:bb_public_spine_demo_001_20260620_043841_permission_boundary` |

## Black Box trace references

- bb_public_spine_demo_001_20260620_043841_permission_boundary

## Working Memory references

- chat:public-spine-demo-loop-001

## Recommended next steps

- Capture alpha screenshots after the demo receipt is visible.
- Write a clean install/run walkthrough for public alpha.
- Keep live autonomy controls unavailable until the route/conductor contract is repaired.

## Source completeness (wired vs missing)

- wired: mission_metadata
- wired: microsteps
- wired: permission_checks
- wired: sandbox_eval
- wired: actions
- wired: audit_refs
- wired: blackbox_refs
- wired: working_memory_refs
- wired: memory_candidates
- wired: harness_plan
- missing: approval_events

## Missing data (honest gaps)

- No live autonomy execution result collected; this demo intentionally uses verified read-only/proposed-only paths.
- External network data not collected; PermissionGraph denied network access.
- source not wired: approval_events

