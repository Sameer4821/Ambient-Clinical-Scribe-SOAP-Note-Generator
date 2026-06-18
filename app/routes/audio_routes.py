from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.whisper_service import transcribe_audio

router = APIRouter()

AUDIO_DIR = Path("data/audio")
TRANSCRIPT_DIR = Path("data/transcripts")


def ensure_directories():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/audio")
def get_audio():
    return {"message": "audio route working"}


@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        ensure_directories()
        
        filename = file.filename
        file_path = AUDIO_DIR / filename
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        transcript = transcribe_audio(str(file_path))
        
        transcript_filename = Path(filename).stem + ".txt"
        transcript_path = TRANSCRIPT_DIR / transcript_filename
        
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        
        return {
            "filename": filename,
            "transcript": transcript
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading or transcribing file: {str(e)}"
        )
