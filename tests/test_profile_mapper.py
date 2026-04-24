from clawthon_openclaw.persona import PersonaConfig
from clawthon_openclaw.profile_mapper import persona_to_wecreate_profile


def test_persona_to_wecreate_profile_maps_core_fields() -> None:
    persona = PersonaConfig(
        agent_name="Claw PM",
        role_preference="pm",
        personality_tags=["cautious", "strategic"],
        execution_style="research-first",
        risk_boundary="No paid APIs",
        memory_summary="Worked on prior hackathons",
        skills=["Product", "Prompting"],
        collaboration_preference="async-first",
        external_tool_policy={"allow_web_search": True, "allow_paid_api": False},
    )

    profile = persona_to_wecreate_profile(persona)

    assert profile["nickname"] == "Claw PM"
    assert profile["skills"] == "Product, Prompting"
    assert profile["personality"] == "cautious / strategic"
    assert "role=pm" in profile["bio"]
    assert "execution=research-first" in profile["bio"]

