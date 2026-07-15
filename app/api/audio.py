import os
import shutil
import uuid

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.audio import Audio

router = APIRouter(prefix="/audio", tags=["Audio"])

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    if not file.filename.endswith((".mp3", ".wav", ".m4a")):
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format.",
        )

    extension = file.filename.split(".")[-1]

    unique_name = f"{uuid.uuid4()}.{extension}"

    save_path = os.path.join(
        UPLOAD_FOLDER,
        unique_name,
    )

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    audio = Audio(
        filename=file.filename,
        path=save_path,
    )

    db.add(audio)
    db.commit()
    db.refresh(audio)

    return {
        "audio_id": str(audio.id),
        "filename": audio.filename,
        "status": audio.status,
    }