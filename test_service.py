# pyrefly: ignore [missing-import]
from app.services.schemas.soap_service import SOAPService

transcript = """
Patient: I have fever since 3 days.
Doctor: Temperature is 101F.
Doctor: Viral infection.
Doctor: Take Paracetamol.
"""

result = SOAPService.generate_soap(transcript)

print(result.model_dump())