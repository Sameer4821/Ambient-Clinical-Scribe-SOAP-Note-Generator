from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Healthcare Ambient Clinical Scribe Project Started"
    }