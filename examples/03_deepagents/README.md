# Deep Agents Examples

This version frames the AI Content Strategy Assistant as a deeper work session.

Use Deep Agents when the work starts to look like a workspace:

- plan the task
- gather and organize context
- produce intermediate notes
- create final deliverables
- potentially use memory, files, permissions, sandboxes, skills, and subagents

This folder contains two examples:

- `agent.py`: creates a Deep Agent directly, seeds a small workspace memory file, and runs the content strategy task with a thread/checkpointer.
- `langgraph_deep_agent.py`: uses LangGraph as the outer workflow and calls a Deep Agent from one graph node.

The examples keep the code minimal and do not implement every Deep Agents capability. The article explains the broader feature set separately.

Run them from the repo root:

```bash
uv run python examples/03_deepagents/agent.py
uv run python examples/03_deepagents/langgraph_deep_agent.py
```
