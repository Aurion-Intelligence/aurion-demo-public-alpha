# Aurion Alpha Status

> **Generated from repo artifacts. Do not edit manually.**
> Regenerate with `python scripts/alpha/generate_alpha_status.py`.

**Generated:** 2026-06-23T00:33:53.495608+00:00

## Overall status

# 🔴 RED

Demo public alpha package is ready (bounded, fixture-backed proof pack); FULL public alpha is NOT ready (see blockers).

## Readiness

- **Public alpha ready:** **no**
- **Demo public alpha ready:** **yes** _(bounded, fixture-backed proof pack — not full release)_
- **Developer alpha ready:** **no**

## Gates

| Gate | Status | Detail / reason |
|---|---|---|
| Memory fragmentation mapped | ❓ unknown | Memory map not found: artifacts/architecture/memory_fragmentation_map_001.json |
| Agents memory index generated | ❓ unknown | agents_memory INDEX.md / latest.json not generated. |
| Public spine demo loop | ✅ pass | receipt_id=rcpt-demo-PUBLIC-SPINE-DEMO-LOOP-001; public_alpha_ready_claimed=false |
| Sandbox Longrun full-safe | ❓ unknown | No full-safe run summary found. |
| Governed mission drills | ❓ unknown | Evidence artifact not found: artifacts/alpha/ALPHA_GOVERNED_MISSION_DRILL_001.md |
| Governed TODO-write approval drill | ❓ unknown | Evidence artifact not found: artifacts/alpha/GOVERNED_TODO_WRITE_APPROVAL_LIVE_DRILL_001.md |
| Mission Receipt correlation | ❓ unknown | TODO [mission-receipt-correlation-hardening-001] not marked complete. |
| Mission Receipt coverage | ❓ unknown | Evidence artifact not found: artifacts/mission_receipts/RECEIPT_COVERAGE_GATE_001.json |
| Mission Receipt source links | ❓ unknown | TODO [mission-receipt-source-linking-001] not marked complete. |
| ApprovalGate proposal detail API | ❓ unknown | TODO [approvalgate-proposal-detail-api-001] not marked complete. |
| Unified mission query API | ❓ unknown | TODO [mission-list-unified-query-001] not marked complete. |
| Mission Control unified UI | ❓ unknown | TODO [mission-control-unified-ui-001] not marked complete. |
| Route contracts | ❓ unknown | Evidence artifact not found: artifacts/routes/ROUTE_CONTRACT_APP_CEILING_REALITY_CHECK_001_after.txt |
| Command Center build | ❓ unknown | No full-safe run. |
| Command Center typecheck | ❓ unknown | No full-safe run. |
| Broad frontend tests | ❓ unknown | Evidence artifact not found: artifacts/command_center/COMMAND_CENTER_BROAD_NPM_TEST_FAILURE_INVENTORY_001.md |
| Install walkthrough | ✅ pass |  |
| Alpha screenshots | ✅ pass |  |

## Latest full-safe run

_no full-safe run found_

## Latest mission drill receipts

_(none)_

## Known blockers (public alpha)

- Sandbox Longrun full-safe: No full-safe run summary found.
- Governed mission drills: Evidence artifact not found: artifacts/alpha/ALPHA_GOVERNED_MISSION_DRILL_001.md
- Governed TODO-write approval drill: Evidence artifact not found: artifacts/alpha/GOVERNED_TODO_WRITE_APPROVAL_LIVE_DRILL_001.md
- Mission Receipt correlation: TODO [mission-receipt-correlation-hardening-001] not marked complete.
- Mission Receipt coverage: Evidence artifact not found: artifacts/mission_receipts/RECEIPT_COVERAGE_GATE_001.json
- Mission Receipt source links: TODO [mission-receipt-source-linking-001] not marked complete.
- ApprovalGate proposal detail API: TODO [approvalgate-proposal-detail-api-001] not marked complete.
- Unified mission query API: TODO [mission-list-unified-query-001] not marked complete.
- Mission Control unified UI: TODO [mission-control-unified-ui-001] not marked complete.
- Route contracts: Evidence artifact not found: artifacts/routes/ROUTE_CONTRACT_APP_CEILING_REALITY_CHECK_001_after.txt
- Command Center build: No full-safe run.
- Command Center typecheck: No full-safe run.
- Broad frontend tests: Evidence artifact not found: artifacts/command_center/COMMAND_CENTER_BROAD_NPM_TEST_FAILURE_INVENTORY_001.md

## Non-blocking debt

- Broad frontend (npm) test suite is not fully green — see artifacts/command_center/COMMAND_CENTER_BROAD_NPM_TEST_FAILURE_INVENTORY_001.md (classified pre-existing dev/lab + harness debt, not alpha-blocking).

## Staleness warnings

- Gate 'full_safe' is unknown: No full-safe run summary found..
- Gate 'governed_mission_drills' is unknown: Evidence artifact not found: artifacts/alpha/ALPHA_GOVERNED_MISSION_DRILL_001.md.
- Gate 'governed_write_drill' is unknown: Evidence artifact not found: artifacts/alpha/GOVERNED_TODO_WRITE_APPROVAL_LIVE_DRILL_001.md.
- Gate 'mission_receipt_correlation' is unknown: TODO [mission-receipt-correlation-hardening-001] not marked complete..
- Gate 'receipt_coverage' is unknown: Evidence artifact not found: artifacts/mission_receipts/RECEIPT_COVERAGE_GATE_001.json.
- Gate 'mission_source_links' is unknown: TODO [mission-receipt-source-linking-001] not marked complete..
- Gate 'approvalgate_detail_api' is unknown: TODO [approvalgate-proposal-detail-api-001] not marked complete..
- Gate 'unified_mission_query' is unknown: TODO [mission-list-unified-query-001] not marked complete..
- Gate 'mission_control_unified_ui' is unknown: TODO [mission-control-unified-ui-001] not marked complete..
- Gate 'route_contracts' is unknown: Evidence artifact not found: artifacts/routes/ROUTE_CONTRACT_APP_CEILING_REALITY_CHECK_001_after.txt.
- Gate 'command_center_build' is unknown: No full-safe run..
- Gate 'command_center_typecheck' is unknown: No full-safe run..
- Gate 'broad_frontend_tests' is unknown: Evidence artifact not found: artifacts/command_center/COMMAND_CENTER_BROAD_NPM_TEST_FAILURE_INVENTORY_001.md.

## Evidence TODO refs

- mission-receipt-correlation-hardening-001
- mission-list-unified-query-001
- mission-control-unified-ui-001
- alpha-governed-mission-drill-001
- governed-todo-write-approval-live-drill-001
- public-spine-demo-loop-001
- receipt-coverage-gate-001
- command-center-broad-npm-test-failure-inventory-001

---

*This page is the source of truth for Aurion's alpha readiness. Public alpha must not be claimed
while `public_alpha_ready` is `no`. See [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md).*
