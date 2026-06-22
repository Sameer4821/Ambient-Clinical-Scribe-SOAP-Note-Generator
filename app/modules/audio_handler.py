import os

from fastapi import UploadFile
import shutil

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a"}

def save_audio_file(file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path

def is_valid_audio_file(filename: str) -> bool:
    extension = os.path.splitext(filename)[1].lower()
    return extension in ALLOWED_EXTENSIONS