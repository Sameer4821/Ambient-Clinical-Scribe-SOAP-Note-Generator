from fastapi import APIRouter, UploadFile, File, HTTPException

from app.modules.audio_handler import (
    is_valid_audio_file,
    save_audio_file
)

router = APIRouter(prefix="/audio", tags=["Audio"])


@router.get("/")
def audio_status():
    return {"message": "Audio service ready"}


@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):

    if not is_valid_audio_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Only wav, mp3 and m4a files are allowed"
        )

    file_path = save_audio_file(file)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "path": file_path
    }