from __future__ import annotations

from typing import TypedDict

from deepagents import create_deep_agent
from deepagents.backends.utils import create_file_data
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from agent_frameworks_field_guide.config import load_config
from agent_frameworks_field_guide.schemas import ContentStrategy
from agent_frameworks_field_guide.tools import (
    DEFAULT_TOPIC,
    lookup_audience_profile,
    print_final_message,
    suggest_content_angles,
)


WORKSPACE_MEMORY = """# AI Content Strategy Assistant

This workspace is for planning a practical four-part technical article series.
Keep the final answer focused on audience, core angle, four-article outline, risks, and next steps.
The core_angle must explicitly mention the AI Content Strategy Assistant.
The next_steps must be publishing actions for this article series, not setup tasks for a new scenario.
Do not change the project into a research, citation, QA, support, or drafting assistant.
"""


class DeepAgentGraphState(TypedDict, total=False):
    topic: str
    task: str
    deep_agent_result: object


def prepare_task(state: DeepAgentGraphState) -> DeepAgentGraphState:
    topic = state.get("topic", DEFAULT_TOPIC)
    return {
        "task": (
            f"Create the final ContentStrategy for the AI Content Strategy Assistant about {topic}. "
            "Use the available tools. The outline must map to exactly these four articles: "
            "comparison intro, LangChain implementation, LangGraph implementation, and Deep Agents implementation. "
            "The core_angle must explicitly mention the AI Content Strategy Assistant. "
            "The next_steps must be publishing actions for this article series, not setup tasks for a new scenario. "
            "Do not turn this into a research, citation, QA, support, or drafting workflow."
        )
    }


def run_deep_agent(state: DeepAgentGraphState) -> DeepAgentGraphState:
    config = load_config()
    agent = create_deep_agent(
        model=config.langchain_model_id,
        tools=[lookup_audience_profile, suggest_content_angles],
        memory=["/AGENTS.md"],
        checkpointer=MemorySaver(),
        response_format=ContentStrategy,
        system_prompt=(
            "You are the deeper work-session agent inside a LangGraph workflow. "
            "Use the memory file and tools to produce a ContentStrategy for the AI Content Strategy Assistant. "
            "The core_angle must name the assistant, and next_steps must be publishing actions. "
            "Stay focused on audience, core angle, outline, risks, and next steps."
        ),
    )
    result = agent.invoke(
        {
            "messages": [{"role": "user", "content": state["task"]}],
            "files": {"/AGENTS.md": create_file_data(WORKSPACE_MEMORY)},
        },
        config={"configurable": {"thread_id": "langgraph-deepagents-content-demo"}},
    )
    return {"deep_agent_result": result}


def finalize_response(state: DeepAgentGraphState) -> DeepAgentGraphState:
    return state


def build_graph():
    graph = StateGraph(DeepAgentGraphState)
    graph.add_node("prepare_task", prepare_task)
    graph.add_node("run_deep_agent", run_deep_agent)
    graph.add_node("finalize_response", finalize_response)

    graph.add_edge(START, "prepare_task")
    graph.add_edge("prepare_task", "run_deep_agent")
    graph.add_edge("run_deep_agent", "finalize_response")
    graph.add_edge("finalize_response", END)
    return graph.compile()


def main() -> None:
    load_config()  # Fail immediately if configuration is invalid
    app = build_graph()
    result = app.invoke({"topic": DEFAULT_TOPIC})
    print_final_message(result["deep_agent_result"])


if __name__ == "__main__":
    main()

