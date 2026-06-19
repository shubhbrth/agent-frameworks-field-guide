# LangGraph Example

This version turns the AI Content Strategy Assistant into an explicit workflow.

Use LangGraph when you want control over the stages and state:

```text
identify_audience -> generate_angles -> select_angle -> draft_outline -> review_strategy
```

This example intentionally does not implement persistence, interrupts, time travel, or deployment. Those are important LangGraph capabilities, but this repo keeps the code focused on the comparison series.

Run it from the repo root:

```bash
uv run python examples/02_langgraph/graph.py
```
