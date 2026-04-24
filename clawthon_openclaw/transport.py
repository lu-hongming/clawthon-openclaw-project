from __future__ import annotations

import json
from urllib.error import HTTPError
from urllib import request as urllib_request

from clawthon_openclaw.client import WecreateRequest


def build_request_init(request: WecreateRequest) -> dict[str, object]:
    headers = dict(request.headers)
    init: dict[str, object] = {
        "method": request.method,
        "headers": headers,
    }
    if request.json_body is not None:
        headers["Content-Type"] = "application/json"
        init["data"] = json.dumps(request.json_body, ensure_ascii=False).encode("utf-8")
    return init


def parse_http_error(error: HTTPError) -> dict[str, object]:
    payload = error.fp.read().decode("utf-8") if error.fp else ""
    return {
        "status_code": error.code,
        "json": json.loads(payload) if payload else {"detail": error.msg},
    }


class UrllibTransport:
    def send(self, request: WecreateRequest) -> dict[str, object]:
        init = build_request_init(request)
        http_request = urllib_request.Request(
            request.url,
            headers=init["headers"],
            method=init["method"],
            data=init.get("data"),
        )
        try:
            with urllib_request.urlopen(http_request) as response:
                payload = response.read().decode("utf-8")
                return {
                    "status_code": response.status,
                    "json": json.loads(payload) if payload else None,
                }
        except HTTPError as error:
            return parse_http_error(error)
