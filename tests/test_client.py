from clawthon_openclaw.client import WecreateClient, WecreateClientConfig


def test_wecreate_client_config_builds_expected_paths_and_headers() -> None:
    config = WecreateClientConfig(
        base_url="http://localhost:8000",
        access_token="secret-token",
    )

    assert config.endpoint("/api/v1/hackathons") == "http://localhost:8000/api/v1/hackathons"
    assert config.endpoint("api/v1/ai/team-match") == "http://localhost:8000/api/v1/ai/team-match"
    assert config.auth_headers() == {"Authorization": "Bearer secret-token"}


def test_wecreate_client_config_returns_empty_headers_without_token() -> None:
    config = WecreateClientConfig(base_url="http://localhost:8000")

    assert config.auth_headers() == {}


def test_wecreate_client_builds_list_hackathons_request() -> None:
    client = WecreateClient(
        WecreateClientConfig(base_url="http://localhost:8000", access_token="token")
    )

    request = client.list_hackathons()

    assert request.method == "GET"
    assert request.url == "http://localhost:8000/api/v1/hackathons"
    assert request.headers["Authorization"] == "Bearer token"
    assert request.json_body is None


def test_wecreate_client_builds_create_enrollment_request() -> None:
    client = WecreateClient(WecreateClientConfig(base_url="http://localhost:8000"))

    request = client.create_enrollment(hackathon_id=12)

    assert request.method == "POST"
    assert request.url == "http://localhost:8000/api/v1/enrollments/"
    assert request.json_body == {"hackathon_id": 12}


def test_wecreate_client_builds_team_match_request() -> None:
    client = WecreateClient(WecreateClientConfig(base_url="http://localhost:8000"))

    request = client.team_match(hackathon_id=12, requirements="Need frontend partner")

    assert request.method == "POST"
    assert request.url == "http://localhost:8000/api/v1/ai/team-match"
    assert request.json_body == {
        "hackathon_id": 12,
        "requirements": "Need frontend partner",
    }


def test_wecreate_client_builds_finalize_submission_request() -> None:
    client = WecreateClient(WecreateClientConfig(base_url="http://localhost:8000"))

    request = client.finalize_submission(submission_id=55)

    assert request.method == "POST"
    assert request.url == "http://localhost:8000/api/v1/submissions/55/finalize"
    assert request.json_body is None
