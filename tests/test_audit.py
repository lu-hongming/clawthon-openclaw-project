from clawthon_openclaw.audit import AuditEvent


def test_audit_event_serializes_to_replayable_payload() -> None:
    event = AuditEvent(
        trace_id="trace-001",
        agent_id="agent-pm",
        phase="teaming",
        skill_name="hackathon_teaming",
        action_name="rank_candidates",
        target_type="hackathon",
        target_id="hackathon-12",
        input_summary="requested teammates for PM role",
        output_summary="ranked 3 candidates",
        decision_reason="preferred skill complementarity",
        status="success",
        external_refs={"hackathon_id": 12, "team_id": None},
    )

    payload = event.to_dict()

    assert payload["trace_id"] == "trace-001"
    assert payload["agent_id"] == "agent-pm"
    assert payload["phase"] == "teaming"
    assert payload["external_refs"]["hackathon_id"] == 12
    assert payload["timestamp"].endswith("Z")

