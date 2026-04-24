from pathlib import Path

import pytest

from clawthon_openclaw.persona import PersonaConfig


def test_persona_config_loads_and_normalizes_fields(tmp_path: Path) -> None:
    config_path = tmp_path / "agent.json"
    config_path.write_text(
        """
        {
          "agent_name": "  Claw PM  ",
          "role_preference": " pm ",
          "personality_tags": [" cautious ", "strategic"],
          "execution_style": " research-first ",
          "risk_boundary": "No paid APIs",
          "memory_summary": "Worked on prior hackathons",
          "skills": [" Product ", "Prompting"],
          "collaboration_preference": " async-first ",
          "external_tool_policy": {
            "allow_web_search": true,
            "allow_paid_api": false
          }
        }
        """,
        encoding="utf-8",
    )

    persona = PersonaConfig.from_file(config_path)

    assert persona.agent_name == "Claw PM"
    assert persona.role_preference == "pm"
    assert persona.personality_tags == ["cautious", "strategic"]
    assert persona.skills == ["Product", "Prompting"]
    assert persona.external_tool_policy["allow_paid_api"] is False


def test_persona_config_rejects_missing_required_fields(tmp_path: Path) -> None:
    config_path = tmp_path / "agent.json"
    config_path.write_text(
        """
        {
          "agent_name": "Claw PM"
        }
        """,
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing required fields"):
        PersonaConfig.from_file(config_path)
