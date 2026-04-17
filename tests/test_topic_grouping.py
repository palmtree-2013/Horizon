from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

from src.ai.summarizer import DailySummarizer
from src.models import ContentItem, SourceType
from src.orchestrator import HorizonOrchestrator


def make_item(
    item_id: str,
    title: str,
    url: str,
    score: float,
    summary: str,
    tags: list[str],
    content: str,
) -> ContentItem:
    item = ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title=title,
        url=url,
        content=content,
        author="tester",
        published_at=datetime.now(timezone.utc),
    )
    item.ai_score = score
    item.ai_editorial_fit = "geoeconomic-core"
    item.ai_summary = summary
    item.ai_tags = tags
    return item


def test_merge_topic_duplicates_groups_closely_related_items(monkeypatch) -> None:
    class FakeClient:
        async def complete(self, system, user, temperature):  # type: ignore[no-untyped-def]
            return '{"duplicates": [[0, 1]]}'

    monkeypatch.setattr("src.orchestrator.create_ai_client", lambda config: FakeClient())

    orchestrator = HorizonOrchestrator(SimpleNamespace(ai=SimpleNamespace(), email=None), SimpleNamespace())
    primary = make_item(
        "item-1",
        "US blockade of Hormuz tests China's restraint",
        "https://example.com/hormuz-1",
        9.0,
        "The blockade raises pressure on China and oil flows.",
        ["Hormuz", "China", "energy security"],
        "Primary content",
    )
    primary.metadata["sources"] = [{"url": str(primary.url), "title": primary.title}]

    related = make_item(
        "item-2",
        "France, UK to host talks on potential multinational mission to Hormuz",
        "https://example.com/hormuz-2",
        8.0,
        "Europe plans a defensive mission around the same Hormuz crisis.",
        ["Hormuz", "France-UK", "maritime security"],
        "Related content",
    )

    merged = asyncio.run(orchestrator.merge_topic_duplicates([primary, related]))

    assert len(merged) == 1
    item = merged[0]
    assert item.ai_score == 9.0
    assert "Europe plans a defensive mission" in (item.ai_summary or "")
    assert item.ai_tags == [
        "Hormuz",
        "China",
        "energy security",
        "France-UK",
        "maritime security",
    ]
    assert "Related content" in (item.content or "")
    assert item.metadata["cluster_member_count"] == 2
    assert item.metadata["cluster_titles"] == [primary.title, related.title]
    assert item.metadata["cluster_references"] == [
        {"url": "https://example.com/hormuz-1", "title": primary.title},
        {"url": "https://example.com/hormuz-2", "title": related.title},
    ]
    assert item.metadata["sources"] == item.metadata["cluster_references"]


def test_merge_topic_duplicates_catches_near_duplicate_outlet_rewrites(monkeypatch) -> None:
    class FakeClient:
        async def complete(self, system, user, temperature):  # type: ignore[no-untyped-def]
            return '{"duplicates": []}'

    monkeypatch.setattr("src.orchestrator.create_ai_client", lambda config: FakeClient())

    orchestrator = HorizonOrchestrator(SimpleNamespace(ai=SimpleNamespace(), email=None), SimpleNamespace())
    primary = make_item(
        "item-1",
        "IMF, World Bank restore relations with Venezuela",
        "https://example.com/venezuela-1",
        8.0,
        "The institutions resume ties with Venezuela.",
        ["IMF", "World Bank", "Venezuela"],
        "Primary content",
    )
    related = make_item(
        "item-2",
        "IMF, World Bank restore ties with Venezuela",
        "https://example.com/venezuela-2",
        7.0,
        "A second outlet reports the same restoration of ties.",
        ["IMF", "World Bank", "Venezuela"],
        "Related content",
    )

    merged = asyncio.run(orchestrator.merge_topic_duplicates([primary, related]))

    assert len(merged) == 1
    assert merged[0].metadata["cluster_member_count"] == 2


def test_merge_topic_duplicates_keeps_conflicting_actions_separate(monkeypatch) -> None:
    class FakeClient:
        async def complete(self, system, user, temperature):  # type: ignore[no-untyped-def]
            return '{"duplicates": []}'

    monkeypatch.setattr("src.orchestrator.create_ai_client", lambda config: FakeClient())

    orchestrator = HorizonOrchestrator(SimpleNamespace(ai=SimpleNamespace(), email=None), SimpleNamespace())
    first = make_item(
        "item-1",
        "EU imposes new sanctions on Venezuela banks",
        "https://example.com/sanctions-impose",
        8.0,
        "The EU imposes a new sanctions package.",
        ["EU", "sanctions", "Venezuela"],
        "First content",
    )
    second = make_item(
        "item-2",
        "EU lifts sanctions on Venezuela banks",
        "https://example.com/sanctions-lift",
        8.0,
        "The EU removes the sanctions package.",
        ["EU", "sanctions", "Venezuela"],
        "Second content",
    )

    merged = asyncio.run(orchestrator.merge_topic_duplicates([first, second]))

    assert len(merged) == 2


def test_merge_topic_duplicates_rejects_unsupported_ai_group(monkeypatch) -> None:
    class FakeClient:
        async def complete(self, system, user, temperature):  # type: ignore[no-untyped-def]
            return '{"duplicates": [[0, 1]]}'

    monkeypatch.setattr("src.orchestrator.create_ai_client", lambda config: FakeClient())

    orchestrator = HorizonOrchestrator(SimpleNamespace(ai=SimpleNamespace(), email=None), SimpleNamespace())
    first = make_item(
        "item-1",
        "IMF, World Bank restore relations with Venezuela",
        "https://example.com/imf-venezuela",
        8.0,
        "The IMF and World Bank restore relations with Venezuela.",
        ["IMF", "World Bank", "Venezuela"],
        "First content",
    )
    second = make_item(
        "item-2",
        "Why Coutts is making an unexpected play for video games",
        "https://example.com/coutts-games",
        8.0,
        "A bank explores a consumer gaming opportunity.",
        ["banking", "gaming", "consumer"],
        "Second content",
    )

    merged = asyncio.run(orchestrator.merge_topic_duplicates([first, second]))

    assert len(merged) == 2


def test_merge_pre_score_duplicates_merges_same_title_across_feeds() -> None:
    orchestrator = HorizonOrchestrator(SimpleNamespace(ai=SimpleNamespace(), email=None), SimpleNamespace())

    primary = make_item(
        "item-1",
        "EU agrees on new sanctions package",
        "https://example.com/sanctions-1",
        0.0,
        "",
        [],
        "Primary content",
    )
    primary.metadata["feed_name"] = "Feed A"

    related = make_item(
        "item-2",
        "EU agrees on new sanctions package!",
        "https://example.com/sanctions-2",
        0.0,
        "",
        [],
        "Related content",
    )
    related.metadata["feed_name"] = "Feed B"

    merged = orchestrator.merge_pre_score_duplicates([primary, related])

    assert len(merged) == 1
    item = merged[0]
    assert item.metadata["pre_score_duplicate_count"] == 2
    assert item.metadata["pre_score_titles"] == [
        "EU agrees on new sanctions package",
        "EU agrees on new sanctions package!",
    ]
    assert item.metadata["sources"] == [
        {"url": "https://example.com/sanctions-1", "title": "EU agrees on new sanctions package"},
        {"url": "https://example.com/sanctions-2", "title": "EU agrees on new sanctions package!"},
    ]
    assert "Related content" in (item.content or "")


def test_merge_pre_score_duplicates_keeps_same_title_from_same_feed_separate() -> None:
    orchestrator = HorizonOrchestrator(SimpleNamespace(ai=SimpleNamespace(), email=None), SimpleNamespace())

    first = make_item(
        "item-1",
        "Live updates from summit",
        "https://example.com/live-1",
        0.0,
        "",
        [],
        "First content",
    )
    first.metadata["feed_name"] = "Feed A"

    second = make_item(
        "item-2",
        "Live updates from summit",
        "https://example.com/live-2",
        0.0,
        "",
        [],
        "Second content",
    )
    second.metadata["feed_name"] = "Feed A"

    merged = orchestrator.merge_pre_score_duplicates([first, second])

    assert len(merged) == 2


def test_summary_references_include_cluster_links_and_enrichment_sources() -> None:
    item = make_item(
        "item-1",
        "Clustered topic",
        "https://example.com/clustered-topic",
        8.5,
        "Combined summary",
        ["tag1", "tag2"],
        "content",
    )
    item.metadata["cluster_references"] = [
        {"url": "https://example.com/source-a", "title": "Source A"},
        {"url": "https://example.com/source-b", "title": "Source B"},
    ]
    item.metadata["sources"] = [
        {"url": "https://example.com/source-b", "title": "Source B"},
        {"url": "https://example.com/context-c", "title": "Context C"},
    ]

    markdown = asyncio.run(
        DailySummarizer().generate_summary(
            [item],
            date="2026-04-14",
            total_fetched=2,
            language="en",
        )
    )

    assert "Source A" in markdown
    assert "Source B" in markdown
    assert "Context C" in markdown
    assert markdown.count("https://example.com/source-b") == 1
