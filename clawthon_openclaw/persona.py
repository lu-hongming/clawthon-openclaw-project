from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


REQUIRED_FIELDS = {
    "agent_name",
    "role_preference",
    "personality_tags",
    "execution_style",
    "risk_boundary",
    "memory_summary",
    "skills",
    "collaboration_preference",
    "external_tool_policy",
}


def _normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def _normalize_list(values: list[str]) -> list[str]:
    return [_normalize_text(value) for value in values if _normalize_text(value)]


@dataclass(frozen=True)
class PersonaConfig:
    agent_name: str
    role_preference: str
    personality_tags: list[str]
    execution_style: str
    risk_boundary: str
    memory_summary: str
    skills: list[str]
    collaboration_preference: str
    external_tool_policy: dict[str, bool]

    @classmethod
    def from_file(cls, path: str | Path) -> "PersonaConfig":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        missing = sorted(REQUIRED_FIELDS - raw.keys())
        if missing:
            raise ValueError(f"missing required fields: {', '.join(missing)}")

        return cls(
            agent_name=_normalize_text(raw["agent_name"]),
            role_preference=_normalize_text(raw["role_preference"]).lower(),
            personality_tags=_normalize_list(raw["personality_tags"]),
            execution_style=_normalize_text(raw["execution_style"]),
            risk_boundary=_normalize_text(raw["risk_boundary"]),
            memory_summary=_normalize_text(raw["memory_summary"]),
            skills=_normalize_list(raw["skills"]),
            collaboration_preference=_normalize_text(raw["collaboration_preference"]),
            external_tool_policy=dict(raw["external_tool_policy"]),
        )

