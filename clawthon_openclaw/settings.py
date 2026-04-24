from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class WecreateRuntimeSettings:
    base_url: str
    access_token: str | None = None

    @classmethod
    def from_env(cls) -> "WecreateRuntimeSettings":
        base_url = os.getenv("WECREATE_BASE_URL", "").strip()
        if not base_url:
            raise ValueError("WECREATE_BASE_URL is required")

        access_token = os.getenv("WECREATE_ACCESS_TOKEN", "").strip() or None
        return cls(base_url=base_url, access_token=access_token)
