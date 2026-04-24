from clawthon_openclaw.cli import build_parser


def test_cli_parser_exposes_expected_commands() -> None:
    parser = build_parser()
    commands = parser._subparsers._group_actions[0].choices.keys()  # type: ignore[attr-defined]

    assert "sync-profile" in commands
    assert "list-hackathons" in commands
    assert "enroll" in commands
    assert "team-match" in commands
    assert "hackathon-detail" in commands
    assert "my-enrollment" in commands
    assert "create-team" in commands
    assert "join-team" in commands
    assert "submit-delivery" in commands
    assert "auto-team" in commands
    assert "timeline" in commands
