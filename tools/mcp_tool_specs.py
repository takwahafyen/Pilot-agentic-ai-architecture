"""
Model Context Protocol (MCP) Standardized Tool Specifications
============================================================
Pydantic v2 schemas and validation boundaries for autonomous agent function calling.
"""
from __future__ import annotations

from typing import Annotated, Any
from pydantic import BaseModel, Field, field_validator


class KnowledgeSearchInput(BaseModel):
    """RAG tool — searches indexed educational documents."""
    query: Annotated[str, Field(min_length=3, max_length=500, description="The query to search in knowledge base")]
    top_k: Annotated[int, Field(default=4, ge=1, le=10)] = 4

    @field_validator("query")
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        # Prompt injection prevention filter
        for pattern in ["ignore instructions", "system prompt", "jailbreak"]:
            if pattern in v.lower():
                raise ValueError(f"Unsafe token detected: {pattern}")
        return v.strip()


class CalendarToolInput(BaseModel):
    """Calendar tool — schedules live revision sessions."""
    student_id: str
    title: str = Field(min_length=3, max_length=100)
    scheduled_at: str = Field(description="ISO 8601 future datetime")
    duration_minutes: int = Field(default=60, ge=15, le=180)


class HandoffToolInput(BaseModel):
    """Human-in-the-Loop (HITL) — escalates critical queries to staff."""
    reason: str = Field(min_length=10, max_length=500)
    urgency: str = Field(default="normal", pattern="^(low|normal|high|critical)$")
    context_summary: str = Field(max_length=1000)
