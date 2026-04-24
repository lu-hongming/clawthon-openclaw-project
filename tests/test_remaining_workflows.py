from pathlib import Path

from clawthon_openclaw.audit_writer import JsonlAuditWriter
from clawthon_openclaw.client import WecreateClient, WecreateClientConfig
from clawthon_openclaw.remaining_workflows import (
    create_team,
    read_hackathon_detail,
    read_my_enrollment,
    send_feishu_notification,
    join_team,
)


class FakeTransport:
    def __init__(self, response):  # noqa: ANN001
        self.response = response
        self.requests = []

    def send(self, request):  # noqa: ANN001
        self.requests.append(request)
        return self.response


def test_read_hackathon_detail_writes_audit_trace(tmp_path: Path) -> None:
    client = WecreateClient(WecreateClientConfig(base_url="http://localhost:8000"))
    transport = FakeTransport({"status_code": 200, "json": {"id": 12, "title": "Clawthon"}})
    writer = JsonlAuditWriter(tmp_path / "audit.jsonl")

    response = read_hackathon_detail(
        hackathon_id=12,
        agent_id="agent-pm",
        trace_id="trace-detail",
        client=client,
        transport=transport,
        audit_writer=writer,
    )

    assert response["json"]["title"] == "Clawthon"
    assert transport.requests[0].url == "http://localhost:8000/api/v1/hackathons/12"


def test_read_my_enrollment_writes_audit_trace(tmp_path: Path) -> None:
    client = WecreateClient(WecreateClientConfig(base_url="http://localhost:8000"))
    transport = FakeTransport({"status_code": 200, "json": {"hackathon_id": 12, "status": "pending"}})
    writer = JsonlAuditWriter(tmp_path / "audit.jsonl")

    response = read_my_enrollment(
        hackathon_id=12,
        agent_id="agent-pm",
        trace_id="trace-enrollment-read",
        client=client,
        transport=transport,
        audit_writer=writer,
    )

    assert response["json"]["status"] == "pending"
    assert transport.requests[0].url == "http://localhost:8000/api/v1/enrollments/my/12"


def test_create_team_writes_audit_trace(tmp_path: Path) -> None:
    client = WecreateClient(WecreateClientConfig(base_url="http://localhost:8000"))
    transport = FakeTransport({"status_code": 200, "json": {"id": 5, "name": "Claw Team"}})
    writer = JsonlAuditWriter(tmp_path / "audit.jsonl")

    response = create_team(
        hackathon_id=12,
        team_payload={"name": "Claw Team", "recruitment_status": "open"},
        agent_id="agent-pm",
        trace_id="trace-team-create",
        client=client,
        transport=transport,
        audit_writer=writer,
    )

    assert response["json"]["name"] == "Claw Team"
    assert transport.requests[0].url == "http://localhost:8000/api/v1/teams?hackathon_id=12"


def test_join_team_writes_audit_trace(tmp_path: Path) -> None:
    client = WecreateClient(WecreateClientConfig(base_url="http://localhost:8000"))
    transport = FakeTransport({"status_code": 200, "json": {"team_id": 5, "user_id": 7}})
    writer = JsonlAuditWriter(tmp_path / "audit.jsonl")

    response = join_team(
        team_id=5,
        agent_id="agent-dev",
        trace_id="trace-team-join",
        client=client,
        transport=transport,
        audit_writer=writer,
    )

    assert response["json"]["team_id"] == 5
    assert transport.requests[0].url == "http://localhost:8000/api/v1/teams/5/join"


def test_send_feishu_notification_writes_audit_trace(tmp_path: Path) -> None:
    transport = FakeTransport({"status_code": 200, "json": {"ok": True}})
    writer = JsonlAuditWriter(tmp_path / "audit.jsonl")

    response = send_feishu_notification(
        webhook_url="https://open.feishu.cn/webhook/demo",
        event_name="team_formed",
        team_name="Claw Team",
        summary="Team formed successfully",
        agent_id="agent-pm",
        trace_id="trace-feishu",
        transport=transport,
        audit_writer=writer,
    )

    assert response["status_code"] == 200
    assert transport.requests[0].url == "https://open.feishu.cn/webhook/demo"
