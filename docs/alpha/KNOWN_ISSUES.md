# Aurion Alpha — Known Issues

> **Generated from repo artifacts. Do not edit manually.**
> Regenerate with `python scripts/alpha/generate_alpha_status.py`.

**Generated:** 2026-06-23T00:33:53.495608+00:00 · Overall: **red** ·
Public alpha ready: **no**

## Public-alpha blockers

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

## Developer-alpha caveats / known issues

- Broad frontend (npm) test suite is not fully green — see artifacts/command_center/COMMAND_CENTER_BROAD_NPM_TEST_FAILURE_INVENTORY_001.md (classified pre-existing dev/lab + harness debt, not alpha-blocking).

## Non-alpha test debt

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

## What Aurion should NOT claim yet

- Aurion is **not production ready** and is **not** a finished product.
- Do **not** claim public alpha readiness while the status page says `public_alpha_ready: no`.
- Do **not** present unfinished dev/lab modules (behind Developer Mode) as alpha features.
- Missing data, refused actions, and unavailable links are shown honestly — never as fake green.

---

*Generated from real repo/test/drill/artifact evidence so alpha claims cannot drift into
fake-green marketing.*
