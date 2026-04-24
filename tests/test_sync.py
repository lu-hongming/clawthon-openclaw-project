from pathlib import Path

from clawthon_openclaw.audit_writer import JsonlAuditWriter
from clawthon_openclaw.client import WecreateClient, WecreateClientConfig
from clawthon_openclaw.persona import PersonaConfig
from clawthon_openclaw.sync import sync_persona_profile


class FakeTransport:
    def __init__(self) -> None:
        self.requests = []

    def send(self, request):  # noqa: ANN001
        self.requests.append(request)
        return {
            "status_code": 200,
            "json": {
                "id": 7,
                "nickname": request.json_body["nickname"],
                "skills": request.json_body["skills"],
            },
        }


def test_sync_persona_profile_updates_wecreate_and_writes_audit_event(
    tmp_path: Path,
) -> None:
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
    client = WecreateClient(
        WecreateClientConfig(base_url="http://localhost:8000", access_token="token")
    )
    transport = FakeTransport()
    audit_path = tmp_path / "audit.jsonl"
    writer = JsonlAuditWriter(audit_path)

    response = sync_persona_profile(
        persona=persona,
        agent_id="agent-pm",
        trace_id="trace-123",
        client=client,
        transport=transport,
        audit_writer=writer,
    )

    assert response["status_code"] == 200
    assert len(transport.requests) == 1
    assert transport.requests[0].url == "http://localhost:8000/api/v1/users/me"
    assert transport.requests[0].json_body["nickname"] == "Claw PM"
    audit_text = audit_path.read_text(encoding="utf-8")
    assert '"action_name": "sync_profile"' in audit_text
    assert '"status": "success"' in audit_text
