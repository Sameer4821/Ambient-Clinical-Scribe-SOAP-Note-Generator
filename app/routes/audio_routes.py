from pathlib import Path
import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.whisper_service import transcribe_audio

router = APIRouter()

AUDIO_DIR = Path("data/audio")
TRANSCRIPT_DIR = Path("data/transcripts")


def ensure_directories():
    """Create necessary directories if they don't exist."""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)


def format_transcript_by_speaker(segments: list) -> list:
    """
    Format transcript segments by speaker.
    Combines consecutive segments from the same speaker.
    
    Args:
        segments: List of segments with speaker labels
        
    Returns:
        List of speaker blocks with combined text
    """
    speaker_transcript = []
    current_speaker = None
    current_text = ""
    
    for segment in segments:
        speaker = segment.get("speaker", "Unknown")
        text = segment.get("text", "").strip()
        
        # New speaker or first segment
        if speaker != current_speaker:
            # Save previous speaker's text if exists
            if current_text:
                speaker_transcript.append({
                    "speaker": current_speaker,
                    "text": current_text.strip()
                })
            
            # Start new speaker block
            current_speaker = speaker
            current_text = text
        else:
            # Same speaker, continue combining text
            current_text += " " + text
    
    # Don't forget the last speaker block
    if current_text:
        speaker_transcript.append({
            "speaker": current_speaker,
            "text": current_text.strip()
        })
    
    return speaker_transcript


@router.get("/audio")
def get_audio():
    """Health check endpoint for audio routes."""
    return {"message": "audio route working"}


@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload audio file, transcribe it with Whisper, and perform speaker diarization.
    
    Args:
        file: Audio file to upload
        
    Returns:
        JSON response with filename and speaker-structured transcript
    """
    try:
        ensure_directories()
        
        filename = file.filename
        file_path = AUDIO_DIR / filename
        
        # Save uploaded audio file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Transcribe and perform diarization
        transcript_result = transcribe_audio(str(file_path))
        
        # Format transcript by speaker
        speaker_transcript = format_transcript_by_speaker(
            transcript_result.get("segments", [])
        )
        
        # Prepare response structure
        response_data = {
            "filename": filename,
            "language": transcript_result.get("language", "unknown"),
            "transcript": speaker_transcript
        }
        
        # Save structured transcript to file as JSON
        transcript_filename = Path(filename).stem + ".json"
        transcript_path = TRANSCRIPT_DIR / transcript_filename
        
        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=2, ensure_ascii=False)
        
        return response_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading or processing file: {str(e)}"
        )
