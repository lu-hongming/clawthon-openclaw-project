from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class AuditEvent:
    trace_id: str
    agent_id: str
    phase: str
    skill_name: str
    action_name: str
    target_type: str
    target_id: str
    input_summary: str
    output_summary: str
    decision_reason: str
    status: str
    external_refs: dict[str, object] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

