from __future__ import annotations

from dataclasses import dataclass

from clawthon_openclaw.client import WecreateRequest


@dataclass(frozen=True)
class FeishuClientConfig:
    webhook_url: str


def format_feishu_event_message(*, event_name: str, team_name: str, summary: str) -> str:
    return f"[Clawthon] {event_name}\nTeam: {team_name}\nSummary: {summary}"


def build_feishu_webhook_request(
    *,
    config: FeishuClientConfig,
    text: str,
) -> WecreateRequest:
    return WecreateRequest(
        method="POST",
        url=config.webhook_url,
        headers={},
        json_body={"msg_type": "text", "content": {"text": text}},
    )

