from urllib.error import HTTPError

from clawthon_openclaw.transport import parse_http_error


def test_parse_http_error_reads_json_payload() -> None:
    error = HTTPError(
        url="http://localhost:8000/api/v1/enrollments/my/1",
        code=404,
        msg="Not Found",
        hdrs=None,
        fp=None,
    )

    class FakeFP:
        def read(self) -> bytes:
            return b'{"detail":"Enrollment not found"}'

    error.fp = FakeFP()

    payload = parse_http_error(error)

    assert payload["status_code"] == 404
    assert payload["json"]["detail"] == "Enrollment not found"
