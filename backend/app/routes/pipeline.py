from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.routes.common import save_and_validate_upload, validate_location
from app.services.detection_service import get_detection_record, save_detection_record
from app.services.model_registry import get_yolo_service
from app.services.yolo_service import YoloService

router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])


@router.post("/run")
def run_pipeline(
    input_type: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    location_name: str = Form(...),
    file: UploadFile = File(...),
    yolo_service: YoloService = Depends(get_yolo_service),
):
    input_type = input_type.lower()
    validate_location(latitude, longitude)

    if input_type not in {"image", "video", "live"}:
        raise HTTPException(status_code=400, detail="input_type must be image, video, or live")

    if input_type == "image" or input_type == "live":
        saved_path = save_and_validate_upload(file, expected="image")
        pipeline_result = yolo_service.process_image(saved_path)
    else:
        saved_path = save_and_validate_upload(file, expected="video")
        pipeline_result = yolo_service.process_video(saved_path)

    record_id = save_detection_record(
        filename=file.filename or Path(saved_path).name,
        input_type=input_type,
        detected_vehicles=pipeline_result["detected_vehicles"],
        detected_hazards=pipeline_result["detected_hazards"],
        severity=pipeline_result["severity"],
        latitude=latitude,
        longitude=longitude,
        location_name=location_name,
        original_file_path=str(saved_path),
        processed_output_path=pipeline_result["output_path"],
    )

    record = get_detection_record(record_id)
    if record is None:
        raise HTTPException(status_code=500, detail="Failed to read saved detection record")

    return {
        "message": "Detection completed",
        "result": record,
        "metrics": {
            "hazard_area_avg_ratio": pipeline_result["hazard_area_avg_ratio"],
            "repeated_occurrence_score": pipeline_result["repeated_occurrence_score"],
        },
    }

