from faster_whisper import WhisperModel
from sqlalchemy.orm import Session

from app.models.transcript import Transcript
from app.repositories.audio_repository import AudioRepository
from app.repositories.transcript_repository import TranscriptRepository


class TranscriptService:
    """
    Handles speech-to-text transcription using Faster-Whisper.
    """

    def __init__(self, db: Session):

        self.db = db

        self.audio_repository = AudioRepository(db)
        self.transcript_repository = TranscriptRepository(db)

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, audio_id):

        audio = self.audio_repository.get_by_id(audio_id)

        if audio is None:
            raise ValueError("Audio file not found.")

        segments, info = self.model.transcribe(
            audio.path,
            beam_size=5,
        )

        transcript_text = ""

        for segment in segments:
            transcript_text += segment.text.strip() + " "

        transcript = Transcript(
            audio_id=audio.id,
            text=transcript_text.strip(),
            language=info.language,
        )

        return self.transcript_repository.create(transcript)