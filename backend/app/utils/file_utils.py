import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import UploadFile

from app.config import OUTPUTS_DIR, UPLOADS_DIR


def timestamp_slug() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def build_file_name(prefix: str, suffix: str) -> str:
    return f"{prefix}_{timestamp_slug()}_{uuid4().hex[:8]}{suffix}"


def save_upload_file(upload: UploadFile, prefix: str = "upload") -> Path:
    suffix = Path(upload.filename or "").suffix.lower() or ".bin"
    filename = build_file_name(prefix, suffix)
    target = UPLOADS_DIR / filename
    with target.open("wb") as f:
        shutil.copyfileobj(upload.file, f)
    return target


def output_path_from_input(input_path: Path, prefix: str = "processed", suffix: Optional[str] = None) -> Path:
    ext = suffix if suffix else input_path.suffix
    filename = build_file_name(prefix, ext)
    return OUTPUTS_DIR / filename
