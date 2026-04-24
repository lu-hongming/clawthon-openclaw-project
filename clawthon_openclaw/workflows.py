from __future__ import annotations

from clawthon_openclaw.audit import AuditEvent
from clawthon_openclaw.audit_writer import JsonlAuditWriter
from clawthon_openclaw.client import WecreateClient


def create_enrollment(
    *,
    hackathon_id: int,
    agent_id: str,
    trace_id: str,
    client: WecreateClient,
    transport,
    audit_writer: JsonlAuditWriter,
) -> dict[str, object]:
    request = client.create_enrollment(hackathon_id=hackathon_id)
    response = transport.send(request)
    audit_writer.write(
        AuditEvent(
            trace_id=trace_id,
            agent_id=agent_id,
            phase="enrollment",
            skill_name="hackathon_teaming",
            action_name="create_enrollment",
            target_type="hackathon",
            target_id=str(hackathon_id),
            input_summary=f"requested enrollment for hackathon {hackathon_id}",
            output_summary="submitted enrollment request to Wecreate",
            decision_reason="agent must be enrolled before team formation",
            status="success" if response.get("status_code") == 200 else "failed",
            external_refs={"endpoint": request.url},
        )
    )
    return response


def request_team_matches(
    *,
    hackathon_id: int,
    requirements: str,
    agent_id: str,
    trace_id: str,
    client: WecreateClient,
    transport,
    audit_writer: JsonlAuditWriter,
) -> dict[str, object]:
    request = client.team_match(
        hackathon_id=hackathon_id,
        requirements=requirements,
    )
    response = transport.send(request)
    match_count = len(response.get("json", {}).get("matches", []))
    audit_writer.write(
        AuditEvent(
            trace_id=trace_id,
            agent_id=agent_id,
            phase="teaming",
            skill_name="hackathon_teaming",
            action_name="team_match",
            target_type="hackathon",
            target_id=str(hackathon_id),
            input_summary=requirements,
            output_summary=f"received {match_count} team match candidates",
            decision_reason="use platform-side AI ranking to narrow teammate search",
            status="success" if response.get("status_code") == 200 else "failed",
            external_refs={"endpoint": request.url},
        )
    )
    return response
