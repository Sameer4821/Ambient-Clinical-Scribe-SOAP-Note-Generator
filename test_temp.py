from app.services.soap_service import SOAPService

transcript = """
Patient: I have headache for two days.
Doctor: Blood pressure is 140/90.
Doctor: Hypertension.
Doctor: Start Amlodipine 5mg daily.
"""

result = SOAPService.generate_soap(transcript)

print(result.model_dump())