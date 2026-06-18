"""
Speaker Diarization Service
Identifies and separates different speakers in audio files.
Uses pyannote.audio for speaker diarization.
"""

from pyannote.audio import Pipeline


def get_diarization(audio_path: str):
    """
    Perform speaker diarization on an audio file.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        diarization object with speaker segments and timestamps
    """
    try:
        # Initialize diarization pipeline
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.0")
        
        # Process audio file
        diarization = pipeline(audio_path)
        
        return diarization
    except Exception as e:
        raise Exception(f"Error performing diarization: {str(e)}")


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


def map_segments_to_speakers(segments: list, diarization) -> list:
    """
    Map transcript segments to speaker labels.
    Assigns "Doctor" to first speaker and "Patient" to second speaker.
    
    Args:
        segments: List of transcript segments from Whisper (with start/end times)
        diarization: Diarization object from pyannote
        
    Returns:
        List of segments with speaker labels added
    """
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
                speaker_labels[speaker] = "Doctor"
            else:
                speaker_labels[speaker] = "Patient"
            speaker_counter += 1
        
        # Add speaker label to segment
        segment["speaker"] = speaker_labels.get(speaker, "Unknown")
    
    return segments
