from pathlib import Path

from clawthon_openclaw.runtime_env import load_env_file


def test_load_env_file_reads_key_value_pairs(tmp_path: Path) -> None:
    env_path = tmp_path / ".env.local"
    env_path.write_text(
        "WECREATE_BASE_URL=http://127.0.0.1:8010\n"
        "WECREATE_ACCESS_TOKEN=token-123\n"
        "FEISHU_WEBHOOK_URL=\n",
        encoding="utf-8",
    )

    data = load_env_file(env_path)

    assert data["WECREATE_BASE_URL"] == "http://127.0.0.1:8010"
    assert data["WECREATE_ACCESS_TOKEN"] == "token-123"
    assert data["FEISHU_WEBHOOK_URL"] == ""
