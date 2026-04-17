from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from src.models import ContentItem, SourceType
from src.mcp.server import hz_get_metrics
from src.mcp.service import HorizonPipelineService


def load_test_config_text(repo_root: Path) -> str:
    for candidate in ("config.example.json", "config.json"):
        path = repo_root / "data" / candidate
        if path.exists():
            return path.read_text(encoding="utf-8")
    raise FileNotFoundError("No test config fixture found in data/")


def make_item(
    item_id: str,
    score: float | None = None,
    editorial_fit: str | None = None,
) -> ContentItem:
    item = ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title=f"Item {item_id}",
        url=f"https://example.com/{item_id}",
        content="content",
        author="tester",
        published_at=datetime.now(timezone.utc),
    )
    item.ai_score = score
    item.ai_editorial_fit = editorial_fit
    return item


def test_validate_config_smoke(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config_path = tmp_path / "config.json"
    config_path.write_text(load_test_config_text(repo_root), encoding="utf-8")

    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")
    result = asyncio.run(
        service.validate_config(
            horizon_path=str(repo_root),
            config_path=str(config_path),
            check_env=False,
        )
    )

    assert result["config_path"] == str(config_path.resolve())
    assert result["enabled_sources"]
    assert result["missing_env"] == []


def test_get_effective_config_can_filter_sources(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config_path = tmp_path / "config.json"
    config_path.write_text(load_test_config_text(repo_root), encoding="utf-8")

    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")
    result = service.get_effective_config(
        horizon_path=str(repo_root),
        config_path=str(config_path),
        sources=["rss"],
    )

    assert result["selected_sources"] == ["rss"]
    assert result["config"]["sources"]["github"] == []
    assert result["config"]["sources"]["rss"]


def test_metrics_tool_smoke() -> None:
    result = hz_get_metrics()

    assert result["ok"] is True
    assert result["tool"] == "hz_get_metrics"


def test_fetch_items_uses_public_orchestrator_api(tmp_path: Path, monkeypatch) -> None:
    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")
    config_path = tmp_path / "config.json"

    monkeypatch.setattr(
        service,
        "_build_context",
        lambda **kwargs: (
            SimpleNamespace(
                horizon_path=tmp_path,
                config_path=config_path,
                runtime=SimpleNamespace(),
                config=SimpleNamespace(),
            ),
            ["rss"],
            [],
        ),
    )
    monkeypatch.setattr("src.mcp.service.make_storage", lambda runtime, config_path: object())

    class FakeOrchestrator:
        async def fetch_all_sources(self, since):  # type: ignore[no-untyped-def]
            return [make_item("item-1"), make_item("item-2")]

        def merge_cross_source_duplicates(self, items):  # type: ignore[no-untyped-def]
            return items[:1]

    monkeypatch.setattr(
        "src.mcp.service.make_orchestrator",
        lambda runtime, config, storage: FakeOrchestrator(),
    )

    result = asyncio.run(service.fetch_items(hours=6))

    assert result["fetched"] == 1
    assert result["raw_before_merge"] == 2
    assert service.run_store.load_items(result["run_id"], "raw")[0]["id"] == "item-1"


def test_filter_items_uses_public_topic_dedup_api(tmp_path: Path, monkeypatch) -> None:
    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")
    service.run_store.create_run("run-topic-dedup")

    monkeypatch.setattr(
        service,
        "_load_stage_items",
        lambda **kwargs: (
            [make_item("item-1", score=9.0), make_item("item-2", score=8.0)],
            SimpleNamespace(
                runtime=SimpleNamespace(),
                config_path=tmp_path / "config.json",
                config=SimpleNamespace(filtering=SimpleNamespace(ai_score_threshold=7.0)),
            ),
        ),
    )
    monkeypatch.setattr("src.mcp.service.make_storage", lambda runtime, config_path: object())

    class FakeOrchestrator:
        async def merge_topic_duplicates(self, items):  # type: ignore[no-untyped-def]
            return items[:1]

    monkeypatch.setattr(
        "src.mcp.service.make_orchestrator",
        lambda runtime, config, storage: FakeOrchestrator(),
    )

    result = asyncio.run(service.filter_items(run_id="run-topic-dedup", topic_dedup=True))

    assert result["kept"] == 1
    assert result["removed_by_topic_dedup"] == 1
    assert service.run_store.load_items("run-topic-dedup", "filtered")[0]["id"] == "item-1"


def test_filter_items_requires_editorial_fit(tmp_path: Path, monkeypatch) -> None:
    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")
    service.run_store.create_run("run-editorial-fit")

    monkeypatch.setattr(
        service,
        "_load_stage_items",
        lambda **kwargs: (
            [
                make_item("item-1", score=9.0, editorial_fit="geoeconomic-core"),
                make_item("item-2", score=9.0, editorial_fit="broad-geopolitics"),
            ],
            SimpleNamespace(
                runtime=SimpleNamespace(),
                config_path=tmp_path / "config.json",
                config=SimpleNamespace(filtering=SimpleNamespace(ai_score_threshold=7.0)),
            ),
        ),
    )

    result = asyncio.run(service.filter_items(run_id="run-editorial-fit", topic_dedup=False))

    assert result["kept"] == 1
    assert service.run_store.load_items("run-editorial-fit", "filtered")[0]["id"] == "item-1"


def test_score_items_uses_public_pre_score_dedup_api(tmp_path: Path, monkeypatch) -> None:
    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")
    service.run_store.create_run("run-pre-score-dedup")
    monkeypatch.setattr("src.mcp.service.make_storage", lambda runtime, config_path: object())

    class FakeOrchestrator:
        def merge_pre_score_duplicates(self, items):  # type: ignore[no-untyped-def]
            return items[:1]

    class FakeAnalyzer:
        def __init__(self, client):  # type: ignore[no-untyped-def]
            pass

        async def analyze_batch(self, items):  # type: ignore[no-untyped-def]
            for item in items:
                item.ai_score = 8.0
            return items

    monkeypatch.setattr(
        "src.mcp.service.make_orchestrator",
        lambda runtime, config, storage: FakeOrchestrator(),
    )
    monkeypatch.setattr(
        service,
        "_load_stage_items",
        lambda **kwargs: (
            [make_item("item-1"), make_item("item-2")],
            SimpleNamespace(
                runtime=SimpleNamespace(
                    create_ai_client=lambda config: object(),
                    ContentAnalyzer=FakeAnalyzer,
                ),
                config_path=tmp_path / "config.json",
                config=SimpleNamespace(
                    ai=SimpleNamespace(),
                    filtering=SimpleNamespace(ai_score_threshold=7.0),
                ),
            ),
        ),
    )

    result = asyncio.run(service.score_items(run_id="run-pre-score-dedup"))

    assert result["scored"] == 1
    assert result["pre_score_dedup_removed"] == 1
    assert service.run_store.load_items("run-pre-score-dedup", "scored")[0]["id"] == "item-1"
