from uuid import UUID

from sqlalchemy.orm import Session

from app.models.audio import Audio


class AudioRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, audio_id: UUID):

        return (
            self.db.query(Audio)
            .filter(Audio.id == audio_id)
            .first()
        )