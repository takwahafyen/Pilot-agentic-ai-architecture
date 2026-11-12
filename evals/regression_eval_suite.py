"""
AI Regression & Evaluation Suite
=================================
Automated evaluation calculating Faithfulness & Answer Relevance scores.
"""
from __future__ import annotations

from typing import Any


def compute_faithfulness(answer: str, contexts: list[str]) -> float:
    """Computes the ratio of claims in the answer supported by ground-truth contexts."""
    answer_words = set(answer.lower().split()) - {"the", "is", "a", "an", "and", "in", "of"}
    context_words = set(" ".join(contexts).lower().split())

    if not answer_words:
        return 0.0
    overlap = answer_words & context_words
    return round(len(overlap) / len(answer_words), 4)


def compute_relevance(answer: str, question: str) -> float:
    """Computes relevance of the answer with respect to the original query."""
    question_keywords = set(question.lower().split()) - {"what", "is", "how", "why", "the", "a"}
    answer_lower = answer.lower()

    if not question_keywords:
        return 1.0
    matches = sum(1 for w in question_keywords if w in answer_lower)
    return round(matches / len(question_keywords), 4)
