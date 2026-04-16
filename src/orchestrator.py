"""Main orchestrator coordinating the entire workflow."""

import asyncio
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import re
from typing import List, Dict, Any
from urllib.parse import urlparse
import httpx
from rich.console import Console

from .models import Config, ContentItem
from .storage.manager import StorageManager
from .services.emailer import EmailManager
from .scrapers.github import GitHubScraper
from .scrapers.hackernews import HackerNewsScraper
from .scrapers.rss import RSSScraper
from .scrapers.reddit import RedditScraper
from .scrapers.telegram import TelegramScraper
from .ai.client import create_ai_client
from .ai.analyzer import ContentAnalyzer
from .ai.summarizer import DailySummarizer
from .ai.enricher import ContentEnricher
from .ai.tokens import get_usage_snapshot


class HorizonOrchestrator:
    """Orchestrates the complete workflow for content aggregation and analysis."""

    def __init__(self, config: Config, storage: StorageManager):
        """Initialize orchestrator.

        Args:
            config: Application configuration
            storage: Storage manager
        """
        self.config = config
        self.storage = storage
        self.console = Console()
        self.email_manager = EmailManager(config.email, console=self.console) if config.email else None

    async def run(self, force_hours: int = None, include_background: bool = False) -> None:
        """Execute the complete workflow.

        Args:
            force_hours: Optional override for time window in hours
            include_background: Whether enrichment should generate background sections
        """
        self.console.print("[bold cyan]🌅 Horizon - Starting aggregation...[/bold cyan]\n")

        # Check email subscriptions if configured
        if self.email_manager and self.config.email and self.config.email.enabled:
            self.console.print("📧 Checking for new email subscriptions...")
            self.email_manager.check_subscriptions(self.storage)

        try:
            # 1. Determine time window
            since = self._determine_time_window(force_hours)
            self.console.print(f"📅 Fetching content since: {since.strftime('%Y-%m-%d %H:%M:%S')}\n")

            # 2. Fetch content from all sources
            all_items = await self.fetch_all_sources(since)
            self.console.print(f"📥 Fetched {len(all_items)} items from all sources\n")

            if not all_items:
                self.console.print("[yellow]No new content found. Exiting.[/yellow]")
                return

            # 3. Merge cross-source duplicates (same URL from different sources)
            merged_items = self.merge_cross_source_duplicates(all_items)
            if len(merged_items) < len(all_items):
                self.console.print(
                    f"🔗 Merged {len(all_items) - len(merged_items)} cross-source duplicates "
                    f"→ {len(merged_items)} unique items\n"
                )

            # 3.5 Merge exact or near-exact title duplicates before scoring
            pre_scored_items = self.merge_pre_score_duplicates(merged_items)
            if len(pre_scored_items) < len(merged_items):
                self.console.print(
                    f"🪶 Merged {len(merged_items) - len(pre_scored_items)} pre-score title duplicates "
                    f"→ {len(pre_scored_items)} items to score\n"
                )

            # 4. Analyze with AI
            analyzed_items = await self._analyze_content(pre_scored_items)
            self.console.print(f"🤖 Analyzed {len(analyzed_items)} items with AI\n")

            # 5. Filter by score threshold
            threshold = self.config.filtering.ai_score_threshold
            important_items = [
                item for item in analyzed_items
                if item.ai_score and item.ai_score >= threshold
            ]
            important_items.sort(key=lambda x: x.ai_score or 0, reverse=True)

            self.console.print(
                f"⭐️ {len(important_items)} items scored ≥ {threshold}\n"
            )

            # 5.5 Semantic deduplication: drop items covering the same topic
            deduped_items = await self.merge_topic_duplicates(important_items)
            if len(deduped_items) < len(important_items):
                self.console.print(
                    f"🧹 Removed {len(important_items) - len(deduped_items)} topic duplicates "
                    f"→ {len(deduped_items)} unique items\n"
                )
            important_items = deduped_items

            # Show per-sub-source selection breakdown
            selected_counts: Dict[str, int] = defaultdict(int)
            for item in important_items:
                key = f"{item.source_type.value}/{self._sub_source_label(item)}"
                selected_counts[key] += 1
            for source_key, count in sorted(selected_counts.items()):
                self.console.print(f"      • {source_key}: {count}")
            self.console.print("")

            # 6. Search related stories + enrich with background knowledge (2nd AI pass)
            await self._enrich_important_items(important_items, include_background=include_background)

            # 7. Generate and save daily summaries for each configured language
            today = datetime.utcnow().strftime("%Y-%m-%d")
            for lang in self.config.ai.languages:
                summary = await self._generate_summary(important_items, today, len(all_items), language=lang)

                # Save to data/summaries/
                summary_path = self.storage.save_daily_summary(today, summary, language=lang)
                self.console.print(f"💾 Saved {lang.upper()} summary to: {summary_path}\n")

                # Copy to docs/ for GitHub Pages
                try:
                    from pathlib import Path

                    post_filename = f"{today}-summary-{lang}.md"
                    posts_dir = Path("docs/_posts")
                    posts_dir.mkdir(parents=True, exist_ok=True)

                    dest_path = posts_dir / post_filename

                    # Add Jekyll front matter
                    front_matter = (
                        "---\n"
                        "layout: default\n"
                        f"title: \"Horizon Summary: {today} ({lang.upper()})\"\n"
                        f"date: {today}\n"
                        f"lang: {lang}\n"
                        "---\n\n"
                    )

                    # Strip leading H1 header to avoid duplication with Jekyll title
                    summary_content = summary
                    first_line = summary_content.strip().split("\n")[0]
                    if first_line.startswith("# "):
                        parts = summary_content.split("\n", 1)
                        if len(parts) > 1:
                            summary_content = parts[1].strip()

                    with open(dest_path, "w", encoding="utf-8") as f:
                        f.write(front_matter + summary_content)

                    self.console.print(f"📄 Copied {lang.upper()} summary to GitHub Pages: {dest_path}\n")
                except Exception as e:
                    self.console.print(f"[yellow]⚠️  Failed to copy {lang.upper()} summary to docs/: {e}[/yellow]\n")

                # Send email if configured
                if self.email_manager and self.config.email and self.config.email.enabled:
                    self.console.print(f"📧 Sending {lang.upper()} email summary...")
                    subscribers = self.storage.load_subscribers()
                    subject = f"Horizon Summary ({lang.upper()}) - {today}"
                    self.email_manager.send_daily_summary(summary, subject, subscribers)

            self.console.print("[bold green]✅ Horizon completed successfully![/bold green]")
            usage = get_usage_snapshot()
            if usage.total_tokens > 0:
                self.console.print(
                    f"\n🧮 Token usage this run: "
                    f"{usage.total_tokens} tokens "
                    f"(input: {usage.total_input_tokens}, output: {usage.total_output_tokens})"
                )
                for provider, u in sorted(usage.per_provider.items()):
                    if u.total <= 0:
                        continue
                    self.console.print(
                        f"   • {provider}: {u.total} tokens "
                        f"(in: {u.input_tokens}, out: {u.output_tokens})"
                    )

        except Exception as e:
            self.console.print(f"[bold red]❌ Error: {e}[/bold red]")
            raise

    def _determine_time_window(self, force_hours: int = None) -> datetime:
        if force_hours:
            since = datetime.now(timezone.utc) - timedelta(hours=force_hours)
        else:
            hours = self.config.filtering.time_window_hours
            since = datetime.now(timezone.utc) - timedelta(hours=hours)
        return since

    async def fetch_all_sources(self, since: datetime) -> List[ContentItem]:
        """Fetch content from all configured sources.

        This is a stable stage entry point for integrations such as MCP.

        Args:
            since: Fetch items published after this time

        Returns:
            List[ContentItem]: All fetched items
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            tasks = []

            # GitHub sources
            if self.config.sources.github:
                github_scraper = GitHubScraper(self.config.sources.github, client)
                tasks.append(self._fetch_with_progress("GitHub", github_scraper, since))

            # Hacker News
            if self.config.sources.hackernews.enabled:
                hn_scraper = HackerNewsScraper(self.config.sources.hackernews, client)
                tasks.append(self._fetch_with_progress("Hacker News", hn_scraper, since))

            # RSS feeds
            if self.config.sources.rss:
                rss_scraper = RSSScraper(self.config.sources.rss, client)
                tasks.append(self._fetch_with_progress("RSS Feeds", rss_scraper, since))

            # Reddit
            if self.config.sources.reddit.enabled:
                reddit_scraper = RedditScraper(self.config.sources.reddit, client)
                tasks.append(self._fetch_with_progress("Reddit", reddit_scraper, since))

            # Telegram
            if self.config.sources.telegram.enabled:
                telegram_scraper = TelegramScraper(self.config.sources.telegram, client)
                tasks.append(self._fetch_with_progress("Telegram", telegram_scraper, since))

            # Fetch all concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Flatten results
            all_items = []
            for result in results:
                if isinstance(result, Exception):
                    self.console.print(f"[red]Error fetching source: {result}[/red]")
                elif isinstance(result, list):
                    all_items.extend(result)

            return all_items

    async def _fetch_with_progress(self, name: str, scraper, since: datetime) -> List[ContentItem]:
        """Fetch from a scraper with progress indication.

        Args:
            name: Source name for display
            scraper: Scraper instance
            since: Fetch items after this time

        Returns:
            List[ContentItem]: Fetched items
        """
        self.console.print(f"🔍 Fetching from {name}...")
        items = await scraper.fetch(since)
        self.console.print(f"   Found {len(items)} items from {name}")

        # Show per-sub-source breakdown when there are multiple sub-sources
        sub_counts: Dict[str, int] = defaultdict(int)
        for item in items:
            sub_counts[self._sub_source_label(item)] += 1
        if len(sub_counts) > 1:
            for sub, count in sorted(sub_counts.items()):
                self.console.print(f"      • {sub}: {count}")

        return items

    @staticmethod
    def _sub_source_label(item: ContentItem) -> str:
        """Return a human-readable sub-source label for an item."""
        meta = item.metadata
        if meta.get("subreddit"):
            return f"r/{meta['subreddit']}"
        if meta.get("feed_name"):
            return meta["feed_name"]
        if meta.get("channel"):
            return f"@{meta['channel']}"
        if meta.get("repo"):
            return meta["repo"]
        return item.author or "unknown"

    @staticmethod
    def _normalize_url(url: str) -> str:
        """Normalize URL for duplicate detection."""
        parsed = urlparse(str(url))
        host = parsed.hostname or ""
        if host.startswith("www."):
            host = host[4:]
        path = parsed.path.rstrip("/")
        return f"{host}{path}"

    @staticmethod
    def _normalize_title(title: str) -> str:
        """Normalize titles for cheap pre-score deduplication."""
        normalized = re.sub(r"[^\w]+", " ", title.casefold())
        return re.sub(r"\s+", " ", normalized).strip()

    def merge_cross_source_duplicates(self, items: List[ContentItem]) -> List[ContentItem]:
        """Merge items that point to the same URL from different sources.

        This is a stable stage helper for integrations such as MCP.

        Keeps the item with the richest content and combines metadata.

        Args:
            items: Items to deduplicate

        Returns:
            List[ContentItem]: Deduplicated items
        """
        # Group by normalized URL
        url_groups: Dict[str, List[ContentItem]] = {}
        for item in items:
            key = self._normalize_url(str(item.url))
            url_groups.setdefault(key, []).append(item)

        merged = []
        for key, group in url_groups.items():
            if len(group) == 1:
                merged.append(group[0])
                continue

            # Pick the item with the richest content as primary
            primary = max(group, key=lambda x: len(x.content or ""))

            # Merge metadata and source info from other items
            all_sources = set()
            for item in group:
                all_sources.add(item.source_type.value)
                # Merge metadata (engagement, discussion, etc.)
                for mk, mv in item.metadata.items():
                    if mk not in primary.metadata or not primary.metadata[mk]:
                        primary.metadata[mk] = mv

                # Append content (e.g., comments from another source)
                if item is not primary and item.content:
                    if primary.content and item.content not in primary.content:
                        primary.content = (primary.content or "") + f"\n\n--- From {item.source_type.value} ---\n" + item.content

            primary.metadata["merged_sources"] = list(all_sources)
            merged.append(primary)

        return merged

    def merge_pre_score_duplicates(self, items: List[ContentItem]) -> List[ContentItem]:
        """Merge exact or near-exact title duplicates before AI scoring.

        This is intentionally conservative. It only merges items whose
        normalized titles match exactly after punctuation/case normalization
        and that came from different sub-sources.
        """
        title_groups: Dict[str, List[ContentItem]] = {}
        for item in items:
            key = self._normalize_title(item.title)
            if not key:
                key = f"item:{item.id}"
            title_groups.setdefault(key, []).append(item)

        merged: List[ContentItem] = []
        for group in title_groups.values():
            if len(group) == 1:
                merged.append(group[0])
                continue

            sub_sources = {f"{item.source_type.value}/{self._sub_source_label(item)}" for item in group}
            if len(sub_sources) == 1:
                merged.extend(group)
                continue

            primary = max(group, key=lambda x: len(x.content or ""))
            grouped_sources = []
            grouped_titles: list[str] = []
            all_sources = set(primary.metadata.get("merged_sources") or [])

            for item in group:
                all_sources.add(item.source_type.value)
                grouped_sources.append({"url": str(item.url), "title": item.title})
                if item.title not in grouped_titles:
                    grouped_titles.append(item.title)
                for mk, mv in item.metadata.items():
                    if mk not in primary.metadata or not primary.metadata[mk]:
                        primary.metadata[mk] = mv
                if item is not primary and item.content:
                    if not primary.content or item.content not in primary.content:
                        primary.content = (primary.content or "") + f"\n\n--- From {item.source_type.value} ---\n{item.content}"

            primary.metadata["merged_sources"] = list(all_sources)
            primary.metadata["pre_score_duplicate_count"] = len(group)
            primary.metadata["pre_score_titles"] = grouped_titles
            primary.metadata["sources"] = self._merge_reference_lists(
                primary.metadata.get("sources") or [],
                grouped_sources,
            )
            merged.append(primary)

        return merged

    @staticmethod
    def _merge_reference_lists(*reference_lists: list[dict[str, str]]) -> list[dict[str, str]]:
        """Merge link references while preserving order and removing duplicates by URL."""
        merged: list[dict[str, str]] = []
        seen: set[str] = set()

        for refs in reference_lists:
            for ref in refs or []:
                url = str(ref.get("url", "")).strip()
                title = str(ref.get("title", "")).strip()
                if not url or url in seen:
                    continue
                merged.append({"url": url, "title": title or url})
                seen.add(url)

        return merged

    async def merge_topic_duplicates(self, items: List[ContentItem]) -> List[ContentItem]:
        """Merge items covering the same topic using AI semantic deduplication.

        This is a stable stage helper for integrations such as MCP.

        Sends all item titles, tags, and summaries to AI in a single call.
        Items must already be sorted by ai_score descending so that the first
        item in each duplicate group is always the highest-scored one.
        Content, tags, summaries, and references from grouped items are merged
        into the primary so downstream enrichment can summarize the topic
        cluster instead of a single article.

        Falls back to returning items unchanged if the AI call fails.
        """
        if len(items) <= 1:
            return items

        from .ai.prompts import TOPIC_DEDUP_SYSTEM, TOPIC_DEDUP_USER
        from .ai.utils import parse_json_response

        # Build the item list for the prompt
        lines = []
        for i, item in enumerate(items):
            tags = ", ".join(item.ai_tags) if item.ai_tags else "—"
            summary = item.ai_summary or "—"
            lines.append(f"[{i}] {item.title}\n    Tags: {tags}\n    Summary: {summary}")
        items_text = "\n\n".join(lines)

        try:
            ai_client = create_ai_client(self.config.ai)
            response = await ai_client.complete(
                system=TOPIC_DEDUP_SYSTEM,
                user=TOPIC_DEDUP_USER.format(items=items_text),
                temperature=0.0,
            )
            result = parse_json_response(response)
            if result is None:
                self.console.print("[yellow]  dedup: could not parse AI response, skipping[/yellow]")
                return items

            duplicate_groups = result.get("duplicates", [])
        except Exception as e:
            self.console.print(f"[yellow]  dedup: AI call failed ({e}), skipping[/yellow]")
            return items

        if not duplicate_groups:
            return items

        # Build a set of indices to drop (all non-primary duplicates)
        drop_indices: set[int] = set()
        for group in duplicate_groups:
            if not isinstance(group, list) or len(group) < 2:
                continue
            primary_idx = group[0]
            if primary_idx < 0 or primary_idx >= len(items):
                continue
            primary = items[primary_idx]
            grouped_titles: list[str] = [primary.title]
            grouped_summaries: list[str] = [primary.ai_summary] if primary.ai_summary else []
            grouped_tags: list[str] = list(primary.ai_tags)
            grouped_sources: list[dict[str, str]] = [
                {"url": str(primary.url), "title": primary.title}
            ]
            cluster_members: list[dict[str, Any]] = [
                {
                    "title": primary.title,
                    "url": str(primary.url),
                    "source_type": primary.source_type.value,
                    "published_at": primary.published_at.isoformat(),
                }
            ]
            for dup_idx in group[1:]:
                if not isinstance(dup_idx, int) or dup_idx < 0 or dup_idx >= len(items):
                    continue
                if dup_idx == primary_idx:
                    continue
                dup = items[dup_idx]
                grouped_titles.append(dup.title)
                if dup.ai_summary and dup.ai_summary not in grouped_summaries:
                    grouped_summaries.append(dup.ai_summary)
                for tag in dup.ai_tags:
                    if tag not in grouped_tags:
                        grouped_tags.append(tag)
                grouped_sources.append({"url": str(dup.url), "title": dup.title})
                cluster_members.append(
                    {
                        "title": dup.title,
                        "url": str(dup.url),
                        "source_type": dup.source_type.value,
                        "published_at": dup.published_at.isoformat(),
                    }
                )
                primary.ai_score = max(primary.ai_score or 0.0, dup.ai_score or 0.0)
                # Merge comments/content from the duplicate into the primary
                if dup.content:
                    if not primary.content or dup.content not in primary.content:
                        label = dup.source_type.value
                        primary.content = (primary.content or "") + f"\n\n--- From {label} ---\n{dup.content}"
                for mk, mv in dup.metadata.items():
                    if mk not in primary.metadata or not primary.metadata[mk]:
                        primary.metadata[mk] = mv
                self.console.print(
                    f"   [dim]dedup: keep [{primary_idx}] {primary.title}[/dim]\n"
                    f"   [dim]       drop [{dup_idx}] {dup.title}[/dim]"
                )
                drop_indices.add(dup_idx)

            primary.ai_tags = grouped_tags
            if grouped_summaries:
                primary.ai_summary = " ".join(grouped_summaries)
            primary.metadata["cluster_member_count"] = len(cluster_members)
            primary.metadata["cluster_members"] = cluster_members
            primary.metadata["cluster_titles"] = grouped_titles
            primary.metadata["cluster_references"] = self._merge_reference_lists(
                primary.metadata.get("cluster_references") or [],
                grouped_sources,
            )
            primary.metadata["sources"] = self._merge_reference_lists(
                primary.metadata.get("sources") or [],
                primary.metadata["cluster_references"],
            )

        return [item for i, item in enumerate(items) if i not in drop_indices]

    async def _enrich_important_items(self, items: List[ContentItem], include_background: bool = False) -> None:
        """Enrich items with background knowledge (2nd AI pass).

        For each item that passed the score threshold, call AI to generate
        background knowledge based on the item's actual content.

        Args:
            items: Important items to enrich (modified in-place)
            include_background: Whether enrichment should generate background sections
        """
        if not items:
            return

        self.console.print("📚 Enriching with background knowledge...")
        ai_client = create_ai_client(self.config.ai)
        enricher = ContentEnricher(ai_client, include_background=include_background)
        await enricher.enrich_batch(items)
        self.console.print(f"   Enriched {len(items)} items\n")

    async def _analyze_content(self, items: List[ContentItem]) -> List[ContentItem]:
        """Analyze content items with AI.

        Args:
            items: Items to analyze

        Returns:
            List[ContentItem]: Analyzed items
        """
        self.console.print("🤖 Analyzing content with AI...")

        ai_client = create_ai_client(self.config.ai)
        analyzer = ContentAnalyzer(ai_client)

        return await analyzer.analyze_batch(items)

    async def _generate_summary(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        language: str = "en",
    ) -> str:
        """Generate daily summary.

        Args:
            items: Important items to include (already enriched with background/related)
            date: Date string
            total_fetched: Total items fetched
            language: Output language ("en" or "zh")

        Returns:
            str: Markdown summary
        """
        self.console.print("📝 Generating daily summary...")

        summarizer = DailySummarizer()

        return await summarizer.generate_summary(items, date, total_fetched, language=language)
