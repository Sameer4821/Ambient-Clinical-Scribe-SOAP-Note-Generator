# Healthcare Ambient Clinical Scribe

This project is developed as part of the Infotact Generative AI Internship.

## Weekly Goals & Progress

### Week 1: Audio Ingestion and Speaker Diarization
*   **Overview:** Initialize the backend and build a pipeline for medical audio transcription.
*   **Key Deliverables:**
    *   FastAPI setup and structured base routing.
    *   Audio upload handling API endpoint.
    *   Whisper transcription integration.
    *   Pyannote.audio integration for Speaker Diarization (separating Doctor and Patient voices).

### Week 2: Prompt Engineering for Clinical Structuring
*   **Overview:** Design prompts to convert raw transcript into a structured SOAP note.
*   **Key Deliverables:**
    *   Define structured Pydantic schema for SOAP notes (`Subjective`, `Objective`, `Assessment`, `Plan`).
    *   Prompt engineering integration using Google Gemini API (`google-generativeai`).
    *   SOAP Note generation service (`SOAPService`) parsing clinical transcripts.
    *   Verification tests for SOAP schema and SOAP generation services.

## Tech Stack

*   **Backend Framework:** FastAPI & Uvicorn
*   **Transcription & Audio Processing:** OpenAI Whisper, Pyannote.audio, PyTorch, TorchAudio
*   **Generative AI / LLM:** Google Gemini API (`google-generativeai`)
*   **Data Validation:** Pydantic (v2)
*   **Frontend UI:** Streamlit
*   **Language:** Python 3.13+