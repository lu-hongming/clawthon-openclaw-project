from clawthon_openclaw.delivery import (
    build_commit_message,
    build_release_tag,
    build_submission_payload,
    slugify_name,
)


def test_slugify_name_normalizes_team_name() -> None:
    assert slugify_name("Claw PM Team") == "claw-pm-team"


def test_delivery_helpers_build_consistent_metadata() -> None:
    assert build_commit_message("pm", "define hackathon flow") == "pm: define hackathon flow"
    assert build_release_tag("Hack Team", "demo") == "hack-team-demo-v1"
    payload = build_submission_payload(
        repo_url="https://github.com/acme/claw",
        demo_url="https://demo.example.com",
        video_url="https://video.example.com",
        release_tag="hack-team-demo-v1",
    )
    assert payload["repo_url"] == "https://github.com/acme/claw"
    assert payload["custom_field_values"]["release_tag"] == "hack-team-demo-v1"

