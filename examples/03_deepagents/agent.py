from __future__ import annotations

from deepagents import create_deep_agent
from deepagents.backends.utils import create_file_data
from langgraph.checkpoint.memory import MemorySaver, InMemorySaver

from agent_frameworks_field_guide.config import load_config
from agent_frameworks_field_guide.schemas import ContentStrategy
from agent_frameworks_field_guide.tools import (
    lookup_audience_profile,
    print_final_message,
    suggest_content_angles,
)

TASK = (
    "Create the final ContentStrategy for the AI Content Strategy Assistant. "
    "The topic is a four-part article series about LangChain, LangGraph, and Deep Agents. "
    "Use the available audience and angle tools. The outline must map to exactly these four articles: "
    "comparison intro, LangChain implementation, LangGraph implementation, and Deep Agents implementation. "
    "The core_angle must explicitly mention the AI Content Strategy Assistant. "
    "The next_steps must be publishing actions for this article series, not setup tasks for a new scenario. "
    "Do not change the example into research, citation, QA, support, or drafting workflows."
)

WORKSPACE_MEMORY = """# AI Content Strategy Assistant

The assistant plans a technical content series.

The final answer must use the ContentStrategy shape:
- audience
- core_angle
- outline
- risks
- next_steps

The outline must stay mapped to four articles:
1. comparison intro
2. LangChain implementation
3. LangGraph implementation
4. Deep Agents implementation

The core_angle must explicitly mention the AI Content Strategy Assistant.
The next_steps must be publishing actions for this article series, not setup tasks for a new scenario.
Do not change the project into a research, citation, QA, support, or drafting assistant.
Use the same AI Content Strategy Assistant idea from the LangChain and LangGraph examples,
but treat this version as a deeper work session with notes and decisions before the final output.
"""

THREAD_ID = "deepagents-content-strategy-demo"


def build_agent():
    config = load_config()
    checkpointer = MemorySaver()

    return create_deep_agent(
        model=config.langchain_model_id,
        tools=[lookup_audience_profile, suggest_content_angles],
        memory=["/AGENTS.md"],
        checkpointer=checkpointer,
        response_format=ContentStrategy,
        system_prompt=(
            "You are a technical content strategist working inside an agent workspace. "
            "Use the memory file as project guidance. Return the final answer as a ContentStrategy. "
            "Stay about the AI Content Strategy Assistant for the LangChain, LangGraph, and Deep Agents "
            "article series. The core_angle must name the assistant, and next_steps must be "
            "publishing actions. Do not redefine the app as research, citation, support, QA, or drafting."
        ),
    )


def run_agent() -> object:
    agent = build_agent()
    return agent.invoke(
        {
            "messages": [{"role": "user", "content": TASK}],
            "files": {"/AGENTS.md": create_file_data(WORKSPACE_MEMORY)},
        },
        config={"configurable": {"thread_id": THREAD_ID}},
    )


def main() -> None:
    print_final_message(run_agent())


if __name__ == "__main__":
    main()

