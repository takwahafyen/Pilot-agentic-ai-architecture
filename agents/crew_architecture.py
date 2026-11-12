"""
CrewAI Multi-Agent Workflow Specification
=========================================
Architectural definition of the 3-agent sequential validation cluster.
"""
from __future__ import annotations

from typing import Any
from crewai import Agent, Crew, Process, Task


def create_tutor_agent(tools: list[Any]) -> Agent:
    """Tutor Agent: Explains concepts using RAG context."""
    return Agent(
        role="Tuteur Pédagogique Expert",
        goal="Expliquer clairement les notions de cours en se basant strictement sur les documents de référence.",
        backstory=(
            "Tu es un professeur bienveillant et rigoureux. Tu adaptes ton vocabulaire au niveau de l'élève. "
            "Tu n'affirmes JAMAIS rien sans citer ta source parmi les documents récupérés."
        ),
        tools=tools,
        verbose=True,
        memory=True,
    )


def create_fact_checker_agent() -> Agent:
    """Fact-Checker: Verifies tutor output against ground-truth chunks."""
    return Agent(
        role="Vérificateur Anti-Hallucination",
        goal="Vérifier chaque affirmation du tuteur par rapport aux documents originaux. Éliminer les hallucinations.",
        backstory=(
            "Tu es un auditeur scientifique impitoyable. Ton rôle est de vérifier chaque fait, chiffre et formule. "
            "Si une information n'est pas dans le cours, tu la signales et bloques sa diffusion."
        ),
        verbose=True,
        memory=False,
    )


def create_quiz_agent() -> Agent:
    """Quiz Generator: Generates targeted follow-up MCQs."""
    return Agent(
        role="Générateur de Quiz Adaptatif",
        goal="Générer 3 questions à choix multiples pertinentes pour tester la compréhension de l'élève.",
        backstory=(
            "Tu crées des exercices courts et ciblés avec des distracteurs intelligents et des explications claires."
        ),
        verbose=True,
        memory=False,
    )


def build_verification_crew(tools: list[Any]) -> Crew:
    """Instantiate the 3-agent Crew with sequential workflow."""
    tutor = create_tutor_agent(tools)
    checker = create_fact_checker_agent()
    quiz_gen = create_quiz_agent()

    task_explain = Task(
        description="Explique la notion demandée par l'élève en exploitant les outils RAG.",
        expected_output="Une explication pédagogique détaillée avec références aux sources.",
        agent=tutor,
    )

    task_verify = Task(
        description="Audite l'explication précédente contre les documents sources. Supprime toute affirmation non prouvée.",
        expected_output="L'explication validée et certifiée sans hallucination.",
        agent=checker,
    )

    task_quiz = Task(
        description="Génère 3 questions QCM basées sur le contenu validé.",
        expected_output="3 questions QCM structurées en JSON avec choix, réponse et explication.",
        agent=quiz_gen,
    )

    return Crew(
        agents=[tutor, checker, quiz_gen],
        tasks=[task_explain, task_verify, task_quiz],
        process=Process.sequential,
        verbose=True,
    )
