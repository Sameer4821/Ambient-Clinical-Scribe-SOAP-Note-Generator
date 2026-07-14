"""
Speaker Diarization Service
Identifies and separates different speakers in audio files.
Uses pyannote.audio for speaker diarization, with a Gemini semantic fallback.
"""

try:
    from pyannote.audio import Pipeline  # pyrefly: ignore [missing-import]
    PYANNOTE_AVAILABLE = True
except ImportError:
    PYANNOTE_AVAILABLE = False


def get_diarization(audio_path: str):
    """
    Perform speaker diarization on an audio file.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        diarization object with speaker segments and timestamps, or None if unavailable.
    """
    if not PYANNOTE_AVAILABLE:
        print("pyannote.audio is not installed. Using Gemini-based diarization fallback.")
        return None

    try:
        # Initialize diarization pipeline
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.0")
        
        # Process audio file
        diarization = pipeline(audio_path)
        
        return diarization
    except Exception as e:
        print(f"Error performing Pyannote diarization: {str(e)}. Using Gemini fallback.")
        return None


def get_speaker_at_time(diarization, time: float) -> str:
    """
    Get the speaker label at a specific time point.
    
    Args:
        diarization: Diarization object from pyannote
        time: Time in seconds
        
    Returns:
        Speaker label (e.g., "Speaker 1", "Speaker 2")
    """
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        # Check if time falls within this speaker's segment
        if turn.start <= time <= turn.end:
            return speaker
    
    return None


def map_segments_via_gemini(segments: list) -> list:
    """
    Fallback method to perform speaker diarization using Gemini.
    Iterates over segments, formats them, and calls Gemini to assign
    each segment to 'Speaker 1: Doctor' or 'Speaker 2: Patient'.
    """
    if not segments:
        return segments
        
    from google import genai
    from google.genai import types
    from pydantic import BaseModel
    from typing import List
    
    class SegmentSpeaker(BaseModel):
        segment_id: int
        speaker: str # Should be exactly "Speaker 1: Doctor" or "Speaker 2: Patient"

    class DiarizationResult(BaseModel):
        segments: List[SegmentSpeaker]

    # Format the input segments for the Gemini prompt
    formatted_segments = []
    for seg in segments:
        formatted_segments.append(
            f"Segment ID {seg.get('id')}: \"{seg.get('text', '').strip()}\""
        )
    segments_text = "\n".join(formatted_segments)
    
    prompt = (
        "You are an expert medical transcriptionist. You are given a list of transcribed text segments "
        "from a doctor-patient consultation. The segments are in chronological order.\n"
        "Your task is to identify which segments are spoken by the Doctor, and which are spoken by the Patient.\n"
        "Assign the speaker for each segment as either 'Speaker 1: Doctor' or 'Speaker 2: Patient'.\n"
        "Rule:\n"
        "- The healthcare provider (asking questions, giving medical diagnoses/instructions) must be labeled as 'Speaker 1: Doctor'.\n"
        "- The patient (reporting symptoms, history, concerns) must be labeled as 'Speaker 2: Patient'.\n\n"
        "Input Segments:\n"
        f"{segments_text}\n"
    )
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DiarizationResult,
            ),
        )
        
        # Parse result
        result = DiarizationResult.model_validate_json(response.text)
        speaker_map = {item.segment_id: item.speaker for item in result.segments}
        
        # Apply labels back to segments
        for seg in segments:
            seg_id = seg.get("id")
            seg["speaker"] = speaker_map.get(seg_id, "Unknown")
            
    except Exception as e:
        print(f"Gemini diarization failed: {e}. Falling back to default alternating speakers.")
        # Default fallback if LLM fails: alternate speakers starting with Doctor
        for idx, seg in enumerate(segments):
            seg["speaker"] = "Speaker 1: Doctor" if idx % 2 == 0 else "Speaker 2: Patient"
            
    return segments


def map_segments_to_speakers(segments: list, diarization) -> list:
    """
    Map transcript segments to speaker labels.
    If diarization object is None (fallback mode), uses Gemini semantic diarization.
    Otherwise, uses pyannote timeline mapping.
    
    Args:
        segments: List of transcript segments from Whisper (with start/end times)
        diarization: Diarization object from pyannote, or None
        
    Returns:
        List of segments with speaker labels added
    """
    if diarization is None:
        return map_segments_via_gemini(segments)
        
    # Track which speakers we've encountered and their labels
    speaker_labels = {}
    speaker_counter = 0
    
    # Process each segment
    for segment in segments:
        # Get the midpoint of the segment to determine speaker
        mid_time = (segment.get("start", 0) + segment.get("end", 0)) / 2
        
        # Find which speaker was active at this time
        speaker = get_speaker_at_time(diarization, mid_time)
        
        # First time seeing this speaker, assign label
        if speaker and speaker not in speaker_labels:
            if speaker_counter == 0:
                speaker_labels[speaker] = "Speaker 1: Doctor"
            else:
                speaker_labels[speaker] = "Speaker 2: Patient"
            speaker_counter += 1
        
        # Add speaker label to segment
        segment["speaker"] = speaker_labels.get(speaker, "Unknown")
    
    return segments
