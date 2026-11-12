"""
Pydantic v2 Architectural Contracts & Schemas
============================================
Defines the strict input/output boundaries of the Agentic AI Mesh.
Zero proprietary startup code included.
"""
from __future__ import annotations

from typing import Annotated, Any
from pydantic import BaseModel, Field, field_validator


class StudentProfile(BaseModel):
    grade: str = "Secondary"
    education_level: str = "High School"
    preferred_language: str = "fr"


class TutorRequest(BaseModel):
    user_message: Annotated[str, Field(min_length=2, max_length=1000)]
    resource_ids: list[int | str] = []
    session_id: str
    student_profile: StudentProfile = Field(default_factory=StudentProfile)


class QuizQuestion(BaseModel):
    question: str
    choices: list[str] = Field(min_length=2, max_length=5)
    correct_answer: str
    explanation: str


class TutorResponse(BaseModel):
    answer: str
    fact_checked: bool = True
    sources: list[dict[str, Any]] = []
    quiz_questions: list[QuizQuestion] = []
    flagged_for_human: bool = False
    flag_reason: str | None = None
    latency_ms: int = 0


class EvalRequest(BaseModel):
    question: str
    answer: str
    context: list[str]


class EvalResponse(BaseModel):
    faithfulness_score: float = Field(ge=0.0, le=1.0)
    relevance_score: float = Field(ge=0.0, le=1.0)
    passed: bool
