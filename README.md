# 🚀 Pilot TN — Production-Grade Agentic AI Architecture

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/Orchestrator-CrewAI_0.80-FF4B4B)](https://www.crewai.com/)
[![LiveKit Agents](https://img.shields.io/badge/Voice_AI-LiveKit_Agents-purple?logo=webrtc)](https://livekit.io/)
[![Langfuse](https://img.shields.io/badge/Observability-Langfuse-orange)](https://langfuse.com/)
[![FastAPI](https://img.shields.io/badge/Microservice-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL pgvector](https://img.shields.io/badge/Vector_DB-PostgreSQL_pgvector-blue?logo=postgresql)](https://github.com/pgvector/pgvector)
[![MCP Protocol](https://img.shields.io/badge/Standard-Model_Context_Protocol-green)](https://modelcontextprotocol.io/)

> **Notice of Proprietary Technology & Open Architecture Showcase**  
> This public repository contains the **architectural design, interface specifications, and orchestration patterns** of the Agentic AI system powering **Pilot TN**, an enterprise educational platform in Tunisia.  
> *To protect the commercial intellectual property of the startup, the core business engine, private database schemas, and Next.js frontend remain in a private enterprise repository. Full live interactive demonstrations and white-box code walkthroughs are conducted during technical interviews.*

---

## 🌟 Architectural Overview

```
                         ┌──────────────────────────────────────────────┐
                         │               Client WebRTC / Web             │
                         │             (Browser & Mobile Apps)          │
                         └──────────────────────┬───────────────────────┘
                                                │
                       ┌────────────────────────┴────────────────────────┐
                       ▼                                                 ▼
        ┌──────────────────────────────┐                 ┌──────────────────────────────┐
        │   Pilot TN Gateway           │                 │ LiveKit SFU (WebRTC Audio)   │
        │   - Next.js 16 / Payload CMS │                 │ - Low-latency audio room     │
        │   - Guardrails & RBAC        │                 └──────────────┬───────────────┘
        └──────────────┬───────────────┘                                │
                       │ (HTTP / JSON)                                  ▼
                       │                                 ┌──────────────────────────────┐
                       ▼                                 │ voice_agent_spec.py          │
        ┌──────────────────────────────┐                 │ - Silero VAD (Barge-in)      │
        │ AI Agent Microservice        │                 │ - Deepgram Streaming STT     │
        │ (Python 3.12 + FastAPI)      │                 │ - Gemini Flash LLM           │
        │                              │                 │ - OpenAI Low-Latency TTS     │
        │  ┌────────────────────────┐  │                 └──────────────────────────────┘
        │  │ CrewAI Workflow Cluster│  │
        │  │ 1. Pedagogical Tutor   │  │
        │  │ 2. Fact-Checker Anti-H │  │
        │  │ 3. Adaptive Quiz Gen   │  │
        │  └───────────┬────────────┘  │
        │              │               │
        │  ┌───────────▼────────────┐  │
        │  │ MCP Tool Connectors    │  │
        │  │ - KnowledgeSearch (RAG)│  │
        │  │ - CalendarBooking      │  │
        │  │ - HumanHandoff (HITL)  │  │
        │  └────────────────────────┘  │
        └──────────────┬───────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │ Langfuse Observability       │
        │ - Token Tracing & Cost       │
        │ - Continuous Evals (Ragas)   │
        └──────────────────────────────┘
```

---

## 🔑 Core Engineering Highlights

### 1. 🎙️ Real-Time Voice Agent with Barge-In Interruption
- **LiveKit Agents Pipeline**: Connects directly into WebRTC audio rooms with a streaming STT ➔ LLM ➔ TTS loop.
- **Natural Interruption (Barge-in)**: Uses **Silero VAD (Voice Activity Detection)** with `interrupt_speech_duration: 0.6s`. When the student interrupts the AI verbally, speech synthesis cuts immediately (< 350ms) to process the new request.

### 2. 🤖 Multi-Agent Orchestration with CrewAI
A team of 3 specialized autonomous agents operating with strict sequential verification:
1. **Tutor Agent**: Focuses strictly on pedagogical explanation using the knowledge base.
2. **Fact-Checker Anti-Hallucination Agent**: Extracts claims from the Tutor's response and verifies them against the ground-truth course chunks. Blocks unverified claims.
3. **Adaptive Quiz Generator**: Synthesizes 3 targeted multiple-choice questions (MCQs) with pedagogical rationale based on the verified lesson content.

### 3. 🔍 Hybrid Semantic RAG & Re-ranking
- **Semantic Chunking**: Context-aware splitting preserving Markdown headers, theorems, and paragraph integrity.
- **Hybrid Scoring**: Combines dense vector similarity with BM25 lexical keyword boost:
  $$\text{Score} = 0.75 \times \text{CosineSimilarity} + 0.25 \times \text{BM25Boost}$$

### 4. 🛠️ Model Context Protocol (MCP) Standardized Tools
All agent tools adhere to strict **Pydantic v2 validation**:
- `KnowledgeSearchInput`: Semantic search with prompt-injection sanitization.
- `CalendarToolInput`: Slot availability and session booking.
- `HandoffToolInput`: **Human-in-the-Loop (HITL)** escalation for critical situations.

### 5. 📊 Observability & Continuous Evaluation (Langfuse)
- **Tracing**: Every agent execution, tool call, latency step, and token cost is streamed to Langfuse.
- **Evaluation Suite**: Automated test harness measuring **Faithfulness** (context fidelity) and **Answer Relevance** to guarantee zero regressions.

---

## 📁 Repository Structure

```
├── README.md                      # Complete architectural breakdown
├── schemas/
│   └── pydantic_contracts.py      # Strict Pydantic v2 input/output schemas
├── agents/
│   └── crew_architecture.py       # CrewAI multi-agent workflow specifications
├── voice/
│   └── livekit_voice_pipeline.py  # LiveKit streaming voice assistant with barge-in
├── tools/
│   └── mcp_tool_specs.py          # Model Context Protocol (MCP) tool schemas
└── evals/
    └── regression_eval_suite.py   # Continuous evaluation harness (Faithfulness / Relevance)
```

---

## 🎥 Video Demonstration

*(A 3-minute video walk-through demonstrating the real-time voice barge-in, multi-agent validation, and Langfuse tracing is available upon request).*

---

## 📩 Contact & Technical Inquiries

Developed by **Takwa Hafyen** — AI & Software Engineer.  
- GitHub: [takwahafyen](https://github.com/takwahafyen)  
- Contact: Available on request for live interactive technical demonstrations.
