CONTENT_SERIES_BRIEF = {
    "topic": "LangChain vs LangGraph vs Deep Agents",
    "primary_audience": "Python developers who are starting to build agentic AI applications.",
    "secondary_audience": "Technical founders and AI engineers evaluating the LangChain ecosystem.",
    "reader_goals": [
        "Understand how the three tools relate.",
        "Choose the right abstraction for a real project.",
        "See runnable examples instead of only conceptual advice.",
    ],
    "content_goals": [
        "Create curiosity in the comparison article.",
        "Use one shared example across the implementation articles.",
        "Keep the code small enough for readers to run locally.",
    ],
}

ARTICLE_FORMATS = [
    {
        "name": "field guide",
        "best_for": "explaining tradeoffs without turning the article into a reference manual",
    },
    {
        "name": "build-along tutorial",
        "best_for": "showing the exact code path readers can run from the repo",
    },
    {
        "name": "architecture walkthrough",
        "best_for": "showing why explicit workflow control matters",
    },
]

FRAMEWORK_HINTS = {
    "langchain": [
        "Use for a straightforward agent loop.",
        "Good fit for model, prompt, tools, and structured output.",
        "Mention broader features like middleware, retrieval, memory, streaming, MCP, and guardrails.",
    ],
    "langgraph": [
        "Use for explicit workflow stages and state transitions.",
        "Good fit for review loops and deterministic orchestration.",
        "Mention broader features like persistence, interrupts, time travel, memory, and subgraphs.",
    ],
    "deepagents": [
        "Use for deeper agentic work sessions.",
        "Good fit when the task looks like planning plus workspace management.",
        "Mention broader features like filesystem context, subagents, memory, permissions, sandboxes, skills, and streaming.",
    ],
}
