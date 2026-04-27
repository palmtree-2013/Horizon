from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from src.ai.analyzer import ContentAnalyzer
from src.models import ContentItem, SourceType


def make_item() -> ContentItem:
    return ContentItem(
        id="item-1",
        source_type=SourceType.RSS,
        title="Activist arrested after backing coup attempt",
        url="https://example.com/story",
        content="Authorities arrested an activist after he backed a coup attempt.",
        author="tester",
        published_at=datetime.now(timezone.utc),
        metadata={
            "feed_name": "BBC News World",
            "category": "world-news",
            "tags": ["Benin", "Africa"],
        },
    )


def test_analyzer_clamps_broad_geopolitics_scores() -> None:
    class FakeClient:
        async def complete(self, system, user, temperature):  # type: ignore[no-untyped-def]
            return """
            {
              "editorial_fit": "broad-geopolitics",
              "score": 9,
              "reason": "Important political event but not geoeconomic.",
              "summary": "A political arrest follows a coup-related dispute.",
              "tags": ["Benin", "arrest", "politics"]
            }
            """

    item = make_item()

    analyzed = asyncio.run(ContentAnalyzer(FakeClient()).analyze_batch([item]))

    assert analyzed[0].ai_editorial_fit == "broad-geopolitics"
    assert analyzed[0].ai_score == 6.0


def test_analyzer_includes_source_context_and_defaults_missing_fit() -> None:
    seen_user_prompt: dict[str, str] = {}

    class FakeClient:
        async def complete(self, system, user, temperature):  # type: ignore[no-untyped-def]
            seen_user_prompt["user"] = user
            return """
            {
              "score": 7,
              "reason": "No fit label returned.",
              "summary": "A generic world-news story.",
              "tags": ["world", "news", "politics"]
            }
            """

    item = make_item()

    analyzed = asyncio.run(ContentAnalyzer(FakeClient()).analyze_batch([item]))

    assert "Source Context: feed: BBC News World; category: world-news; entry tags: Benin, Africa" in seen_user_prompt["user"]
    assert analyzed[0].ai_editorial_fit == "broad-geopolitics"
    assert analyzed[0].ai_score == 6.0


def test_analyzer_downgrades_generic_question_market_commentary() -> None:
    class FakeClient:
        async def complete(self, system, user, temperature):  # type: ignore[no-untyped-def]
            return """
            {
              "editorial_fit": "geoeconomic-core",
              "score": 8,
              "reason": "Markets are moving higher.",
              "summary": "A market rally continues.",
              "tags": ["markets", "equities", "rally"]
            }
            """

    item = make_item()
    item.title = "What kind of rally is this?"
    item.content = "Equity investors are debating whether the rally can continue."

    analyzed = asyncio.run(ContentAnalyzer(FakeClient()).analyze_batch([item]))

    assert analyzed[0].ai_editorial_fit == "off-topic"
    assert analyzed[0].ai_score == 2.0


def test_analyzer_downgrades_private_sector_deal_without_public_interest() -> None:
    class FakeClient:
        async def complete(self, system, user, temperature):  # type: ignore[no-untyped-def]
            return """
            {
              "editorial_fit": "geoeconomic-core",
              "score": 8,
              "reason": "A large consumer deal reflects regional consolidation and faces EU competition concerns.",
              "summary": "Uber expands its stake in Delivery Hero in a cross-border deal after EU competition concerns.",
              "tags": ["M&A", "consumer", "corporate"]
            }
            """

    item = make_item()
    item.title = "Uber expands its stake in Delivery Hero in €270mn deal"
    item.content = "The transaction expands Uber's ownership in Delivery Hero."

    analyzed = asyncio.run(ContentAnalyzer(FakeClient()).analyze_batch([item]))

    assert analyzed[0].ai_editorial_fit == "off-topic"
    assert analyzed[0].ai_score == 2.0


def test_analyzer_scores_multiple_items_in_one_batch_call() -> None:
    calls: list[str] = []

    class FakeClient:
        async def complete(self, system, user, temperature):  # type: ignore[no-untyped-def]
            calls.append(user)
            return """
            {
              "items": [
                {
                  "id": "item-1",
                  "editorial_fit": "geoeconomic-core",
                  "score": 8,
                  "reason": "A trade policy item.",
                  "summary": "A trade policy shift matters for markets.",
                  "tags": ["trade", "policy", "markets"]
                },
                {
                  "id": "item-2",
                  "editorial_fit": "geoeconomic-linked",
                  "score": 7,
                  "reason": "An energy-security item.",
                  "summary": "An energy development affects regional supply.",
                  "tags": ["energy", "security", "supply"]
                }
              ]
            }
            """

    first = make_item()
    second = make_item()
    second.id = "item-2"
    second.title = "Energy disruption threatens regional supply"

    analyzed = asyncio.run(ContentAnalyzer(FakeClient()).analyze_batch([first, second], batch_size=10))

    assert len(calls) == 1
    assert "ID: item-1" in calls[0]
    assert "ID: item-2" in calls[0]
    assert [item.ai_score for item in analyzed] == [8.0, 7.0]


def test_analyzer_repairs_missing_object_boundary_after_tags() -> None:
    response = """
    {
      "type": "object",
      "items": [
        {
          "id": "item-1",
          "editorial_fit": "geoeconomic-linked",
          "score": 7,
          "reason": "Shipping risk.",
          "summary": "Piracy threatens shipping.",
          "tags": ["shipping", "risk"],
          "id": "item-2",
          "editorial_fit": "broad-geopolitics",
          "score": 4,
          "reason": "Mostly geopolitical.",
          "summary": "Military spending rises.",
          "tags": ["military", "spending"]
        }
      ]
    }
    """

    parsed = ContentAnalyzer._parse_batch_response(response)

    assert parsed is not None
    assert [entry["id"] for entry in parsed] == ["item-1", "item-2"]


def test_analyzer_extracts_complete_objects_from_truncated_batch_response() -> None:
    response = """
    {"items": [
      {
        "id": "item-1",
        "editorial_fit": "broad-geopolitics",
        "score": 5,
        "reason": "Mostly geopolitical.",
        "summary": "Military spending rises.",
        "tags": ["military", "spending"]
      },
      {
        "id": "item-2",
        "editorial_fit": "broad-geopolitics",
        "score": 4,
        "reason": "Military
    """

    parsed = ContentAnalyzer._parse_batch_response(response)

    assert parsed is not None
    assert [entry["id"] for entry in parsed] == ["item-1"]
