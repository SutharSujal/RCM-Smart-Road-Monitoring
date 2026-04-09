from fastapi import APIRouter, HTTPException

from app.services.detection_service import get_detection_record, list_detection_records

router = APIRouter(prefix="/api/detections", tags=["detections"])


@router.get("")
def list_detections():
    return {"items": list_detection_records()}


@router.get("/{record_id}")
def get_detection(record_id: int):
    record = get_detection_record(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Detection not found")
    return record

