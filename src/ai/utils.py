"""Shared AI utility functions."""

import json
import re
from typing import Optional

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
