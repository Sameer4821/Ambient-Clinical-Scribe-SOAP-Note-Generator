import whisper
from app.services.diarization_service import (
    get_diarization,
    map_segments_to_speakers
)


def transcribe_audio(file_path: str) -> dict:
    """
    Transcribe audio file using Whisper and perform speaker diarization.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Dictionary containing full text, segments with speakers, and metadata
    """
    try:
        # Load Whisper model and transcribe
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        
        # Perform speaker diarization
        diarization = get_diarization(file_path)
        
        # Map transcript segments to speaker labels
        segments = result.get("segments", [])
        segments_with_speakers = map_segments_to_speakers(segments, diarization)
        
        # Return structured result
        return {
            "text": result["text"],
            "segments": segments_with_speakers,
            "language": result.get("language", "unknown")
        }
    except Exception as e:
        raise Exception(f"Error transcribing audio: {str(e)}")
