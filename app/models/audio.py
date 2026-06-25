from pydantic import BaseModel


class AudioUploadResponse(BaseModel):
    message: str
    filename: str
    path: str