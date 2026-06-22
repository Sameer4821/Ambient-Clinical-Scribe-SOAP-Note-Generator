from fastapi import FastAPI
from app.api.audio import router as audio_router

app = FastAPI(title="Ambient Clinical Scribe API")

app.include_router(audio_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ambient Clinical Scribe API"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ambient-clinical-scribe"
    }