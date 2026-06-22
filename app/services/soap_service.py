from app.services.schemas.soap_schema import SOAPNote
import os
import json

class SOAPService:

    @staticmethod
    def generate_soap(transcript: str) -> SOAPNote:

        subjective = ""
        objective = ""
        assessment = ""
        plan = ""

        lines = transcript.split("\n")

        for line in lines:

            line = line.strip()

            if line.startswith("Patient:"):
                subjective += line.replace("Patient:", "").strip() + " "

            elif "Temperature" in line:
                objective += line.replace("Doctor:", "").strip() + " "

            elif "infection" in line:
                assessment += line.replace("Doctor:", "").strip() + " "

            elif "Take" in line:
                plan += line.replace("Doctor:", "").strip() + " "

        return SOAPNote(
            subjective=subjective.strip(),
            objective=objective.strip(),
            assessment=assessment.strip(),
            plan=plan.strip()
        )