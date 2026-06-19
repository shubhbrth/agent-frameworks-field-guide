from __future__ import annotations

import sys
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agent_frameworks_field_guide.config import build_chat_model, load_config
from agent_frameworks_field_guide.schemas import ContentStrategy
from agent_frameworks_field_guide.tools import (
    DEFAULT_TOPIC,
    lookup_audience_profile,
    suggest_content_angles,
)


class StrategyState(TypedDict, total=False):
    topic: str
    audience_notes: str
    angle_notes: str
    selected_angle: str
    outline: str
    final_strategy: ContentStrategy


def identify_audience(state: StrategyState) -> StrategyState:
    topic = state.get("topic", DEFAULT_TOPIC)
    return {"audience_notes": lookup_audience_profile(topic)}


def generate_angles(state: StrategyState) -> StrategyState:
    topic = state.get("topic", DEFAULT_TOPIC)
    return {"angle_notes": suggest_content_angles(topic)}


def select_angle(state: StrategyState) -> StrategyState:
    model = build_chat_model()
    response = model.invoke(
        [
            (
                "system",
                "You choose concise editorial angles for a technical article series. "
                "Stay focused on the AI Content Strategy Assistant example.",
            ),
            (
                "human",
                "Choose the strongest angle for a blog series about LangChain, LangGraph, "
                "and Deep Agents. The shared demo app is an AI Content Strategy Assistant "
                "that returns audience, core angle, outline, risks, and next steps. "
                "Do not change the demo app into another project.\n\n"
                f"Audience notes:\n{state['audience_notes']}\n\n"
                f"Angle notes:\n{state['angle_notes']}",
            ),
        ]
    )
    return {"selected_angle": response.content}


def draft_outline(state: StrategyState) -> StrategyState:
    model = build_chat_model()
    response = model.invoke(
        [
            (
                "system",
                "You create clear outlines for practical technical articles. "
                "Stay focused on LangChain, LangGraph, Deep Agents, and the AI Content Strategy Assistant.",
            ),
            (
                "human",
                "Draft a concise four-part article series outline using this angle. "
                "The four articles must be: comparison intro, LangChain implementation, "
                "LangGraph implementation, and Deep Agents implementation. "
                "Do not introduce a different app or workflow.\n\n"
                f"{state['selected_angle']}",
            ),
        ]
    )
    return {"outline": response.content}


def review_strategy(state: StrategyState) -> StrategyState:
    model = build_chat_model()
    structured_model = model.with_structured_output(ContentStrategy)
    strategy = structured_model.invoke(
        [
            (
                "system",
                "You review the draft content strategy and return the final structured strategy. "
                "The final answer must stay about the AI Content Strategy Assistant for a "
                "LangChain vs LangGraph vs Deep Agents article series.",
            ),
            (
                "human",
                "Create the final AI Content Strategy Assistant output using the same schema "
                "as the LangChain version. Do not change the app into research, drafting, "
                "verification, citation, or QA workflows.\n\n"
                f"Audience notes:\n{state['audience_notes']}\n\n"
                f"Selected angle:\n{state['selected_angle']}\n\n"
                f"Draft outline:\n{state['outline']}\n\n"
                "Return audience, core_angle, outline, risks, and next_steps. "
                "The outline should map to the four article series: comparison, LangChain, "
                "LangGraph, and Deep Agents.",
            ),
        ]
    )
    return {"final_strategy": strategy}


def build_graph():
    graph = StateGraph(StrategyState)
    graph.add_node("identify_audience", identify_audience)
    graph.add_node("generate_angles", generate_angles)
    graph.add_node("select_angle", select_angle)
    graph.add_node("draft_outline", draft_outline)
    graph.add_node("review_strategy", review_strategy)

    graph.add_edge(START, "identify_audience")
    graph.add_edge("identify_audience", "generate_angles")
    graph.add_edge("generate_angles", "select_angle")
    graph.add_edge("select_angle", "draft_outline")
    graph.add_edge("draft_outline", "review_strategy")
    graph.add_edge("review_strategy", END)
    return graph.compile()


def main() -> None:
    load_config()  # Fail immediately if configuration is invalid
    app = build_graph()
    result = app.invoke({"topic": DEFAULT_TOPIC})
    output = result["final_strategy"].model_dump_json(indent=2)
    sys.stdout.buffer.write(output.encode("utf-8"))
    sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
