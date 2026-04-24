import json
from pathlib import Path

from clawthon_openclaw.audit import AuditEvent
from clawthon_openclaw.audit_writer import JsonlAuditWriter


def test_jsonl_audit_writer_appends_event_as_json_line(tmp_path: Path) -> None:
    output_path = tmp_path / "audit.jsonl"
    writer = JsonlAuditWriter(output_path)
    event = AuditEvent(
        trace_id="trace-001",
        agent_id="agent-pm",
        phase="enrollment",
        skill_name="hackathon_profile",
        action_name="sync_profile",
        target_type="user",
        target_id="user-1",
        input_summary="loaded persona config",
        output_summary="prepared profile payload",
        decision_reason="sync before enroll",
        status="success",
    )

    writer.write(event)

    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["trace_id"] == "trace-001"
    assert payload["action_name"] == "sync_profile"
