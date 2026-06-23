from app.services.schemas.soap_schema import SOAPNote
from dotenv import load_dotenv
import os
import json
# pyrefly: ignore [missing-import]
from google import genai
from google.genai import types

load_dotenv()

# Instantiate the GenAI client. It will automatically load GEMINI_API_KEY from environment variables.
client = genai.Client()

class SOAPService:

    @staticmethod
    def generate_soap(transcript: str) -> SOAPNote:
        """
        Generate a SOAP note from a medical consultation transcript.
        Uses the Gemini API with structured output matching the SOAPNote schema.
        """
        prompt = (
            "Analyze the following medical consultation transcript and extract the SOAP note. "
            "Populate each section as follows:\n"
            "- subjective: Patient symptoms, history, feelings as reported by the patient.\n"
            "- objective: Vital signs, measurements, physical exam findings, or lab results.\n"
            "- assessment: Diagnoses, clinical impressions, or status of conditions.\n"
            "- plan: Next steps, medications prescribed, recommended tests, or follow-up instructions.\n\n"
            f"Transcript:\n{transcript}"
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SOAPNote,
            ),
        )

        # Parse the structured response into the SOAPNote model
        return SOAPNote.model_validate_json(response.text)