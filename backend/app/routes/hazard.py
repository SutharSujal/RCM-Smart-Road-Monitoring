from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.routes.common import save_and_validate_upload
from app.services.model_registry import get_yolo_service
from app.services.yolo_service import YoloService

router = APIRouter(prefix="/api/hazard", tags=["hazard"])


@router.post("/image")
def hazard_image(
    file: UploadFile = File(...),
    yolo_service: YoloService = Depends(get_yolo_service),
):
    image_path = save_and_validate_upload(file, expected="image")
    return yolo_service.run_hazard_only_on_image(image_path)


@router.post("/video")
def hazard_video(
    file: UploadFile = File(...),
    yolo_service: YoloService = Depends(get_yolo_service),
):
    video_path = save_and_validate_upload(file, expected="video")
    result = yolo_service.process_video(video_path)
    return {
        "detected_hazards": result["detected_hazards"],
        "severity": result["severity"],
        "processed_output_path": result["output_path"],
    }


@router.post("/live-frame")
def hazard_live_frame(
    file: UploadFile = File(...),
    input_type: str = Form("live"),
    yolo_service: YoloService = Depends(get_yolo_service),
):
    _ = input_type
    image_path = save_and_validate_upload(file, expected="image")
    return yolo_service.run_hazard_only_on_image(image_path)

