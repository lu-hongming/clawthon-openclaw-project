from __future__ import annotations

import json
from pathlib import Path

from clawthon_openclaw.audit_writer import JsonlAuditWriter
from clawthon_openclaw.cli import build_parser
from clawthon_openclaw.client import WecreateClient, WecreateClientConfig
from clawthon_openclaw.persona import PersonaConfig
from clawthon_openclaw.remaining_workflows import (
    create_team,
    join_team,
    read_hackathon_detail,
    read_my_enrollment,
)
from clawthon_openclaw.runtime_env import apply_env_overrides, load_env_file
from clawthon_openclaw.settings import WecreateRuntimeSettings
from clawthon_openclaw.submission_workflow import submit_delivery
from clawthon_openclaw.sync import sync_persona_profile
from clawthon_openclaw.timeline import render_markdown_timeline
from clawthon_openclaw.transport import UrllibTransport
from clawthon_openclaw.workflows import create_enrollment, request_team_matches


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    apply_env_overrides(load_env_file(args.env_file))
    settings = WecreateRuntimeSettings.from_env()
    client = WecreateClient(
        WecreateClientConfig(
            base_url=settings.base_url,
            access_token=settings.access_token,
        )
    )
    transport = UrllibTransport()
    audit_path = Path("output/audit/demo.jsonl")
    audit_writer = JsonlAuditWriter(audit_path)

    if args.command == "sync-profile":
        persona = PersonaConfig.from_file(args.persona)
        result = sync_persona_profile(
            persona=persona,
            agent_id=persona.agent_name,
            trace_id="trace-sync-profile",
            client=client,
            transport=transport,
            audit_writer=audit_writer,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "list-hackathons":
        result = transport.send(client.list_hackathons())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "hackathon-detail":
        result = read_hackathon_detail(
            hackathon_id=args.hackathon_id,
            agent_id="cli-agent",
            trace_id="trace-hackathon-detail",
            client=client,
            transport=transport,
            audit_writer=audit_writer,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "my-enrollment":
        result = read_my_enrollment(
            hackathon_id=args.hackathon_id,
            agent_id="cli-agent",
            trace_id="trace-my-enrollment",
            client=client,
            transport=transport,
            audit_writer=audit_writer,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "enroll":
        result = create_enrollment(
            hackathon_id=args.hackathon_id,
            agent_id="cli-agent",
            trace_id="trace-enroll",
            client=client,
            transport=transport,
            audit_writer=audit_writer,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "team-match":
        result = request_team_matches(
            hackathon_id=args.hackathon_id,
            requirements=args.requirements,
            agent_id="cli-agent",
            trace_id="trace-team-match",
            client=client,
            transport=transport,
            audit_writer=audit_writer,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "create-team":
        result = create_team(
            hackathon_id=args.hackathon_id,
            team_payload={
                "name": args.name,
                "description": args.description,
                "recruitment_status": args.recruitment_status,
            },
            agent_id="cli-agent",
            trace_id="trace-create-team",
            client=client,
            transport=transport,
            audit_writer=audit_writer,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "join-team":
        result = join_team(
            team_id=args.team_id,
            agent_id="cli-agent",
            trace_id="trace-join-team",
            client=client,
            transport=transport,
            audit_writer=audit_writer,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "submit-delivery":
        result = submit_delivery(
            hackathon_id=args.hackathon_id,
            team_id=args.team_id,
            title=args.title,
            tagline=args.tagline,
            cover_image=args.cover_image,
            repo_url=args.repo_url,
            demo_url=args.demo_url,
            video_url=args.video_url,
            release_tag=args.release_tag,
            description=args.description,
            ai_capabilities=args.ai_capabilities,
            inference_stack=args.inference_stack,
            finalize=args.finalize,
            agent_id="cli-agent",
            trace_id="trace-submit-delivery",
            client=client,
            transport=transport,
            audit_writer=audit_writer,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "auto-team":
        detail = read_hackathon_detail(
            hackathon_id=args.hackathon_id,
            agent_id="cli-agent",
            trace_id="trace-auto-detail",
            client=client,
            transport=transport,
            audit_writer=audit_writer,
        )
        enrollment = read_my_enrollment(
            hackathon_id=args.hackathon_id,
            agent_id="cli-agent",
            trace_id="trace-auto-enrollment-read",
            client=client,
            transport=transport,
            audit_writer=audit_writer,
        )
        if enrollment.get("status_code") == 404:
            enrollment = create_enrollment(
                hackathon_id=args.hackathon_id,
                agent_id="cli-agent",
                trace_id="trace-auto-enroll",
                client=client,
                transport=transport,
                audit_writer=audit_writer,
            )
        matches = request_team_matches(
            hackathon_id=args.hackathon_id,
            requirements=args.requirements,
            agent_id="cli-agent",
            trace_id="trace-auto-team-match",
            client=client,
            transport=transport,
            audit_writer=audit_writer,
        )
        result = {
            "hackathon": detail,
            "enrollment": enrollment,
            "team_matches": matches,
            "next_step": {
                "action": "create_team",
                "team_name": args.team_name,
                "team_description": args.team_description,
            },
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "timeline":
        print(render_markdown_timeline(args.audit_path))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
