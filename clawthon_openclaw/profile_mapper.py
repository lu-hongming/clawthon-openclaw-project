from __future__ import annotations

from clawthon_openclaw.persona import PersonaConfig


def persona_to_wecreate_profile(persona: PersonaConfig) -> dict[str, str]:
    bio_parts = [
        f"role={persona.role_preference}",
        f"execution={persona.execution_style}",
        f"risk={persona.risk_boundary}",
        f"memory={persona.memory_summary}",
        f"collaboration={persona.collaboration_preference}",
    ]

    return {
        "nickname": persona.agent_name,
        "skills": ", ".join(persona.skills),
        "personality": " / ".join(persona.personality_tags),
        "bio": " | ".join(bio_parts),
    }
