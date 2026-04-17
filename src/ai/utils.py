"""Shared AI utility functions."""

import json
import math
import re
from typing import Any, Optional

EDITORIAL_FIT_CORE = "geoeconomic-core"
EDITORIAL_FIT_LINKED = "geoeconomic-linked"
EDITORIAL_FIT_BROAD = "broad-geopolitics"
EDITORIAL_FIT_OFF_TOPIC = "off-topic"


def parse_json_response(response: str) -> Optional[dict]:
    """Try multiple strategies to extract a JSON object from an AI response.

    Returns the parsed dict, or None if all strategies fail.
    """
    text = response.strip()

    # Strategy 1: direct parse
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        pass

    # Strategy 2: extract from ```json ... ``` code block
    if "```json" in text:
        try:
            json_str = text.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError, IndexError):
            pass

    # Strategy 3: extract from ``` ... ``` code block
    if "```" in text:
        try:
            json_str = text.split("```")[1].split("```")[0].strip()
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError, IndexError):
            pass

    # Strategy 4: find the first { ... } block using brace matching
    start = text.find("{")
    if start != -1:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start : i + 1])
                    except (json.JSONDecodeError, ValueError):
                        break

    # Strategy 5: regex extraction as last resort
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except (json.JSONDecodeError, ValueError):
            pass

    return None


def normalize_editorial_fit(value: str | None) -> str | None:
    """Normalize editorial-fit labels returned by the model."""
    if not value:
        return None

    normalized = re.sub(r"[^a-z]+", "-", value.strip().lower()).strip("-")
    aliases = {
        "geoeconomic-core": EDITORIAL_FIT_CORE,
        "geoeconomics-core": EDITORIAL_FIT_CORE,
        "core-geoeconomic": EDITORIAL_FIT_CORE,
        "core": EDITORIAL_FIT_CORE,
        "geoeconomic-linked": EDITORIAL_FIT_LINKED,
        "geoeconomics-linked": EDITORIAL_FIT_LINKED,
        "geoeconomic-link": EDITORIAL_FIT_LINKED,
        "linked": EDITORIAL_FIT_LINKED,
        "strategic-with-economic-link": EDITORIAL_FIT_LINKED,
        "broad-geopolitics": EDITORIAL_FIT_BROAD,
        "broad-geopolitical": EDITORIAL_FIT_BROAD,
        "broad-geopolitic": EDITORIAL_FIT_BROAD,
        "general-geopolitics": EDITORIAL_FIT_BROAD,
        "geopolitics": EDITORIAL_FIT_BROAD,
        "off-topic": EDITORIAL_FIT_OFF_TOPIC,
        "offtopic": EDITORIAL_FIT_OFF_TOPIC,
        "domestic": EDITORIAL_FIT_OFF_TOPIC,
        "noise": EDITORIAL_FIT_OFF_TOPIC,
    }
    if normalized in aliases:
        return aliases[normalized]

    if "core" in normalized:
        return EDITORIAL_FIT_CORE
    if "linked" in normalized or "economic-link" in normalized:
        return EDITORIAL_FIT_LINKED
    if "geopolitic" in normalized or "foreign-affairs" in normalized:
        return EDITORIAL_FIT_BROAD
    if "off" in normalized or "noise" in normalized or "domestic" in normalized:
        return EDITORIAL_FIT_OFF_TOPIC
    return None


def clamp_score_for_editorial_fit(score: float, editorial_fit: str | None) -> float:
    """Enforce score ceilings for non-geoeconomic buckets."""
    fit = normalize_editorial_fit(editorial_fit)
    if fit == EDITORIAL_FIT_BROAD:
        return min(score, 6.0)
    if fit == EDITORIAL_FIT_OFF_TOPIC:
        return min(score, 2.0)
    return score


def is_editorially_eligible(editorial_fit: str | None) -> bool:
    """Return whether an item is allowed into the final digest.

    Missing labels are treated as eligible for backwards compatibility with
    older stored runs that were scored before this field existed.
    """
    fit = normalize_editorial_fit(editorial_fit)
    return fit is None or fit in {EDITORIAL_FIT_CORE, EDITORIAL_FIT_LINKED}


def is_editorially_selectable(editorial_fit: str | None) -> bool:
    """Return whether an item can be considered for adaptive backfill."""
    fit = normalize_editorial_fit(editorial_fit)
    return fit is None or fit != EDITORIAL_FIT_OFF_TOPIC


def editorial_priority(editorial_fit: str | None) -> int:
    """Return sort priority for editorial-fit buckets."""
    fit = normalize_editorial_fit(editorial_fit)
    if fit == EDITORIAL_FIT_CORE:
        return 3
    if fit == EDITORIAL_FIT_LINKED:
        return 2
    if fit == EDITORIAL_FIT_BROAD:
        return 1
    return 0


def target_keep_count(total_items: int, keep_ratio: float, max_items: int) -> int:
    """Compute adaptive keep count from total analyzed items."""
    if total_items <= 0 or max_items <= 0:
        return 0

    normalized_ratio = keep_ratio if keep_ratio > 0 else 1.0
    target = max(1, math.ceil(total_items * normalized_ratio))
    return min(total_items, max_items, target)


def select_important_items(
    items: list[Any],
    score_threshold: float,
    keep_ratio: float = 0.2,
    max_items: int = 20,
) -> tuple[list[Any], dict[str, int]]:
    """Select important items with adaptive backfill.

    Preferred items are editor-approved core/linked stories above threshold.
    If they are fewer than the target count, backfill from the highest-scoring
    non-off-topic remainder until the adaptive target is reached.
    """
    candidates = [
        item
        for item in items
        if (item.ai_score or 0) > 0 and is_editorially_selectable(getattr(item, "ai_editorial_fit", None))
    ]
    candidates.sort(
        key=lambda item: (
            float(getattr(item, "ai_score", 0) or 0),
            editorial_priority(getattr(item, "ai_editorial_fit", None)),
        ),
        reverse=True,
    )

    target_count = target_keep_count(len(items), keep_ratio, max_items)
    preferred_items = [
        item
        for item in candidates
        if (item.ai_score or 0) >= score_threshold and is_editorially_eligible(getattr(item, "ai_editorial_fit", None))
    ]

    if target_count == 0:
        return [], {
            "target_count": 0,
            "preferred_count": 0,
            "backfilled_count": 0,
            "selectable_count": len(candidates),
        }

    if len(preferred_items) >= target_count:
        selected = preferred_items[:target_count]
        return selected, {
            "target_count": target_count,
            "preferred_count": len(preferred_items),
            "backfilled_count": 0,
            "selectable_count": len(candidates),
        }

    selected = list(preferred_items)
    selected_ids = {item.id for item in selected}
    for item in candidates:
        if item.id in selected_ids:
            continue
        selected.append(item)
        selected_ids.add(item.id)
        if len(selected) >= target_count:
            break

    return selected, {
        "target_count": target_count,
        "preferred_count": len(preferred_items),
        "backfilled_count": max(0, len(selected) - len(preferred_items)),
        "selectable_count": len(candidates),
    }
