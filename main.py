from fastapi import FastAPI

app = FastAPI(title="Ambient Clinical Scribe API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ambient Clinical Scribe API"}