from __future__ import annotations

from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy

from agent_frameworks_field_guide.config import build_chat_model
from agent_frameworks_field_guide.schemas import ContentStrategy
from agent_frameworks_field_guide.tools import (
    lookup_audience_profile,
    print_final_message,
    suggest_content_angles,
)

PROMPT = (
    "Create a content strategy for a blog series about LangChain, "
    "LangGraph, and Deep Agents. Use the available tools before answering."
)


def main() -> None:
    agent = create_agent(
        model=build_chat_model(),
        tools=[lookup_audience_profile, suggest_content_angles],
        system_prompt=(
            "You are a practical content strategist for technical articles. "
            "Return a concise strategy that is specific enough for a writer to use."
        ),
        response_format=ProviderStrategy(ContentStrategy),
    )

    result = agent.invoke({"messages": [{"role": "user", "content": PROMPT}]})
    print_final_message(result)


if __name__ == "__main__":
    main()
