from __future__ import annotations

import re


def slugify_name(name: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    return normalized or "clawthon"


def build_commit_message(role: str, summary: str) -> str:
    return f"{role.strip().lower()}: {summary.strip()}"


def build_release_tag(team_name: str, stage: str) -> str:
    return f"{slugify_name(team_name)}-{slugify_name(stage)}-v1"


def build_submission_payload(
    *,
    repo_url: str,
    demo_url: str,
    video_url: str,
    release_tag: str,
) -> dict[str, object]:
    return {
        "repo_url": repo_url,
        "demo_url": demo_url,
        "video_url": video_url,
        "custom_field_values": {
            "release_tag": release_tag,
        },
    }

