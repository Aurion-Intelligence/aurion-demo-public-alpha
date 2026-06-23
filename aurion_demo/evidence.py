"""
Evidence writers — AuditLedger (JSONL) and BlackBox (decision records).

Every governed run produces fresh, append-only evidence. Records carry a unique run_id and ISO-8601
UTC timestamps. Paths in evidence are repo-relative POSIX (never absolute/local). No network, no
private imports.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class AuditLedger:
    """Append-only JSONL audit ledger for a single run."""

    def __init__(self, path: Path, run_id: str) -> None:
        self.path = Path(path)
        self.run_id = run_id
        self.events: list[dict] = []
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, event_type: str, outcome: str, summary: str, **extra: object) -> str:
        seq = len(self.events) + 1
        event_id = f"audit_{self.run_id}_{seq:03d}"
        event = {
            "audit_event_id": event_id,
            "run_id": self.run_id,
            "seq": seq,
            "event_type": event_type,
            "outcome": outcome,
            "summary": summary,
            "created_at": utc_now_iso(),
            "redaction_applied": True,
            **extra,
        }
        self.events.append(event)
        return event_id

    def flush(self) -> None:
        with self.path.open("w", encoding="utf-8", newline="\n") as fh:
            for ev in self.events:
                fh.write(json.dumps(ev, sort_keys=True) + "\n")

    @property
    def event_ids(self) -> list[str]:
        return [e["audit_event_id"] for e in self.events]


class BlackBox:
    """Decision-trace writer: one JSON record per governed decision in a run."""

    def __init__(self, directory: Path, run_id: str) -> None:
        self.dir = Path(directory)
        self.run_id = run_id
        self.records: list[dict] = []
        self.dir.mkdir(parents=True, exist_ok=True)

    def record(self, decision_type: str, outcome: str, reason_codes: list[str],
               audit_refs: list[str], evidence_refs: list[str], **extra: object) -> str:
        seq = len(self.records) + 1
        trace_id = f"bb_{self.run_id}_{seq:03d}"
        rec = {
            "trace_id": trace_id,
            "run_id": self.run_id,
            "seq": seq,
            "decision_type": decision_type,
            "outcome": outcome,
            "reason_codes": reason_codes,
            "audit_refs": audit_refs,
            "evidence_refs": evidence_refs,
            "model_role": "not_called_deterministic_runtime",
            "created_at": utc_now_iso(),
            "redaction_applied": True,
            **extra,
        }
        self.records.append(rec)
        path = self.dir / f"{trace_id}.json"
        path.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return trace_id

    @property
    def trace_ids(self) -> list[str]:
        return [r["trace_id"] for r in self.records]
