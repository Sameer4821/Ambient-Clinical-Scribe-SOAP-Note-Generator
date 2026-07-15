from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.soap_generator import SOAPGenerator
from app.repositories.audio_repository import AudioRepository
from app.repositories.transcript_repository import TranscriptRepository

router = APIRouter(
    prefix="/soap",
    tags=["SOAP"],
)


@router.post("/{audio_id}")
def generate_soap(
    audio_id: UUID,
    db: Session = Depends(get_db),
):

    audio_repo = AudioRepository(db)
    transcript_repo = TranscriptRepository(db)

    audio = audio_repo.get_by_id(audio_id)

    if audio is None:
        raise HTTPException(
            status_code=404,
            detail="Audio not found.",
        )

    transcript = transcript_repo.get_by_audio(audio.id)

    if transcript is None:
        raise HTTPException(
            status_code=404,
            detail="Transcript not found.",
        )

    generator = SOAPGenerator()

    return generator.generate(
        transcript.text,
    )