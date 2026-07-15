from fastapi import FastAPI

from app.database.base import Base
from app.database.connection import engine

import app.models

from app.api.audio import router as audio_router
from app.api.transcript import router as transcript_router
from app.api.soap import router as soap_router
from app.api.icd import router as icd_router
from app.api.report import router as report_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ambient Clinical Scribe",
    version="0.1.0",
)

# Register routers
app.include_router(audio_router)
app.include_router(transcript_router)
app.include_router(soap_router)
app.include_router(icd_router)
app.include_router(report_router)