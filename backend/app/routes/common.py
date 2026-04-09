from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.config import ALLOWED_IMAGE_EXTS, ALLOWED_VIDEO_EXTS
from app.utils.file_utils import save_upload_file


def validate_location(latitude: float, longitude: float) -> None:
    if not (-90 <= latitude <= 90):
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
    if not (-180 <= longitude <= 180):
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")


def save_and_validate_upload(upload: UploadFile, expected: str) -> Path:
    ext = Path(upload.filename or "").suffix.lower()
    if expected == "image" and ext not in ALLOWED_IMAGE_EXTS:
        raise HTTPException(status_code=400, detail="Unsupported image file type")
    if expected == "video" and ext not in ALLOWED_VIDEO_EXTS:
        raise HTTPException(status_code=400, detail="Unsupported video file type")
    if expected == "either" and ext not in ALLOWED_IMAGE_EXTS.union(ALLOWED_VIDEO_EXTS):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    return save_upload_file(upload)

