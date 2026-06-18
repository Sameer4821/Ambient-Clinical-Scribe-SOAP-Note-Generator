from fastapi import FastAPI
from app.routes.audio_routes import router

app = FastAPI()
app.include_router(router)


@app.get("/")
def home():
    return {"message": "Healthcare Ambient Clinical Scribe"}