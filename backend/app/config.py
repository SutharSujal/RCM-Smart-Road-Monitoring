from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
MODELS_DIR = APP_DIR / "models"
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
DB_PATH = BASE_DIR / "rcm.db"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

VEHICLE_MODEL_PATH = MODELS_DIR / "yolov8m.pt"
PLATE_MODEL_PATH = MODELS_DIR / "plate_blur_model.pt"
HAZARD_MODEL_PATH = MODELS_DIR / "best.pt"

ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
ALLOWED_VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".wmv"}

