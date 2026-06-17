# pyrefly: ignore [missing-import]
from fastapi import FastAPI

app = FastAPI(title="Smart Grid Load Balancing API")

@app.get("/")
def read_root():
    return {"message": "Hello Smart Grid"}