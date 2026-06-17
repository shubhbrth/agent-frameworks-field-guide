from __future__ import annotations

from pydantic import BaseModel, Field


class ContentStrategy(BaseModel):
    audience: str = Field(description="The primary audience for the content.")
    core_angle: str = Field(description="The strongest editorial angle.")
    outline: list[str] = Field(description="A concise article or series outline.")
    risks: list[str] = Field(description="Risks or weak spots in the content plan.")
    next_steps: list[str] = Field(description="Concrete next actions for the writer.")
