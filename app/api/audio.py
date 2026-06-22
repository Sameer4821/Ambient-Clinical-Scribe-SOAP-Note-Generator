from fastapi import APIRouter

router = APIRouter()


@router.get("/audio")
def audio_status():
    return {"message": "Audio service ready"}