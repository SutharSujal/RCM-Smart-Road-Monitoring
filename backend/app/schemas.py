from pydantic import BaseModel


class DetectionRecord(BaseModel):
    id: int
    filename: str
    input_type: str
    detected_vehicles: dict[str, int]
    detected_hazards: dict[str, int]
    severity: str
    latitude: float
    longitude: float
    location_name: str
    timestamp: str
    original_file_path: str
    processed_output_path: str
    processed_output_url: str

