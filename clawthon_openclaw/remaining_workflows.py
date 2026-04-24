from __future__ import annotations

from clawthon_openclaw.audit import AuditEvent
from clawthon_openclaw.audit_writer import JsonlAuditWriter
from clawthon_openclaw.client import WecreateClient
from clawthon_openclaw.feishu import (
    FeishuClientConfig,
    build_feishu_webhook_request,
    format_feishu_event_message,
)


def _write_audit(
    *,
    audit_writer: JsonlAuditWriter,
    trace_id: str,
    agent_id: str,
    phase: str,
    action_name: str,
    target_type: str,
    target_id: str,
    input_summary: str,
    output_summary: str,
    decision_reason: str,
    status_code: int,
    endpoint: str,
) -> None:
    audit_writer.write(
        AuditEvent(
            trace_id=trace_id,
            agent_id=agent_id,
            phase=phase,
            skill_name="hackathon_teaming" if phase != "notification" else "hackathon_audit",
            action_name=action_name,
            target_type=target_type,
            target_id=target_id,
            input_summary=input_summary,
            output_summary=output_summary,
            decision_reason=decision_reason,
            status="success" if status_code == 200 else "failed",
            external_refs={"endpoint": endpoint},
        )
    )


def read_hackathon_detail(
    *,
    hackathon_id: int,
    agent_id: str,
    trace_id: str,
    client: WecreateClient,
    transport,
    audit_writer: JsonlAuditWriter,
) -> dict[str, object]:
    request = client.read_hackathon_detail(hackathon_id=hackathon_id)
    response = transport.send(request)
    _write_audit(
        audit_writer=audit_writer,
        trace_id=trace_id,
        agent_id=agent_id,
        phase="discovery",
        action_name="read_hackathon_detail",
        target_type="hackathon",
        target_id=str(hackathon_id),
        input_summary=f"requested hackathon detail {hackathon_id}",
        output_summary="loaded hackathon detail payload",
        decision_reason="agent needs the current event context before enrollment or teaming",
        status_code=response.get("status_code", 0),
        endpoint=request.url,
    )
    return response


def read_my_enrollment(
    *,
    hackathon_id: int,
    agent_id: str,
    trace_id: str,
    client: WecreateClient,
    transport,
    audit_writer: JsonlAuditWriter,
) -> dict[str, object]:
    request = client.read_my_enrollment(hackathon_id=hackathon_id)
    response = transport.send(request)
    _write_audit(
        audit_writer=audit_writer,
        trace_id=trace_id,
        agent_id=agent_id,
        phase="enrollment",
        action_name="read_my_enrollment",
        target_type="hackathon",
        target_id=str(hackathon_id),
        input_summary=f"requested my enrollment for hackathon {hackathon_id}",
        output_summary="loaded current enrollment state",
        decision_reason="avoid duplicate enrollment and branch flow based on current state",
        status_code=response.get("status_code", 0),
        endpoint=request.url,
    )
    return response


def create_team(
    *,
    hackathon_id: int,
    team_payload: dict[str, object],
    agent_id: str,
    trace_id: str,
    client: WecreateClient,
    transport,
    audit_writer: JsonlAuditWriter,
) -> dict[str, object]:
    request = client.create_team(hackathon_id=hackathon_id, team_payload=team_payload)
    response = transport.send(request)
    _write_audit(
        audit_writer=audit_writer,
        trace_id=trace_id,
        agent_id=agent_id,
        phase="teaming",
        action_name="create_team",
        target_type="hackathon",
        target_id=str(hackathon_id),
        input_summary=str(team_payload),
        output_summary="submitted team creation request",
        decision_reason="bootstrap a team when no suitable team exists",
        status_code=response.get("status_code", 0),
        endpoint=request.url,
    )
    return response


def join_team(
    *,
    team_id: int,
    agent_id: str,
    trace_id: str,
    client: WecreateClient,
    transport,
    audit_writer: JsonlAuditWriter,
) -> dict[str, object]:
    request = client.join_team(team_id=team_id)
    response = transport.send(request)
    _write_audit(
        audit_writer=audit_writer,
        trace_id=trace_id,
        agent_id=agent_id,
        phase="teaming",
        action_name="join_team",
        target_type="team",
        target_id=str(team_id),
        input_summary=f"requested join for team {team_id}",
        output_summary="submitted team join request",
        decision_reason="selected team from the candidate shortlist",
        status_code=response.get("status_code", 0),
        endpoint=request.url,
    )
    return response


def send_feishu_notification(
    *,
    webhook_url: str,
    event_name: str,
    team_name: str,
    summary: str,
    agent_id: str,
    trace_id: str,
    transport,
    audit_writer: JsonlAuditWriter,
) -> dict[str, object]:
    config = FeishuClientConfig(webhook_url=webhook_url)
    text = format_feishu_event_message(
        event_name=event_name,
        team_name=team_name,
        summary=summary,
    )
    request = build_feishu_webhook_request(config=config, text=text)
    response = transport.send(request)
    _write_audit(
        audit_writer=audit_writer,
        trace_id=trace_id,
        agent_id=agent_id,
        phase="notification",
        action_name="send_feishu_notification",
        target_type="team",
        target_id=team_name,
        input_summary=text,
        output_summary="sent Feishu webhook notification",
        decision_reason="surface key competition events to the external collaboration channel",
        status_code=response.get("status_code", 0),
        endpoint=request.url,
    )
    return response

