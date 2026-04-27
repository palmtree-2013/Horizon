"""Content analysis using AI."""

import json
import re
from typing import Any, List, Optional
from tenacity import RetryError, retry, stop_after_attempt, wait_exponential
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, MofNCompleteColumn

from .client import AIClient
from .prompts import CONTENT_ANALYSIS_BATCH_USER, CONTENT_ANALYSIS_SYSTEM, CONTENT_ANALYSIS_USER
from .utils import (
    EDITORIAL_FIT_BROAD,
    EDITORIAL_FIT_OFF_TOPIC,
    clamp_score_for_editorial_fit,
    normalize_editorial_fit,
    parse_json_response,
)
from ..models import ContentItem


class ContentAnalyzer:
    """Analyzes content items using AI to determine importance."""

    def __init__(self, ai_client: AIClient):
        self.client = ai_client

    @staticmethod
    def _format_exception(exc: Exception) -> str:
        """Return the useful underlying exception for tenacity retry failures."""
        if isinstance(exc, RetryError):
            try:
                last_exc = exc.last_attempt.exception()
            except Exception:
                last_exc = None
            if last_exc is not None:
                return f"{type(last_exc).__name__}: {last_exc}"
        return f"{type(exc).__name__}: {exc}"

    @staticmethod
    def _parse_json_response(response: str) -> Optional[dict]:
        """Try multiple strategies to extract a JSON object from an AI response.

        Returns the parsed dict, or None if all strategies fail.
        """
        return parse_json_response(response)

    @staticmethod
    def _parse_batch_response(response: str) -> Optional[list[dict[str, Any]]]:
        """Parse a batch response that may be an object or a bare JSON array."""
        for text in ContentAnalyzer._batch_response_candidates(response):
            parsed = parse_json_response(text)
            if isinstance(parsed, dict):
                for key in ("items", "results", "analyses", "analysis"):
                    value = parsed.get(key)
                    if isinstance(value, list):
                        return [entry for entry in value if isinstance(entry, dict)]
                continue

            for candidate in ContentAnalyzer._array_candidates(text):
                try:
                    value = json.loads(candidate)
                except (json.JSONDecodeError, ValueError):
                    continue
                if isinstance(value, list):
                    return [entry for entry in value if isinstance(entry, dict)]
        partial = ContentAnalyzer._extract_complete_objects(response)
        if partial:
            return partial
        return None

    @staticmethod
    def _batch_response_candidates(response: str) -> list[str]:
        """Return original and lightly repaired batch JSON candidates."""
        text = response.strip()
        candidates = [text]
        if "```json" in text:
            try:
                candidates.append(text.split("```json", 1)[1].split("```", 1)[0].strip())
            except IndexError:
                pass
        if "```" in text:
            try:
                candidates.append(text.split("```", 1)[1].split("```", 1)[0].strip())
            except IndexError:
                pass

        repaired = []
        for candidate in candidates:
            fixed = re.sub(
                r'("tags"\s*:\s*\[[^\]]*\])\s*,\s*("id"\s*:)',
                r'\1}, {\2',
                candidate,
            )
            fixed = re.sub(
                r'("tags"\s*:\s*\[[^\]]*\])\s*,\s*("item_id"\s*:)',
                r'\1}, {\2',
                fixed,
            )
            fixed = re.sub(
                r'("tags"\s*:\s*\[[^\]]*\])\s*,\s*("content_id"\s*:)',
                r'\1}, {\2',
                fixed,
            )
            if fixed != candidate:
                repaired.append(fixed)

        return [*repaired, *candidates]

    @staticmethod
    def _array_candidates(text: str) -> list[str]:
        candidates = []
        match = re.search(r"\[[\s\S]*\]", text)
        if match:
            candidates.append(match.group())
        return candidates

    @staticmethod
    def _extract_complete_objects(response: str) -> list[dict[str, Any]]:
        """Extract complete item objects from a truncated batch JSON response."""
        marker = re.search(r'"(?:items|results|analyses|analysis)"\s*:\s*\[', response)
        start = marker.end() if marker else response.find("[") + 1
        if start <= 0:
            return []

        objects: list[dict[str, Any]] = []
        depth = 0
        obj_start: int | None = None
        in_string = False
        escape = False

        for idx in range(start, len(response)):
            char = response[idx]
            if in_string:
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
                continue
            if char == "{":
                if depth == 0:
                    obj_start = idx
                depth += 1
                continue
            if char == "}":
                if depth <= 0:
                    continue
                depth -= 1
                if depth == 0 and obj_start is not None:
                    obj_text = response[obj_start : idx + 1]
                    for candidate in ContentAnalyzer._batch_response_candidates(obj_text):
                        try:
                            obj = json.loads(candidate)
                        except (json.JSONDecodeError, ValueError):
                            continue
                        if isinstance(obj, dict):
                            objects.append(obj)
                            break
                    obj_start = None

        return objects

    async def analyze_batch(
        self,
        items: List[ContentItem],
        batch_size: int = 10
    ) -> List[ContentItem]:
        analyzed_items = []
        batch_size = max(1, int(batch_size or 1))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("Analyzing", total=len(items))

            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                try:
                    await self._analyze_item_batch(batch)
                    analyzed_items.extend(batch)
                except Exception as e:
                    print(f"Error analyzing batch starting at {i}: {self._format_exception(e)}")
                    await self._analyze_split_fallback(batch)
                    analyzed_items.extend(batch)
                progress.advance(task, advance=len(batch))

        return analyzed_items

    @staticmethod
    def _apply_analysis_defaults(item: ContentItem, reason: str) -> None:
        item.ai_score = 0.0
        item.ai_editorial_fit = EDITORIAL_FIT_OFF_TOPIC
        item.ai_reason = reason
        item.ai_summary = item.title
        item.ai_tags = []

    async def _analyze_split_fallback(self, items: List[ContentItem]) -> None:
        """Recover from failed batch analysis by recursively splitting the batch."""
        if not items:
            return

        if len(items) == 1:
            try:
                await self._analyze_item(items[0])
            except Exception as exc:
                print(f"Error analyzing item {items[0].id}: {exc}")
                self._apply_analysis_defaults(items[0], "Analysis failed")
            return

        midpoint = len(items) // 2
        for sub_batch in (items[:midpoint], items[midpoint:]):
            try:
                await self._analyze_item_batch(sub_batch)
            except Exception as exc:
                print(
                    f"Error analyzing split batch of {len(sub_batch)} item(s): "
                    f"{self._format_exception(exc)}"
                )
                await self._analyze_split_fallback(sub_batch)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=2, max=10)
    )
    async def _analyze_item(self, item: ContentItem) -> None:
        """Analyze a single content item.

        Args:
            item: Content item to analyze (modified in-place)
        """
        # Prepare content section
        content_section = ""
        if item.content:
            # Split off comments if present
            content_text = item.content
            if "--- Top Comments ---" in content_text:
                main, comments_part = content_text.split("--- Top Comments ---", 1)
                content_section = f"Content: {main.strip()[:800]}"
            else:
                content_section = f"Content: {content_text[:1000]}"

        # Prepare discussion section (comments, engagement)
        discussion_parts = []
        if item.content and "--- Top Comments ---" in item.content:
            comments_part = item.content.split("--- Top Comments ---", 1)[1]
            discussion_parts.append(f"Community Comments:\n{comments_part[:1500]}")

        meta = item.metadata
        engagement_items = []
        if meta.get("score"):
            engagement_items.append(f"score: {meta['score']}")
        if meta.get("descendants"):
            engagement_items.append(f"{meta['descendants']} comments")
        if meta.get("favorite_count"):
            engagement_items.append(f"{meta['favorite_count']} likes")
        if meta.get("retweet_count"):
            engagement_items.append(f"{meta['retweet_count']} retweets")
        if meta.get("reply_count"):
            engagement_items.append(f"{meta['reply_count']} replies")
        if meta.get("views"):
            engagement_items.append(f"{meta['views']} views")
        if meta.get("bookmarks"):
            engagement_items.append(f"{meta['bookmarks']} bookmarks")
        if meta.get("upvote_ratio"):
            engagement_items.append(f"upvote ratio: {meta['upvote_ratio']:.0%}")
        if engagement_items:
            discussion_parts.append(f"Engagement: {', '.join(engagement_items)}")
        if meta.get("discussion_url"):
            discussion_parts.append(f"Discussion: {meta['discussion_url']}")
        if meta.get("community_note"):
            discussion_parts.append(f"Community Note: {meta['community_note']}")

        discussion_section = "\n".join(discussion_parts) if discussion_parts else ""
        source_context = self._build_source_context(item)

        # Generate user prompt
        user_prompt = CONTENT_ANALYSIS_USER.format(
            title=item.title,
            source=f"{item.source_type.value}",
            source_context=source_context,
            author=item.author or "Unknown",
            url=str(item.url),
            content_section=content_section,
            discussion_section=discussion_section
        )

        # Get AI completion
        response = await self.client.complete(
            system=CONTENT_ANALYSIS_SYSTEM,
            user=user_prompt,
            temperature=0.0
        )

        # Parse JSON response with robust fallback
        result = self._parse_json_response(response)
        if result is None:
            print(f"Warning: could not parse analysis response for {item.id}, using defaults")
            self._apply_analysis_defaults(item, "Analysis response parse failed")
            return

        # Update item with analysis results
        self._apply_analysis_result(item, result)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=2, max=10)
    )
    async def _analyze_item_batch(self, items: List[ContentItem]) -> None:
        """Analyze multiple content items in one model request."""
        if not items:
            return

        if len(items) == 1:
            await self._analyze_item(items[0])
            return

        item_blocks = []
        for index, item in enumerate(items, start=1):
            content_section = ""
            if item.content:
                content_text = item.content
                if "--- Top Comments ---" in content_text:
                    main, comments_part = content_text.split("--- Top Comments ---", 1)
                    content_section = (
                        f"Content: {main.strip()[:700]}\n"
                        f"Community Comments: {comments_part.strip()[:700]}"
                    )
                else:
                    content_section = f"Content: {content_text[:900]}"

            meta = item.metadata
            engagement_items = []
            for key, label in [
                ("score", "score"),
                ("descendants", "comments"),
                ("favorite_count", "likes"),
                ("retweet_count", "retweets"),
                ("reply_count", "replies"),
                ("views", "views"),
                ("bookmarks", "bookmarks"),
            ]:
                if meta.get(key):
                    engagement_items.append(f"{meta[key]} {label}" if label != "score" else f"score: {meta[key]}")
            if meta.get("upvote_ratio"):
                engagement_items.append(f"upvote ratio: {meta['upvote_ratio']:.0%}")
            discussion_section = f"Engagement: {', '.join(engagement_items)}" if engagement_items else ""

            item_blocks.append(
                "\n".join(
                    part
                    for part in [
                        f"Item {index}",
                        f"ID: {item.id}",
                        f"Title: {item.title}",
                        f"Source: {item.source_type.value}",
                        f"Source Context: {self._build_source_context(item)}",
                        f"Author: {item.author or 'Unknown'}",
                        f"URL: {item.url}",
                        content_section,
                        discussion_section,
                    ]
                    if part
                )
            )

        response = await self.client.complete(
            system=CONTENT_ANALYSIS_SYSTEM,
            user=CONTENT_ANALYSIS_BATCH_USER.format(items="\n\n---\n\n".join(item_blocks)),
            temperature=0.0,
        )

        results = self._parse_batch_response(response)
        if results is None:
            snippet = re.sub(r"\s+", " ", response).strip()[:500]
            raise ValueError(f"Batch analysis response parse failed. Response starts: {snippet}")

        by_id = {
            str(entry.get("id") or entry.get("item_id") or entry.get("content_id")): entry
            for entry in results
            if entry.get("id") or entry.get("item_id") or entry.get("content_id")
        }
        if not by_id and len(results) == len(items):
            for item, entry in zip(items, results):
                self._apply_analysis_result(item, entry)
            return

        missing = []
        for item in items:
            entry = by_id.get(item.id)
            if entry is None:
                missing.append(item.id)
                continue
            self._apply_analysis_result(item, entry)

        if missing:
            if len(missing) < len(items):
                missing_items = [item for item in items if item.id in set(missing)]
                await self._analyze_split_fallback(missing_items)
                return
            raise ValueError(f"Batch analysis missing all item results: {', '.join(missing[:5])}")

    def _apply_analysis_result(self, item: ContentItem, result: dict) -> None:
        """Update one item from a parsed analysis result."""
        raw_score = float(result.get("score", 0) or 0)
        editorial_fit = normalize_editorial_fit(result.get("editorial_fit"))
        if editorial_fit is None:
            editorial_fit = EDITORIAL_FIT_BROAD if raw_score > 0 else EDITORIAL_FIT_OFF_TOPIC
        editorial_fit = self._apply_editorial_guardrails(
            item=item,
            editorial_fit=editorial_fit,
            summary=result.get("summary", item.title),
            reason=result.get("reason", ""),
            tags=result.get("tags", []),
        )
        item.ai_editorial_fit = editorial_fit
        item.ai_score = clamp_score_for_editorial_fit(raw_score, editorial_fit)
        item.ai_reason = result.get("reason", "")
        item.ai_summary = result.get("summary", item.title)
        item.ai_tags = result.get("tags", [])

    @staticmethod
    def _build_source_context(item: ContentItem) -> str:
        """Build concise source metadata for the analysis prompt."""
        meta = item.metadata
        parts = []
        if meta.get("feed_name"):
            parts.append(f"feed: {meta['feed_name']}")
        if meta.get("category"):
            parts.append(f"category: {meta['category']}")
        if meta.get("tags"):
            tags = ", ".join(str(tag) for tag in meta["tags"][:6] if tag)
            if tags:
                parts.append(f"entry tags: {tags}")
        if meta.get("merged_sources"):
            merged = ", ".join(str(source) for source in meta["merged_sources"])
            if merged:
                parts.append(f"merged sources: {merged}")
        return "; ".join(parts) if parts else "none"

    @staticmethod
    def _apply_editorial_guardrails(
        item: ContentItem,
        editorial_fit: str,
        summary: str,
        reason: str,
        tags: list[str],
    ) -> str:
        """Apply deterministic exclusions for recurring non-briefing patterns."""
        combined = " ".join(
            part
            for part in [
                item.title,
                summary,
                reason,
                " ".join(tags),
                item.content or "",
            ]
            if part
        ).casefold()

        public_interest_markers = [
            "antitrust",
            "banking",
            "central bank",
            "competition",
            "critical mineral",
            "currency",
            "debt",
            "derivatives",
            "energy",
            "export control",
            "financial stability",
            "imf",
            "industrial policy",
            "investment screening",
            "oil",
            "private credit",
            "regulator",
            "sanction",
            "shipping",
            "sovereign",
            "state",
            "strait of hormuz",
            "supply chain",
            "tariff",
            "trade",
            "world bank",
        ]
        hard_policy_markers = [
            "central bank",
            "competition chief",
            "critical mineral",
            "energy",
            "export control",
            "financial stability",
            "imf",
            "industrial policy",
            "investment screening",
            "merger rules",
            "national security",
            "regulation",
            "regulator",
            "rules",
            "sanction",
            "shipping",
            "sovereign",
            "state",
            "strait of hormuz",
            "supply chain",
            "systemic risk",
            "tariff",
            "trade",
            "world bank",
        ]
        corporate_deal_markers = [
            "acquisition",
            "deal",
            "m&a",
            "merger",
            "stake",
            "takeover",
        ]

        has_public_interest = any(marker in combined for marker in public_interest_markers)
        has_hard_policy_marker = any(marker in combined for marker in hard_policy_markers)
        has_corporate_deal = any(marker in combined for marker in corporate_deal_markers)

        if item.title.strip().endswith("?") and not has_public_interest:
            return EDITORIAL_FIT_OFF_TOPIC
        if has_corporate_deal and not has_hard_policy_marker:
            return EDITORIAL_FIT_OFF_TOPIC
        return editorial_fit
