# LangChain Example

This version treats the AI Content Strategy Assistant as a simple agent app.

Use LangChain when your application mostly fits this shape:

```text
prompt -> model -> tools -> final response
```

This example demonstrates:

- `create_agent`
- local Python tools
- structured output
- OpenRouter as the model provider

Run it from the repo root:

```bash
uv run python examples/01_langchain/agent.py
```
