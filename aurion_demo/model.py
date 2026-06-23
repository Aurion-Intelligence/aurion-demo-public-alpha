"""
Minimal mission model + deterministic planner.

A bounded mission is a goal plus an ordered list of microsteps. Each microstep declares the capability
it needs (fs.read / fs.write / net.request) and a target, so the PermissionGraph can evaluate it before
execution. The planner is fully deterministic: the same goal always yields the same plan.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from .paths import GENERATED_DIR, SAMPLE_NOTE, rel_to_repo

# The bundled bounded mission goal.
DEMO_GOAL = (
    "Review the included project note, identify three action items, save the result inside the demo "
    "workspace, and do not use the internet."
)


@dataclass(frozen=True)
class MicroStep:
    index: int
    capability: str          # "fs.read" | "fs.write" | "net.request"
    target: str              # repo-relative path or URL
    description: str
    expects: str             # "allowed" | "denied" (planner's honest expectation)


@dataclass
class MissionPlan:
    goal: str
    plan_id: str
    microsteps: list[MicroStep] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "goal": self.goal,
            "plan_id": self.plan_id,
            "microsteps": [
                {
                    "index": s.index,
                    "capability": s.capability,
                    "target": s.target,
                    "description": s.description,
                    "expects": s.expects,
                }
                for s in self.microsteps
            ],
        }


def build_plan(goal: str = DEMO_GOAL) -> MissionPlan:
    """Deterministically build the bounded plan for the demo goal.

    plan_id is derived from the goal text (stable across runs and platforms), distinct from the per-run
    run_id which is unique each execution.
    """
    plan_id = "plan_" + hashlib.sha256(goal.encode("utf-8")).hexdigest()[:12]

    out_path = GENERATED_DIR / "action_items.md"
    steps = [
        MicroStep(
            index=1,
            capability="fs.read",
            target=rel_to_repo(SAMPLE_NOTE),
            description="Read the included project note (inside the bundled demo workspace).",
            expects="allowed",
        ),
        MicroStep(
            index=2,
            capability="net.request",
            target="https://example.com/research",
            description="Attempt external research to enrich the note (no network permission granted).",
            expects="denied",
        ),
        MicroStep(
            index=3,
            capability="fs.write",
            target=rel_to_repo(out_path),
            description="Write the three identified action items into the generated-artifacts directory.",
            expects="allowed",
        ),
    ]
    return MissionPlan(goal=goal, plan_id=plan_id, microsteps=steps)
