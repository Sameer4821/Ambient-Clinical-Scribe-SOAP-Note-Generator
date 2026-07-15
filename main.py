from app.database.base import Base
from app.database.connection import engine

import app.models

Base.metadata.create_all(bind=engine)

from fastapi import FastAPI

from app.api.audio import router as audio_router

app = FastAPI(
    title="Ambient Clinical Scribe",
)

app.include_router(audio_router)