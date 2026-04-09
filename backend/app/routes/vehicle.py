from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.routes.common import save_and_validate_upload
from app.services.model_registry import get_yolo_service
from app.services.yolo_service import YoloService

router = APIRouter(prefix="/api/vehicle", tags=["vehicle"])


@router.post("/image")
def vehicle_image(
    file: UploadFile = File(...),
    yolo_service: YoloService = Depends(get_yolo_service),
):
    image_path = save_and_validate_upload(file, expected="image")
    return yolo_service.run_vehicle_only_on_image(image_path)


@router.post("/video")
def vehicle_video(
    file: UploadFile = File(...),
    yolo_service: YoloService = Depends(get_yolo_service),
):
    video_path = save_and_validate_upload(file, expected="video")
    result = yolo_service.process_video(video_path)
    return {
        "detected_vehicles": result["detected_vehicles"],
        "processed_output_path": result["output_path"],
    }


@router.post("/live-frame")
def vehicle_live_frame(
    file: UploadFile = File(...),
    input_type: str = Form("live"),
    yolo_service: YoloService = Depends(get_yolo_service),
):
    _ = input_type
    image_path = save_and_validate_upload(file, expected="image")
    return yolo_service.run_vehicle_only_on_image(image_path)

