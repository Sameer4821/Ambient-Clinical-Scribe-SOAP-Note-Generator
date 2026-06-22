# pyrefly: ignore [missing-import]
from app.services.schemas.soap_schema import SOAPNote

note = SOAPNote(
    subjective="Fever",
    objective="101F",
    assessment="Flu",
    plan="Rest"
)

print(note.model_dump())