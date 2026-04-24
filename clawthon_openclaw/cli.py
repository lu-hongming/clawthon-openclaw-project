from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clawthon-openclaw")
    parser.add_argument(
        "--env-file",
        default="config/openclaw.env.local",
        help="Path to the local env file used for runtime API settings",
    )
    subparsers = parser.add_subparsers(dest="command")

    sync_profile = subparsers.add_parser("sync-profile")
    sync_profile.add_argument("--persona", required=True)

    subparsers.add_parser("list-hackathons")

    enroll = subparsers.add_parser("enroll")
    enroll.add_argument("--hackathon-id", required=True, type=int)

    team_match = subparsers.add_parser("team-match")
    team_match.add_argument("--hackathon-id", required=True, type=int)
    team_match.add_argument("--requirements", required=True)

    hackathon_detail = subparsers.add_parser("hackathon-detail")
    hackathon_detail.add_argument("--hackathon-id", required=True, type=int)

    my_enrollment = subparsers.add_parser("my-enrollment")
    my_enrollment.add_argument("--hackathon-id", required=True, type=int)

    create_team = subparsers.add_parser("create-team")
    create_team.add_argument("--hackathon-id", required=True, type=int)
    create_team.add_argument("--name", required=True)
    create_team.add_argument("--description", default="")
    create_team.add_argument("--recruitment-status", default="open")

    join_team = subparsers.add_parser("join-team")
    join_team.add_argument("--team-id", required=True, type=int)

    submit_delivery = subparsers.add_parser("submit-delivery")
    submit_delivery.add_argument("--hackathon-id", required=True, type=int)
    submit_delivery.add_argument("--team-id", required=True, type=int)
    submit_delivery.add_argument("--title", required=True)
    submit_delivery.add_argument("--tagline", required=True)
    submit_delivery.add_argument("--cover-image", required=True)
    submit_delivery.add_argument("--repo-url", required=True)
    submit_delivery.add_argument("--demo-url", required=True)
    submit_delivery.add_argument("--video-url", required=True)
    submit_delivery.add_argument("--release-tag", required=True)
    submit_delivery.add_argument("--description")
    submit_delivery.add_argument("--ai-capability", action="append", dest="ai_capabilities")
    submit_delivery.add_argument("--inference-stack")
    submit_delivery.add_argument("--finalize", action="store_true")

    auto_team = subparsers.add_parser("auto-team")
    auto_team.add_argument("--hackathon-id", required=True, type=int)
    auto_team.add_argument("--requirements", required=True)
    auto_team.add_argument("--team-name", required=True)
    auto_team.add_argument("--team-description", default="")

    timeline = subparsers.add_parser("timeline")
    timeline.add_argument("--audit-path", required=True)

    return parser
