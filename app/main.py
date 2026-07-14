from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.audio_routes import router

app = FastAPI()

# Configure CORS middleware to allow communication from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Healthcare Ambient Clinical Scribe"}