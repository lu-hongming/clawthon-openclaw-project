from __future__ import annotations

from clawthon_openclaw.audit import AuditEvent
from clawthon_openclaw.audit_writer import JsonlAuditWriter
from clawthon_openclaw.client import WecreateClient
from clawthon_openclaw.persona import PersonaConfig
from clawthon_openclaw.profile_mapper import persona_to_wecreate_profile


def sync_persona_profile(
    *,
    persona: PersonaConfig,
    agent_id: str,
    trace_id: str,
    client: WecreateClient,
    transport,
    audit_writer: JsonlAuditWriter,
) -> dict[str, object]:
    profile = persona_to_wecreate_profile(persona)
    request = client.update_current_user(profile=profile)
    response = transport.send(request)

    audit_writer.write(
        AuditEvent(
            trace_id=trace_id,
            agent_id=agent_id,
            phase="profile",
            skill_name="hackathon_profile",
            action_name="sync_profile",
            target_type="user",
            target_id="me",
            input_summary=f"loaded persona for {persona.agent_name}",
            output_summary="synced profile payload to Wecreate",
            decision_reason="keep platform-visible agent profile aligned with local persona",
            status="success" if response.get("status_code") == 200 else "failed",
            external_refs={"endpoint": request.url},
        )
    )
    return response
