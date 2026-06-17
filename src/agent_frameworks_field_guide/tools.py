from __future__ import annotations

import json

from agent_frameworks_field_guide.sample_data import (
    ARTICLE_FORMATS,
    CONTENT_SERIES_BRIEF,
    FRAMEWORK_HINTS,
)


DEFAULT_TOPIC = "LangChain vs LangGraph vs Deep Agents"


def lookup_audience_profile(topic: str = DEFAULT_TOPIC) -> str:
    """Return the target audience and reader goals for the content topic."""
    return json.dumps(
        {
            "topic": topic,
            "primary_audience": CONTENT_SERIES_BRIEF["primary_audience"],
            "secondary_audience": CONTENT_SERIES_BRIEF["secondary_audience"],
            "reader_goals": CONTENT_SERIES_BRIEF["reader_goals"],
        },
        indent=2,
    )


def suggest_content_angles(topic: str = DEFAULT_TOPIC) -> str:
    """Return article angles and format guidance for the content topic."""
    return json.dumps(
        {
            "topic": topic,
            "content_goals": CONTENT_SERIES_BRIEF["content_goals"],
            "article_formats": ARTICLE_FORMATS,
            "framework_hints": FRAMEWORK_HINTS,
        },
        indent=2,
    )


def print_final_message(result: object) -> None:
    """Print the most useful final response shape across the examples."""
    if isinstance(result, dict):
        if "structured_response" in result:
            structured = result["structured_response"]
            if hasattr(structured, "model_dump_json"):
                print(structured.model_dump_json(indent=2))
            else:
                print(structured)
            return
        messages = result.get("messages")
        if messages:
            final_message = messages[-1]
            print(getattr(final_message, "content", final_message))
            return
    print(result)
