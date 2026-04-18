from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

import pytest

from src.ai.client import create_ai_client
from src.models import AIConfig


def load_ai_config() -> AIConfig:
    config_path = Path(__file__).resolve().parents[1] / "data" / "config.json"
    if not config_path.exists():
        pytest.skip("data/config.json is required for the live AI API smoke test")

    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return AIConfig.model_validate(payload["ai"])


def test_ai_api_smoke() -> None:
    config = load_ai_config()
    if not os.getenv(config.api_key_env):
        pytest.skip(f"{config.api_key_env} is not set")

    client = create_ai_client(config)
    response = asyncio.run(
        asyncio.wait_for(
            client.complete(
                system='Return a tiny JSON object with {"status":"ok"} only.',
                user="Health check.",
                temperature=0.0,
                max_tokens=32,
            ),
            timeout=45,
        )
    )

    assert isinstance(response, str)
    assert response.strip()
    assert "ok" in response.lower()
