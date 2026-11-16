"""Local overlap scores, the judge prompt, and chat-history expiry."""

from __future__ import annotations

import json
import re

JUDGE_SYSTEM_PROMPT = """You compare answers that different AI models gave to the same user prompt.
Return only a JSON object with these keys:
- similarities: array of short strings describing where the answers agree
- differences: array of short strings describing where the answers disagree
- reasoning_quality: an object whose keys are the provider labels you were given, each value a short assessment of clarity and reasoning
- accuracy: a short assessment. If a reference answer is present, compare the answers against it. If no reference answer is present, say that factual accuracy cannot be verified and assess internal consistency only
- caveats: a short string about the limits of this comparison
Do not wrap the JSON in markdown.
"""


def history_expired(last_activity: float | None, now: float, ttl_minutes: int) -> bool:
    """True when an in-memory transcript has passed its idle limit."""
    if last_activity is None or ttl_minutes <= 0:
        return False
    return now - last_activity >= ttl_minutes * 60


def _tokens(text: str) -> set[str]:
    return {word for word in re.findall(r"[a-z0-9']+", text.lower()) if len(word) > 2}


def jaccard_similarity(left: str, right: str) -> float:
    left_tokens = _tokens(left)
    right_tokens = _tokens(right)
    if not left_tokens and not right_tokens:
        return 1.0
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def surface_overlap(answers: dict[str, str]) -> list[dict[str, float | str]]:
    """Pairwise share of wording. This is a surface score, not a judgment of meaning."""
    names = [name for name, text in answers.items() if text.strip()]
    rows: list[dict[str, float | str]] = []
    for index, left in enumerate(names):
        for right in names[index + 1 :]:
            score = jaccard_similarity(answers[left], answers[right])
            rows.append({"pair": f"{left} vs {right}", "overlap": round(score, 3)})
    return rows


def build_judge_prompt(user_prompt: str, answers: dict[str, str], reference: str) -> str:
    parts = [f"User prompt:\n{user_prompt.strip()}"]
    if reference.strip():
        parts.append(f"Reference answer:\n{reference.strip()}")
    else:
        parts.append("Reference answer: none provided.")
    for name, text in answers.items():
        parts.append(f"Answer from {name}:\n{text.strip()}")
    return "\n\n".join(parts)


def parse_judge_payload(text: str) -> dict | None:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    return payload


def string_list(value) -> list[str]:
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []

