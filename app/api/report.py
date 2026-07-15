from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.icd_recommender import ICDRecommender
from app.modules.pdf_generator import PDFGenerator
from app.modules.soap_generator import SOAPGenerator
from app.repositories.audio_repository import AudioRepository
from app.repositories.transcript_repository import TranscriptRepository

router = APIRouter(
    prefix="/report",
    tags=["Report"],
)


@router.get("/{audio_id}")
def generate_report(
    audio_id: UUID,
    db: Session = Depends(get_db),
):

    audio = AudioRepository(db).get_by_id(audio_id)

    transcript = TranscriptRepository(db).get_by_audio(audio.id)

    soap = SOAPGenerator().generate(
        transcript.text,
    )

    icd = ICDRecommender().recommend(
        soap["assessment"],
    )

    pdf = PDFGenerator().generate(
        audio_id,
        transcript.text,
        soap,
        icd,
    )

    return FileResponse(
        pdf,
        media_type="application/pdf",
        filename="clinical_report.pdf",
    )