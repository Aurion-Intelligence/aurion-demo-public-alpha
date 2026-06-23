"""
Minimal public PermissionGraph contract.

This is a deliberately small, public re-implementation of the *contract* Aurion's governed spine
enforces — not the full private PermissionGraph. The rules are intentionally simple and conservative:

  - fs.read   : allowed only inside the bundled demo workspace (WORKSPACE_DIR).
  - fs.write  : allowed only inside the designated generated-artifacts directory (GENERATED_DIR).
  - net.request : always denied (no network permission is granted in this bounded runtime).

Everything else is denied by default. There is no escalation path and no network capability at all.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .paths import GENERATED_DIR, REPO_ROOT, WORKSPACE_DIR, is_within


@dataclass(frozen=True)
class PermissionDecision:
    capability: str
    target: str
    allowed: bool
    reason_code: str
    reason: str


def _resolve_target_path(target: str) -> Path:
    """Resolve a repo-relative target string to an absolute path for boundary checks."""
    p = Path(target)
    if not p.is_absolute():
        p = REPO_ROOT / p
    return p.resolve()


def evaluate(capability: str, target: str) -> PermissionDecision:
    """Evaluate one capability request against the bounded contract. Pure, deterministic, offline."""
    if capability == "fs.read":
        path = _resolve_target_path(target)
        if is_within(path, WORKSPACE_DIR):
            return PermissionDecision(
                capability, target, True, "READ_IN_WORKSPACE",
                "Read allowed: target is inside the bundled demo workspace.",
            )
        return PermissionDecision(
            capability, target, False, "READ_OUTSIDE_WORKSPACE",
            "Read denied: target is outside the bundled demo workspace.",
        )

    if capability == "fs.write":
        path = _resolve_target_path(target)
        if is_within(path, GENERATED_DIR):
            return PermissionDecision(
                capability, target, True, "WRITE_IN_GENERATED",
                "Write allowed: target is inside the designated generated-artifacts directory.",
            )
        return PermissionDecision(
            capability, target, False, "WRITE_OUTSIDE_GENERATED",
            "Write denied: target is outside the designated generated-artifacts directory.",
        )

    if capability == "net.request":
        return PermissionDecision(
            capability, target, False, "NETWORK_NOT_PERMITTED",
            "Network denied: this bounded runtime grants no network permission.",
        )

    return PermissionDecision(
        capability, target, False, "CAPABILITY_UNKNOWN",
        f"Denied: unknown capability {capability!r} has no grant in the bounded contract.",
    )
