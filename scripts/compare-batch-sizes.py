"""Compare analyzer LLM request counts for different batch sizes.

This is a local smoke test: it uses the real ContentAnalyzer batching logic
with a fake AI client, so it does not call any online model provider.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from datetime import datetime, timezone

from src.ai.analyzer import ContentAnalyzer
from src.models import ContentItem, SourceType


class FakeBatchClient:
    """Fake AI client that returns valid analysis JSON for requested item IDs."""

    def __init__(self, fail_batch_size_over: int | None = None):
        self.calls = 0
        self.item_ids_per_call: list[list[str]] = []
        self.fail_batch_size_over = fail_batch_size_over

    async def complete(self, system: str, user: str, temperature: float = 0.0) -> str:
        self.calls += 1
        ids = re.findall(r"^ID: (.+)$", user, flags=re.MULTILINE)
        if not ids:
            ids = ["single-item"]
        self.item_ids_per_call.append(ids)

        if self.fail_batch_size_over is not None and len(ids) > self.fail_batch_size_over:
            return '{"items": []}'

        if ids == ["single-item"]:
            return json.dumps(
                {
                    "editorial_fit": "geoeconomic-core",
                    "score": 8,
                    "reason": "Synthetic single-item fallback.",
                    "summary": "Synthetic summary.",
                    "tags": ["synthetic", "fallback", "test"],
                }
            )

        return json.dumps(
            {
                "items": [
                    {
                        "id": item_id,
                        "editorial_fit": "geoeconomic-core",
                        "score": 8,
                        "reason": "Synthetic batch analysis.",
                        "summary": f"Synthetic summary for {item_id}.",
                        "tags": ["synthetic", "batch", "test"],
                    }
                    for item_id in ids
                ]
            }
        )


def make_items(count: int) -> list[ContentItem]:
    now = datetime.now(timezone.utc)
    return [
        ContentItem(
            id=f"item-{idx + 1}",
            source_type=SourceType.RSS,
            title=f"Trade policy development {idx + 1}",
            url=f"https://example.com/story-{idx + 1}",
            content=(
                "A synthetic geoeconomic story about trade, sanctions, "
                "energy security, and cross-border market effects."
            ),
            author="synthetic",
            published_at=now,
            metadata={"feed_name": "Synthetic Feed", "category": "global-economy"},
        )
        for idx in range(count)
    ]


async def run_case(item_count: int, batch_size: int, fail_batch_size_over: int | None) -> dict:
    client = FakeBatchClient(fail_batch_size_over=fail_batch_size_over)
    analyzer = ContentAnalyzer(client)
    items = make_items(item_count)
    analyzed = await analyzer.analyze_batch(items, batch_size=batch_size)
    successful = sum(1 for item in analyzed if (item.ai_score or 0) > 0)
    return {
        "batch_size": batch_size,
        "items": item_count,
        "llm_calls": client.calls,
        "successful_items": successful,
        "call_shapes": [len(ids) for ids in client.item_ids_per_call],
    }


async def main() -> None:
    parser = argparse.ArgumentParser(description="Compare ContentAnalyzer batch-size call counts.")
    parser.add_argument("--items", type=int, default=80, help="Synthetic item count.")
    parser.add_argument(
        "--batch-sizes",
        default="5,10,20,40",
        help="Comma-separated batch sizes to test.",
    )
    parser.add_argument(
        "--fail-batch-size-over",
        type=int,
        default=None,
        help="Simulate malformed batch output when a batch has more than N items.",
    )
    args = parser.parse_args()

    batch_sizes = [int(value.strip()) for value in args.batch_sizes.split(",") if value.strip()]
    results = [
        await run_case(args.items, batch_size, args.fail_batch_size_over)
        for batch_size in batch_sizes
    ]

    print(json.dumps({"results": results}, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
