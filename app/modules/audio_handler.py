from fastapi import UploadFile, HTTPException
import os
import shutil

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a"}


def is_valid_audio_file(filename: str) -> bool:
    extension = os.path.splitext(filename)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def save_audio_file(file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


def process_uploaded_file(file: UploadFile) -> str:
    if not is_valid_audio_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Only wav, mp3 and m4a files are allowed"
        )

    return save_audio_file(file)