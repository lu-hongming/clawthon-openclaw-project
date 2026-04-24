from clawthon_openclaw.feishu import (
    FeishuClientConfig,
    build_feishu_webhook_request,
    format_feishu_event_message,
)


def test_format_feishu_event_message_contains_team_and_event() -> None:
    message = format_feishu_event_message(
        event_name="team_formed",
        team_name="Claw Team",
        summary="Team formed successfully",
    )

    assert "team_formed" in message
    assert "Claw Team" in message
    assert "Team formed successfully" in message


def test_build_feishu_webhook_request_creates_post_payload() -> None:
    config = FeishuClientConfig(webhook_url="https://open.feishu.cn/webhook/demo")
    request = build_feishu_webhook_request(
        config=config,
        text="Hello Feishu",
    )

    assert request.method == "POST"
    assert request.url == "https://open.feishu.cn/webhook/demo"
    assert request.json_body == {"msg_type": "text", "content": {"text": "Hello Feishu"}}

