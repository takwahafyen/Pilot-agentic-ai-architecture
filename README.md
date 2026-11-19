# 🏛️ Pilot TN — Multi-Agent & Voice AI Architecture Specification

[![Architecture](https://img.shields.io/badge/Architecture-Agentic_AI_Mesh-blue.svg)](https://github.com/takwahafyen/Pilot-agentic-ai-architecture)
[![Next.js 16](https://img.shields.io/badge/Next.js-16.2.3-black?logo=next.js)](https://nextjs.org/)
[![Payload CMS 3](https://img.shields.io/badge/Payload_CMS-3.82.0-blue?logo=payloadcms)](https://payloadcms.com/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/Multi--Agent-CrewAI_0.80-FF4B4B)](https://www.crewai.com/)
[![LiveKit Agents](https://img.shields.io/badge/Voice_AI-LiveKit_WebRTC-purple?logo=webrtc)](https://livekit.io/)
[![Langfuse](https://img.shields.io/badge/Observability-Langfuse-orange)](https://langfuse.com/)

> **Public Architecture Repository**: [https://github.com/takwahafyen/Pilot-agentic-ai-architecture](https://github.com/takwahafyen/Pilot-agentic-ai-architecture)  
> **Live Production Platform**: [https://pilot-web-onv5.onrender.com](https://pilot-web-onv5.onrender.com)

---

## 🧭 Executive Architecture Summary

**Pilot TN** implements a production-grade, distributed **Agentic AI Mesh** designed specifically for real-time education in Tunisia. Rather than relying on a generic monolithic chatbot, the platform orchestrates **4 specialized autonomous AI agents** operating across client browser runtimes, serverless edge APIs, a dedicated Python multi-agent microservice, and WebRTC streaming media servers.

---

## 🗺️ High-Level System Architecture Diagram

```
                                      ┌─────────────────────────────────────────────────────────┐
                                      │                     CLIENT TIER                         │
                                      │      (Next.js 16.2 · React 19 · Web Speech API)        │
                                      └────────────┬─────────────────────────────┬───────────────┘
                                                   │                             │
                                        HTTP/REST  │                             │ LiveKit WebRTC
                                                   ▼                             ▼
┌──────────────────────────────────────────────────────────────────┐   ┌────────────────────────────────┐
│               FULLSTACK APPLICATION & CMS CORE                   │   │     LIVEKIT CLOUD SFU          │
│                (Next.js App Router + Payload CMS 3)              │   │   - Low-latency Audio Stream   │
│                                                                  │   │   - Real-time Voice Rooms      │
│  ┌───────────────────────┐             ┌──────────────────────┐  │   └───────────────┬────────────────┘
│  │   Auth & RBAC Layer   │             │   Child Safety Hub   │  │                   │
│  │   Teacher/Student/Adm │             │   8 Category Rules   │  │                   │ WebRTC Bridge
│  └───────────┬───────────┘             │   PII Asterisk Mask  │  │                   ▼
│              │                         └──────────┬───────────┘  │   ┌────────────────────────────────┐
│              ▼                                    │              │   │    PYTHON VOICE WORKER         │
│  ┌────────────────────────────────────────────────┼───────────┐  │   │    - Silero VAD (Barge-in)     │
│  │                     4 AUTONOMOUS AGENTS        │           │  │   │    - Deepgram Streaming STT    │
│  │                                                │           │  │   │    - Gemini Flash Reasoning    │
│  │  1. Session Rec Engine      2. Teacher Assistant           │  │   │    - ElevenLabs Streaming TTS  │
│  │     (/dashboard/sessions)      (Conversational Actions)    │  │   └────────────────────────────────┘
│  │                                                            │  │
│  │  3. RAG Resource Assistant  4. Student Voice Tutor         │  │
│  │     (Semantic & BM25)          (Hands-free Call & Drafts)  │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────┬────────────────────────────────┬──────────────┘
                   │                                │
                   ▼                                ▼
┌──────────────────────────────────────┐  ┌─────────────────────────────────────┐
│          PERSISTENCE TIER            │  │      PYTHON AI SERVICE (FastAPI)    │
│  - PostgreSQL 16 (Neon Serverless)   │  │  - CrewAI 0.80 Orchestrator         │
│  - pgvector (Semantic Embeddings)    │  │  - Tutor + Fact-Checker + Quiz Crew │
│  - ModerationEvents & AuditEvents    │  │  - Model Context Protocol (MCP)     │
│  - Centrifugo v6 (WebSocket Engine)  │  │  - Langfuse Tracing & Latency Tele. │
└──────────────────────────────────────┘  └─────────────────────────────────────┘
```

---

## 🤖 Deep Dive: The 4 Autonomous Agents

```
+----------------------------------------------------------------------------------------------------+
|                                    PILOT TN AGENTIC MESH                                           |
+--------------------------+--------------------------+------------------------+---------------------+
| AGENT 1: RECOMMENDATION  | AGENT 2: TEACHER COPILOT | AGENT 3: RAG ASSISTANT | AGENT 4: VOICE TUTOR|
+--------------------------+--------------------------+------------------------+---------------------+
| Domain: /sessions        | Domain: Educator Studio  | Domain: Course Library | Domain: Global Call |
| Logic: Next.js Cache     | Logic: NLP Action Parser | Logic: Vector + BM25   | Logic: State-Machine|
| LLM: Gemini Flash        | LLM: Gemini Flash        | LLM: Gemini + CrewAI   | LLM: Gemini Flash   |
| Modality: UI Spotlight   | Modality: Chat + Voice   | Modality: Document QA  | Modality: Full Voice|
+--------------------------+--------------------------+------------------------+---------------------+
```

---

### 🎯 Agent 1: Session Recommendation Engine
- **Primary Route**: `/dashboard/sessions` *(via `getRecommendedSessions()` in `src/app/(frontend)/sessions/actions.ts`)*
- **Architectural Role**: Proactive curriculum pathfinding.
- **Data Flow & Sequence**:
  ```
  [Student Profile] ──┐
  [Past Attendance] ──┼──> [Candidate Pool (20)] ──> [Gemini Reasoning] ──> [Top 3 Recommendations]
  [Curriculum Level] ──┘                                                      │
                                                                              ▼
                                                                [Next.js 30-min User Cache]
                                                                              │
                                                                              ▼
                                                                [DashboardSpotlightCard UI]
  ```
- **Key Architectural Features**:
  1. **Candidate Pool Isolation**: Filters active, upcoming sessions (`published` or `live`) from `live-sessions`, capping candidate input tokens.
  2. **Pedagogical Rationale Generation**: Does not merely score items; outputs structured JSON containing an encouraging `recommendationReason` justifying *why* the session benefits the student.
  3. **Zero-Latency Invalidation**: Cached using Next.js `unstable_cache` with a 30-minute TTL per student, shielding backend databases from repetitive querying.

---

### 👨‍🏫 Agent 2: Teacher Assistant & Action Copilot
- **Primary Component**: `AiSessionAgent.tsx` + `/api/teacher-agent/route.ts`
- **Architectural Role**: Natural language administrative automation.
- **Data Flow & Sequence**:
  ```
  [Teacher Input (Text/Voice)] ──> [Tunisian Phonetic Auto-Correct] ──> [/api/teacher-agent]
                                                                               │
                                       ┌───────────────────────────────────────┴───────────────────┐
                                       ▼                                                           ▼
                             [Action: create_session]                                    [Action: create_announcement]
                                       │                                                           │
                                       ▼                                                           ▼
                             [Resolve Relative Dates]                                    [Extract Group & Pin]
                             ("tomorrow" ➔ ISO-8601)                                               │
                                       │                                                           ▼
                                       ▼                                                 [Payload DB Mutation]
                             [Draft in live-sessions]                                    [Notify Group Members]
  ```
- **Key Architectural Features**:
  1. **Phonetic & Semantic Auto-Correction**: Pre-processes raw voice transcripts against common Tunisian/ESL mispronunciations (e.g. `shedul` ➔ `schedule`, `anouncment` ➔ `announcement`).
  2. **Deterministic Action Parsing**: The model outputs strict raw JSON actions (`create_session` or `create_announcement`) executed server-side with teacher authorization validation.
  3. **Trilingual Context Engine**: Dynamically switches prompts, database date formatters, and TTS voices across French, English, and Arabic.

---

### 📚 Agent 3: Hybrid RAG Resource Assistant & Anti-Hallucination Crew
- **Primary Component**: `AiResourceDialog.tsx` + `/dashboard/resources/ai-actions.ts` + `tutor_crew.py`
- **Architectural Role**: Grounded syllabus companion and multi-agent knowledge verification.
- **RAG Architecture**:
  ```
  [Document Ingestion] ──> [Semantic Markdown Chunking] ──> [Gemini text-embedding-004] ──> [resource-indices]
                                                                                                  │
  [User Query] ──> [Query Embedding] ──> [Dense Cosine Search (0.75)] ──┐                         │
                                      ──> [Lexical BM25 Boost (0.25)]  ──┴──> [Top K Chunks Context]
                                                                                     │
                                                                                     ▼
                                                                        [CrewAI Multi-Agent Pipeline]
                                                                        • Tutor: Formulates explanation
                                                                        • Fact-Checker: Audits against context
                                                                        • Quiz Gen: Formats 5 verified MCQs
  ```
- **Key Architectural Features**:
  1. **Hybrid Retrieval**: Dense semantic similarity merged with BM25 lexical boost to capture both conceptual queries and exact formula terms.
  2. **Multi-Agent Anti-Hallucination**: Offloads complex queries to a decoupled Python 3.12 microservice running CrewAI where claims are cross-checked before returning.
  3. **Instant Workflows**: UI chips for immediate summarization (`Summarize`), structural breakdown (`Describe`), and assessment creation (`Quiz`).

---

### 🎙️ Agent 4: Student Voice Tutor & Child Safety Agent
- **Primary Component**: `FloatingVoiceAgent.tsx` + `/api/voice-tutor/route.ts` + `guardrails.ts`
- **Architectural Role**: Real-time hands-free voice companion with strict child protection.
- **Voice State-Machine & Lifecycle**:
  ```
  [Start Call] ➔ [Ringtone (440Hz)] ➔ [Microphone Init] ➔ [Trilingual Greeting]
                                                                 │
          ┌──────────────────────────────────────────────────────┴───────────────────────┐
          ▼                                                                              ▼
  [Student Speaks]                                                               [Student Silent]
          │                                                                              │
          ▼                                                                              ▼
  [Dynamic Asterisk Masking]                                                     [7s Inactivity Warning]
  ("code secret 1234" ➔ "code secret ******")                                     ("S'il vous plaît...")
          │                                                                              │
          ▼                                                                              ▼
  [3s Silence Countdown]                                                         [Still Silent (+7s)]
          │                                                                              │
          ▼                                                                              ▼
  [Check 8 Guardrails]                                                           [Auto-Hangup Protocol]
          │                                                                              │
          ├─────────────────────────┬─────────────────────────┐                          │
          ▼                         ▼                         ▼                          │
  [Child Harm Blocked]     [Urgent Escalation]      [Safe Study Query]                   │
  (Benevolent deflection)   (Alert & ModEvent)      (Gemini 25-word TTS)                 │
          │                         │                         │                          │
          └─────────────────────────┴─────────────┬───────────┘                          │
                                                  ▼                                      ▼
                                       [Farewell / CALL_END] ───────────────────> [Call Ended Screen]
                                                                                  • PhoneOff Animated Logo
                                                                                  • Trilingual Call Ended
                                                                                  • 1.5s Auto-Close
  ```
- **Voice-to-Channel Draft Pipeline (Human-in-the-Loop)**:
  - If student asks to communicate (e.g., *"Dis dans le groupe qu'on révise ce soir"*), the AI drafts a respectful message and populates the `ChannelComposer` via client `localStorage` and custom events.
  - **Zero automated posting without student manual review and click**.
- **Child Protection Guardrails (8 Categories)**:
  - Intercepts sexual content, violence, self-harm, drugs, bullying, radicalization, adult platforms, and PII in Arabic, French, and English.
- **Urgent Moderation Escalation**:
  - Urgent student requests trigger automated message creation, notify teachers, and inject priority incidents directly into `moderation-events`.

---

## ⚖️ Moderation vs. Audit Architecture

```
                       INCOMING PLATFORM ACTIVITY
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
┌─────────────────────────────────┐         ┌─────────────────────────────────┐
│     ModerationEvents Hub        │         │        AuditEvents Registry     │
│   (Domain Moderation Queue)     │         │   (Technical Compliance Log)    │
├─────────────────────────────────┤         ├─────────────────────────────────┤
│ • Visibility: Teachers & Admins │         │ • Visibility: Superadmins only  │
│ • Mutability: Active Workflow   │         │ • Mutability: Immutably Append  │
│   (open ➔ investigating ➔ done) │         │ • Purpose: Forensics & Legal    │
│ • Purpose: Content triage,      │         │ • Captures: System operations,  │
│   bullying intervention &       │         │   role changes, moderation event│
│   emergency session alerts      │         │   lifecycle modifications       │
└─────────────────────────────────┘         └─────────────────────────────────┘
```

---

## 📊 Observability & Cost Telemetry (Langfuse)

All AI interactions flow through a unified Langfuse tracing layer:
- **Zero-Dependency Direct REST Ingestion**: Client and Next.js server actions log execution traces asynchronously.
- **Telemetry Captured**:
  - Exact token usage (Prompt tokens vs Completion tokens).
  - Multi-turn conversation latency breakdown.
  - Model fallback tracking (Gemini Flash primary with automatic failover).
  - User session ID and role attribution.

---

## 🛠️ Technology Stack Breakdown

| Layer | Technologies | Architectural Significance |
|:---|:---|:---|
| **Frontend Framework** | Next.js 16.2.3, React 19 | Server Components, Turbopack, low bundle size |
| **Data & Auth Core** | Payload CMS 3.82, PostgreSQL 16 | Type-safe schema generation, granular RBAC |
| **Realtime WebRTC** | LiveKit Cloud SFU, Web Speech API | Dual-mode streaming voice and client-side STT/TTS |
| **AI Orchestration** | CrewAI 0.80, FastAPI, Python 3.12 | Multi-agent collaborative reasoning pipelines |
| **Foundation Models** | Google Gemini Flash, `text-embedding-004` | High speed inference and semantic vector search |
| **Realtime Messaging** | Centrifugo v6, WebSockets | Ephemeral presence, unread counters, live push |
| **Observability** | Langfuse REST Client | Continuous prompt evaluation and cost governance |
| **Internationalization** | `next-intl`, Bi-directional RTL CSS | Native Arabic, French, and English accessibility |

---

## 📄 License
This architecture specification is licensed under the MIT License.
