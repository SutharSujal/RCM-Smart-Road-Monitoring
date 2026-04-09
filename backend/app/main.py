from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import BASE_DIR, OUTPUTS_DIR, UPLOADS_DIR
from app.database import init_db
from app.routes.detections import router as detections_router
from app.routes.hazard import router as hazard_router
from app.routes.pipeline import router as pipeline_router
from app.routes.plate import router as plate_router
from app.routes.vehicle import router as vehicle_router

app = FastAPI(title="RCM - Road Condition Monitoring")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vehicle_router)
app.include_router(plate_router)
app.include_router(hazard_router)
app.include_router(pipeline_router)
app.include_router(detections_router)

static_root = Path(BASE_DIR)
app.mount("/static", StaticFiles(directory=str(static_root)), name="static")


@app.on_event("startup")
def startup_event():
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    init_db()


@app.get("/")
def root():
    return {"message": "RCM backend is running"}

