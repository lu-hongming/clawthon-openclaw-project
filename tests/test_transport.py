from clawthon_openclaw.client import WecreateRequest
from clawthon_openclaw.transport import build_request_init


def test_build_request_init_adds_json_headers_and_body() -> None:
    request = WecreateRequest(
        method="POST",
        url="http://localhost:8000/api/v1/users/me",
        headers={"Authorization": "Bearer token"},
        json_body={"nickname": "Claw PM"},
    )

    init = build_request_init(request)

    assert init["method"] == "POST"
    assert init["headers"]["Authorization"] == "Bearer token"
    assert init["headers"]["Content-Type"] == "application/json"
    assert init["data"] == b'{"nickname": "Claw PM"}'


def test_build_request_init_skips_body_for_get_requests() -> None:
    request = WecreateRequest(
        method="GET",
        url="http://localhost:8000/api/v1/hackathons",
        headers={},
        json_body=None,
    )

    init = build_request_init(request)

    assert init["method"] == "GET"
    assert init["headers"] == {}
    assert "data" not in init
