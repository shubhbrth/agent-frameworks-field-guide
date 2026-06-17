from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter


@dataclass(frozen=True)
class OpenRouterConfig:
    api_key: str
    model: str
    base_url: str

    @property
    def langchain_model_id(self) -> str:
        return f"openrouter:{self.model}"


def load_config() -> OpenRouterConfig:
    load_dotenv()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Create a .env file from .env.example "
            "and add your OpenRouter API key."
        )

    return OpenRouterConfig(
        api_key=api_key,
        model=os.getenv("OPENROUTER_MODEL", "~openai/gpt-latest"),
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    )


def build_chat_model(temperature: float = 0.2) -> ChatOpenRouter:
    config = load_config()
    return ChatOpenRouter(
        model=config.model,
        api_key=config.api_key,
        base_url=config.base_url,
        temperature=temperature,
        max_retries=2,
    )
