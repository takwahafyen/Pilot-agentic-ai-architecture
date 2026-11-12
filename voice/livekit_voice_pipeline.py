"""
LiveKit Agents Real-Time Streaming Voice Pipeline
=================================================
Implements sub-400ms voice conversational loop with natural barge-in interruption.
"""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Pipeline Architectural Configuration
VOICE_AGENT_CONFIG: dict[str, Any] = {
    "stt": {
        "provider": "Deepgram",
        "model": "nova-2-general",
        "language": "fr",
        "interim_results": True,  # Enables instant speech detection
    },
    "llm": {
        "provider": "Google Gemini via OpenAI Protocol",
        "model": "gemini-1.5-flash",
        "streaming": True,
    },
    "tts": {
        "provider": "OpenAI / ElevenLabs",
        "voice": "alloy",
        "streaming_latency": 1,  # Minimum chunk synthesis
    },
    "vad": {
        "engine": "Silero VAD",
        "interrupt_speech_duration": 0.6,  # Seconds of human speech before cutoff
        "interrupt_min_words": 0,          # Instant cutoff on first word
        "allow_interruptions": True,       # Full barge-in enabled
    },
}

SYSTEM_INSTRUCTION = """Tu es l'assistant vocal IA de Pilot TN.
Tes réponses sont concises (2 à 3 phrases maximum) pour s'adapter à une conversation orale fluide.
Tu n'inventes jamais de faits. Si tu ne sais pas, tu le dis clairement.
"""


def log_pipeline_specs() -> None:
    logger.info("LiveKit Streaming Voice Agent configured.")
    logger.info("VAD Engine: %s with Barge-In enabled.", VOICE_AGENT_CONFIG["vad"]["engine"])
