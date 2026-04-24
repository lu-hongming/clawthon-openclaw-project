#!/usr/bin/env python3
"""Participant-safe wrapper around the Wecreate submissions API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_FIELD_FLAGS = (
    "title",
    "cover_image",
    "tagline",
    "description",
    "demo_url",
    "repo_url",
)


class CliError(RuntimeError):
    """Raised for user-correctable CLI and API errors."""


@dataclass
class ApiContext:
    base_url: str
    bearer_token: str
    allowed_hackathon_ids: set[int]
    timeout_seconds: float


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Wecreate participant submission APIs safely.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=float(os.getenv("WECREATE_TIMEOUT_SECONDS", "20")),
        help="HTTP timeout in seconds. Defaults to WECREATE_TIMEOUT_SECONDS or 20.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    form_config = subparsers.add_parser(
        "form-config",
        help="Read the resolved submission form for a hackathon.",
    )
    form_config.add_argument("--hackathon-id", type=int, required=True)

    my_submissions = subparsers.add_parser(
        "my-submissions",
        help="Read the authenticated user's submissions.",
    )
    my_submissions.add_argument(
        "--hackathon-id",
        type=int,
        help="Optional hackathon filter. Without it, results are filtered to allowed hackathons only.",
    )

    list_submissions = subparsers.add_parser(
        "list-submissions",
        help="List visible submissions for a hackathon.",
    )
    list_submissions.add_argument("--hackathon-id", type=int, required=True)
    list_submissions.add_argument("--offset", type=int, default=0)
    list_submissions.add_argument("--limit", type=int, default=100)
    list_submissions.add_argument("--sort-by-score", action="store_true")

    get_submission = subparsers.add_parser(
        "get-submission",
        help="Read one submission after verifying its hackathon.",
    )
    get_submission.add_argument("--hackathon-id", type=int, required=True)
    get_submission.add_argument("--submission-id", type=int, required=True)

    for name, help_text in (
        ("create", "Create a draft submission."),
        ("update", "Update an existing draft submission."),
    ):
        command_parser = subparsers.add_parser(name, help=help_text)
        command_parser.add_argument("--hackathon-id", type=int, required=True)
        if name == "create":
            command_parser.add_argument("--team-id", type=int)
            command_parser.add_argument("--project-id", type=int)
        else:
            command_parser.add_argument("--submission-id", type=int, required=True)
        _add_payload_arguments(command_parser)

    finalize = subparsers.add_parser(
        "finalize",
        help="Finalize a draft submission.",
    )
    finalize.add_argument("--hackathon-id", type=int, required=True)
    finalize.add_argument("--submission-id", type=int, required=True)

    return parser.parse_args()


def _add_payload_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--payload-file",
        help="Path to a JSON file shaped like SubmissionCreate.",
    )
    parser.add_argument("--title")
    parser.add_argument("--cover-image")
    parser.add_argument("--tagline")
    parser.add_argument("--description")
    parser.add_argument("--demo-url")
    parser.add_argument("--repo-url")
    parser.add_argument(
        "--custom-field",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Repeatable custom field. VALUE is parsed as JSON first, then as a plain string.",
    )


def _build_context(timeout_seconds: float) -> ApiContext:
    base_url = os.getenv("WECREATE_API_BASE_URL", "").strip().rstrip("/")
    bearer_token = os.getenv("WECREATE_API_BEARER_TOKEN", "").strip()
    raw_allowed_ids = os.getenv("WECREATE_ALLOWED_HACKATHON_IDS", "").strip()

    if not base_url:
        raise CliError("WECREATE_API_BASE_URL is required")
    if not bearer_token:
        raise CliError("WECREATE_API_BEARER_TOKEN is required")
    if not raw_allowed_ids:
        raise CliError("WECREATE_ALLOWED_HACKATHON_IDS is required")

    allowed_ids = _parse_allowed_hackathon_ids(raw_allowed_ids)
    if not allowed_ids:
        raise CliError("WECREATE_ALLOWED_HACKATHON_IDS must contain at least one integer id")

    return ApiContext(
        base_url=base_url,
        bearer_token=bearer_token,
        allowed_hackathon_ids=allowed_ids,
        timeout_seconds=timeout_seconds,
    )


def _parse_allowed_hackathon_ids(raw_value: str) -> set[int]:
    result: set[int] = set()
    for piece in raw_value.replace(",", " ").split():
        try:
            result.add(int(piece))
        except ValueError as exc:
            raise CliError(
                "WECREATE_ALLOWED_HACKATHON_IDS must be a comma- or space-separated list of integers"
            ) from exc
    return result


def _ensure_allowed(ctx: ApiContext, hackathon_id: int) -> None:
    if hackathon_id not in ctx.allowed_hackathon_ids:
        allowed = ", ".join(str(item) for item in sorted(ctx.allowed_hackathon_ids))
        raise CliError(
            f"Hackathon {hackathon_id} is outside WECREATE_ALLOWED_HACKATHON_IDS ({allowed})"
        )


def _request_json(
    ctx: ApiContext,
    *,
    method: str,
    path: str,
    query: dict[str, Any] | None = None,
    body: dict[str, Any] | list[Any] | None = None,
) -> Any:
    url = f"{ctx.base_url}{path}"
    if query:
        query_string = urllib.parse.urlencode(
            {key: value for key, value in query.items() if value is not None}
        )
        if query_string:
            url = f"{url}?{query_string}"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {ctx.bearer_token}",
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=ctx.timeout_seconds) as response:
            charset = response.headers.get_content_charset("utf-8")
            raw_body = response.read().decode(charset)
    except urllib.error.HTTPError as exc:
        raw_error = exc.read().decode(exc.headers.get_content_charset("utf-8"), errors="replace")
        raise CliError(f"HTTP {exc.code}: {_extract_error_message(raw_error)}") from exc
    except urllib.error.URLError as exc:
        raise CliError(f"Request failed: {exc.reason}") from exc

    if not raw_body:
        return {}

    try:
        return json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise CliError(f"Response was not valid JSON: {raw_body}") from exc


def _extract_error_message(raw_body: str) -> str:
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        return raw_body.strip() or "unknown error"

    if isinstance(payload, dict):
        for key in ("detail", "error", "message"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
            if isinstance(value, list) and value:
                return json.dumps(value, ensure_ascii=False)
    return json.dumps(payload, ensure_ascii=False)


def _parse_custom_fields(entries: list[str]) -> dict[str, Any]:
    custom_fields: dict[str, Any] = {}
    for entry in entries:
        if "=" not in entry:
            raise CliError(f"Invalid --custom-field value '{entry}'. Expected KEY=VALUE.")
        key, raw_value = entry.split("=", 1)
        key = key.strip()
        if not key:
            raise CliError("Custom field keys cannot be empty")

        parsed_value: Any
        try:
            parsed_value = json.loads(raw_value)
        except json.JSONDecodeError:
            parsed_value = raw_value
        custom_fields[key] = parsed_value
    return custom_fields


def _payload_has_inline_values(args: argparse.Namespace) -> bool:
    inline_values = [getattr(args, field) for field in DEFAULT_FIELD_FLAGS]
    return any(value is not None for value in inline_values) or bool(args.custom_field)


def _load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.payload_file:
        if _payload_has_inline_values(args):
            raise CliError("Do not combine --payload-file with inline field arguments")

        payload_path = Path(args.payload_file)
        try:
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise CliError(f"Payload file not found: {payload_path}") from exc
        except json.JSONDecodeError as exc:
            raise CliError(f"Payload file is not valid JSON: {payload_path}") from exc

        if not isinstance(payload, dict):
            raise CliError("Payload file must contain a JSON object")

        default_field_values = payload.get("default_field_values", {})
        custom_field_values = payload.get("custom_field_values", {})
        if not isinstance(default_field_values, dict) or not isinstance(custom_field_values, dict):
            raise CliError(
                "Payload file must use object values for default_field_values and custom_field_values"
            )
        return {
            "default_field_values": default_field_values,
            "custom_field_values": custom_field_values,
        }

    payload = {
        "default_field_values": {},
        "custom_field_values": _parse_custom_fields(args.custom_field),
    }

    for field in DEFAULT_FIELD_FLAGS:
        value = getattr(args, field)
        if value is not None:
            payload["default_field_values"][field] = value
    return payload


def _get_submission_and_verify(
    ctx: ApiContext,
    *,
    hackathon_id: int,
    submission_id: int,
) -> dict[str, Any]:
    _ensure_allowed(ctx, hackathon_id)
    submission = _request_json(
        ctx,
        method="GET",
        path=f"/api/v1/submissions/{submission_id}",
    )
    actual_hackathon_id = submission.get("hackathon_id")
    if actual_hackathon_id != hackathon_id:
        raise CliError(
            f"Submission {submission_id} belongs to hackathon {actual_hackathon_id}, not {hackathon_id}"
        )
    return submission


def _print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    args = _parse_args()
    try:
        ctx = _build_context(args.timeout_seconds)

        if args.command == "form-config":
            _ensure_allowed(ctx, args.hackathon_id)
            response = _request_json(
                ctx,
                method="GET",
                path=f"/api/v1/submission-fields/hackathons/{args.hackathon_id}/form-config",
            )
            _print_json(response)
            return 0

        if args.command == "my-submissions":
            submissions = _request_json(
                ctx,
                method="GET",
                path="/api/v1/submissions/me",
            )
            if not isinstance(submissions, list):
                raise CliError("Expected /api/v1/submissions/me to return a JSON array")
            if args.hackathon_id is not None:
                _ensure_allowed(ctx, args.hackathon_id)
                submissions = [
                    item
                    for item in submissions
                    if isinstance(item, dict) and item.get("hackathon_id") == args.hackathon_id
                ]
            else:
                submissions = [
                    item
                    for item in submissions
                    if isinstance(item, dict)
                    and item.get("hackathon_id") in ctx.allowed_hackathon_ids
                ]
            _print_json(submissions)
            return 0

        if args.command == "list-submissions":
            _ensure_allowed(ctx, args.hackathon_id)
            response = _request_json(
                ctx,
                method="GET",
                path="/api/v1/submissions",
                query={
                    "hackathon_id": args.hackathon_id,
                    "offset": args.offset,
                    "limit": args.limit,
                    "sort_by_score": str(bool(args.sort_by_score)).lower(),
                },
            )
            _print_json(response)
            return 0

        if args.command == "get-submission":
            submission = _get_submission_and_verify(
                ctx,
                hackathon_id=args.hackathon_id,
                submission_id=args.submission_id,
            )
            _print_json(submission)
            return 0

        if args.command == "create":
            _ensure_allowed(ctx, args.hackathon_id)
            payload = _load_payload(args)
            response = _request_json(
                ctx,
                method="POST",
                path="/api/v1/submissions",
                query={
                    "hackathon_id": args.hackathon_id,
                    "team_id": args.team_id,
                    "project_id": args.project_id,
                },
                body=payload,
            )
            _print_json(response)
            return 0

        if args.command == "update":
            _get_submission_and_verify(
                ctx,
                hackathon_id=args.hackathon_id,
                submission_id=args.submission_id,
            )
            payload = _load_payload(args)
            response = _request_json(
                ctx,
                method="PATCH",
                path=f"/api/v1/submissions/{args.submission_id}",
                body=payload,
            )
            _print_json(response)
            return 0

        if args.command == "finalize":
            _get_submission_and_verify(
                ctx,
                hackathon_id=args.hackathon_id,
                submission_id=args.submission_id,
            )
            response = _request_json(
                ctx,
                method="POST",
                path=f"/api/v1/submissions/{args.submission_id}/finalize",
            )
            _print_json(response)
            return 0

        raise CliError(f"Unsupported command: {args.command}")
    except CliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
