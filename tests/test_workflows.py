from pathlib import Path

from clawthon_openclaw.audit_writer import JsonlAuditWriter
from clawthon_openclaw.client import WecreateClient, WecreateClientConfig
from clawthon_openclaw.workflows import create_enrollment, request_team_matches


class FakeTransport:
    def __init__(self, response):  # noqa: ANN001
        self.response = response
        self.requests = []

    def send(self, request):  # noqa: ANN001
        self.requests.append(request)
        return self.response


def test_create_enrollment_sends_request_and_writes_audit_event(tmp_path: Path) -> None:
    client = WecreateClient(WecreateClientConfig(base_url="http://localhost:8000"))
    transport = FakeTransport(
        {
            "status_code": 200,
            "json": {"id": 10, "hackathon_id": 12, "status": "pending"},
        }
    )
    writer = JsonlAuditWriter(tmp_path / "audit.jsonl")

    response = create_enrollment(
        hackathon_id=12,
        agent_id="agent-pm",
        trace_id="trace-enroll",
        client=client,
        transport=transport,
        audit_writer=writer,
    )

    assert response["json"]["hackathon_id"] == 12
    assert transport.requests[0].url == "http://localhost:8000/api/v1/enrollments/"
    assert '"action_name": "create_enrollment"' in (tmp_path / "audit.jsonl").read_text(encoding="utf-8")


def test_request_team_matches_sends_requirements_and_writes_audit_event(tmp_path: Path) -> None:
    client = WecreateClient(WecreateClientConfig(base_url="http://localhost:8000"))
    transport = FakeTransport(
        {
            "status_code": 200,
            "json": {"matches": [{"user_id": 3, "match_score": 92}]},
        }
    )
    writer = JsonlAuditWriter(tmp_path / "audit.jsonl")

    response = request_team_matches(
        hackathon_id=12,
        requirements="Need frontend partner",
        agent_id="agent-pm",
        trace_id="trace-match",
        client=client,
        transport=transport,
        audit_writer=writer,
    )

    assert response["json"]["matches"][0]["user_id"] == 3
    assert transport.requests[0].json_body["requirements"] == "Need frontend partner"
    assert '"action_name": "team_match"' in (tmp_path / "audit.jsonl").read_text(encoding="utf-8")
