from __future__ import annotations

from clawthon_openclaw.audit import AuditEvent
from clawthon_openclaw.audit_writer import JsonlAuditWriter
from clawthon_openclaw.client import WecreateClient


def submit_delivery(
    *,
    hackathon_id: int,
    team_id: int,
    title: str,
    tagline: str,
    cover_image: str,
    repo_url: str,
    demo_url: str,
    video_url: str,
    release_tag: str,
    description: str | None,
    ai_capabilities: list[str] | None,
    inference_stack: str | None,
    finalize: bool,
    agent_id: str,
    trace_id: str,
    client: WecreateClient,
    transport,
    audit_writer: JsonlAuditWriter,
) -> dict[str, object]:
    description_text = description or ""
    metadata_suffix = f"Release tag: {release_tag}\nVideo URL: {video_url}"
    description_text = f"{description_text}\n\n{metadata_suffix}".strip()

    custom_field_values: dict[str, object] = {}
    if ai_capabilities:
        custom_field_values["ai_capabilities"] = ai_capabilities
    if inference_stack:
        custom_field_values["inference_stack"] = inference_stack

    payload = {
        "default_field_values": {
            "title": title,
            "cover_image": cover_image,
            "tagline": tagline,
            "repo_url": repo_url,
            "demo_url": demo_url,
            "description": description_text,
        },
        "custom_field_values": custom_field_values,
    }
    request = client.create_submission(
        hackathon_id=hackathon_id,
        team_id=team_id,
        payload=payload,
    )
    response = transport.send(request)
    audit_writer.write(
        AuditEvent(
            trace_id=trace_id,
            agent_id=agent_id,
            phase="delivery",
            skill_name="hackathon_delivery",
            action_name="submit_delivery",
            target_type="team",
            target_id=str(team_id),
            input_summary=f"repo={repo_url} demo={demo_url} release={release_tag}",
            output_summary="submitted delivery metadata to Wecreate",
            decision_reason="persist repo and release artifacts into the platform submission record",
            status="success" if response.get("status_code") == 200 else "failed",
            external_refs={"endpoint": request.url},
        )
    )
    if not finalize:
        return response

    submission_id = response.get("json", {}).get("id")
    if not submission_id:
        return response

    finalize_request = client.finalize_submission(submission_id=int(submission_id))
    finalize_response = transport.send(finalize_request)
    audit_writer.write(
        AuditEvent(
            trace_id=trace_id,
            agent_id=agent_id,
            phase="delivery",
            skill_name="hackathon_delivery",
            action_name="finalize_submission",
            target_type="submission",
            target_id=str(submission_id),
            input_summary=f"finalize submission {submission_id}",
            output_summary="finalized draft submission into submitted state",
            decision_reason="lock the current project artifacts as the team's official submission",
            status="success" if finalize_response.get("status_code") == 200 else "failed",
            external_refs={"endpoint": finalize_request.url},
        )
    )
    return finalize_response
