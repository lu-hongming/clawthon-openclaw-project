from pathlib import Path

from clawthon_openclaw.audit import AuditEvent
from clawthon_openclaw.audit_writer import JsonlAuditWriter
from clawthon_openclaw.timeline import render_markdown_timeline


def test_render_markdown_timeline_includes_core_event_fields(tmp_path: Path) -> None:
    path = tmp_path / "audit.jsonl"
    writer = JsonlAuditWriter(path)
    writer.write(
        AuditEvent(
            trace_id="trace-1",
            agent_id="agent-pm",
            phase="profile",
            skill_name="hackathon_profile",
            action_name="sync_profile",
            target_type="user",
            target_id="me",
            input_summary="persona loaded",
            output_summary="profile synced",
            decision_reason="align profile first",
            status="success",
        )
    )

    timeline = render_markdown_timeline(path)

    assert "# Audit Timeline" in timeline
    assert "sync_profile" in timeline
    assert "align profile first" in timeline

