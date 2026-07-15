from sqlalchemy.orm import Session

from app.models.transcript import Transcript


class TranscriptRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, transcript):

        self.db.add(transcript)
        self.db.commit()
        self.db.refresh(transcript)

        return transcript
    
    def get_by_audio(self, audio_id):

        return (
            self.db.query(Transcript)
            .filter(
                Transcript.audio_id == audio_id,
            )
            .first()
        )