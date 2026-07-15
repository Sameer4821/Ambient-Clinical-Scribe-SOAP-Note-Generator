from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.icd_recommender import ICDRecommender
from app.repositories.audio_repository import AudioRepository
from app.repositories.transcript_repository import TranscriptRepository
from app.modules.soap_generator import SOAPGenerator

router = APIRouter(
    prefix="/icd",
    tags=["ICD"],
)


@router.post("/{audio_id}")
def recommend_icd(
    audio_id: UUID,
    db: Session = Depends(get_db),
):

    audio = AudioRepository(db).get_by_id(audio_id)

    if audio is None:
        raise HTTPException(
            status_code=404,
            detail="Audio not found.",
        )

    transcript = TranscriptRepository(db).get_by_audio(audio.id)

    if transcript is None:
        raise HTTPException(
            status_code=404,
            detail="Transcript not found.",
        )

    soap = SOAPGenerator().generate(
        transcript.text,
    )

    return ICDRecommender().recommend(
        soap["assessment"],
    )