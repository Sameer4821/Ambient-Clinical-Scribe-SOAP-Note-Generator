from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.transcript_service import TranscriptService

router = APIRouter(
    prefix="/transcript",
    tags=["Transcript"],
)


@router.post("/{audio_id}")
def generate_transcript(
    audio_id: UUID,
    db: Session = Depends(get_db),
):

    service = TranscriptService(db)

    try:
        transcript = service.transcribe(audio_id)

        return {
            "id": str(transcript.id),
            "audio_id": str(transcript.audio_id),
            "language": transcript.language,
            "transcript": transcript.text,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )