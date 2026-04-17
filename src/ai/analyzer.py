"""Content analysis using AI."""

from typing import List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, MofNCompleteColumn

from .client import AIClient
from .prompts import CONTENT_ANALYSIS_SYSTEM, CONTENT_ANALYSIS_USER
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
    def _parse_json_response(response: str) -> Optional[dict]:
        """Try multiple strategies to extract a JSON object from an AI response.

        Returns the parsed dict, or None if all strategies fail.
        """
        return parse_json_response(response)

    async def analyze_batch(
        self,
        items: List[ContentItem],
        batch_size: int = 10
    ) -> List[ContentItem]:
        analyzed_items = []

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
                for item in batch:
                    try:
                        await self._analyze_item(item)
                        analyzed_items.append(item)
                    except Exception as e:
                        print(f"Error analyzing item {item.id}: {e}")
                        item.ai_score = 0.0
                        item.ai_editorial_fit = EDITORIAL_FIT_OFF_TOPIC
                        item.ai_reason = "Analysis failed"
                        item.ai_summary = item.title
                        analyzed_items.append(item)
                    progress.advance(task)

        return analyzed_items

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
            item.ai_score = 0.0
            item.ai_editorial_fit = EDITORIAL_FIT_OFF_TOPIC
            item.ai_reason = "Analysis response parse failed"
            item.ai_summary = item.title
            item.ai_tags = []
            return

        # Update item with analysis results
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
