from pathlib import Path

from clawthon_openclaw.audit_writer import JsonlAuditWriter
from clawthon_openclaw.client import WecreateClient, WecreateClientConfig
from clawthon_openclaw.submission_workflow import submit_delivery


class FakeTransport:
    def __init__(self, response):  # noqa: ANN001
        self.response = response
        self.requests = []

    def send(self, request):  # noqa: ANN001
        self.requests.append(request)
        return self.response


def test_submit_delivery_creates_submission_request_and_audit(tmp_path: Path) -> None:
    client = WecreateClient(WecreateClientConfig(base_url="http://localhost:8000"))
    transport = FakeTransport({"status_code": 200, "json": {"id": 99, "status": "submitted"}})
    writer = JsonlAuditWriter(tmp_path / "audit.jsonl")

    response = submit_delivery(
        hackathon_id=1,
        team_id=33,
        title="OpenClaw Builders",
        tagline="Autonomous hackathon teaming and delivery",
        cover_image="https://images.example.com/openclaw-cover.png",
        repo_url="https://github.com/acme/openclaw-builders",
        demo_url="https://demo.example.com",
        video_url="https://video.example.com",
        release_tag="openclaw-builders-demo-v1",
        description="Agent-native team workflow built on Wecreate and OpenClaw.",
        ai_capabilities=["Agent 工作流", "多模态"],
        inference_stack="OpenAI API + OpenClaw runtime",
        finalize=True,
        agent_id="agent-pm",
        trace_id="trace-submit",
        client=client,
        transport=transport,
        audit_writer=writer,
    )

    assert response["json"]["id"] == 99
    assert transport.requests[0].url == "http://localhost:8000/api/v1/submissions?hackathon_id=1&team_id=33"
    assert transport.requests[1].url == "http://localhost:8000/api/v1/submissions/99/finalize"
    assert transport.requests[0].json_body["default_field_values"]["title"] == "OpenClaw Builders"
    assert transport.requests[0].json_body["default_field_values"]["tagline"] == "Autonomous hackathon teaming and delivery"
    assert transport.requests[0].json_body["default_field_values"]["cover_image"] == "https://images.example.com/openclaw-cover.png"
    assert transport.requests[0].json_body["default_field_values"]["repo_url"] == "https://github.com/acme/openclaw-builders"
    assert transport.requests[0].json_body["default_field_values"]["description"].startswith(
        "Agent-native team workflow built on Wecreate and OpenClaw."
    )
    assert "Release tag: openclaw-builders-demo-v1" in transport.requests[0].json_body["default_field_values"]["description"]
    assert "Video URL: https://video.example.com" in transport.requests[0].json_body["default_field_values"]["description"]
    assert transport.requests[0].json_body["custom_field_values"]["ai_capabilities"] == ["Agent 工作流", "多模态"]
    assert transport.requests[0].json_body["custom_field_values"]["inference_stack"] == "OpenAI API + OpenClaw runtime"
