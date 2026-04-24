import os

import pytest

from clawthon_openclaw.settings import WecreateRuntimeSettings


def test_runtime_settings_loads_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WECREATE_BASE_URL", "http://localhost:8000")
    monkeypatch.setenv("WECREATE_ACCESS_TOKEN", "token-123")

    settings = WecreateRuntimeSettings.from_env()

    assert settings.base_url == "http://localhost:8000"
    assert settings.access_token == "token-123"


def test_runtime_settings_requires_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("WECREATE_BASE_URL", raising=False)
    monkeypatch.delenv("WECREATE_ACCESS_TOKEN", raising=False)

    with pytest.raises(ValueError, match="WECREATE_BASE_URL"):
        WecreateRuntimeSettings.from_env()
