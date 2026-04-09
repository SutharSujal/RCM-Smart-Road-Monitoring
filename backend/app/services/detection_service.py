import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import BASE_DIR
from app.database import get_db


def _relative_to_backend(path: str) -> str:
    p = Path(path)
    try:
        return str(p.relative_to(BASE_DIR)).replace("\\", "/")
    except ValueError:
        return str(p).replace("\\", "/")


def save_detection_record(
    *,
    filename: str,
    input_type: str,
    detected_vehicles: dict[str, int],
    detected_hazards: dict[str, int],
    severity: str,
    latitude: float,
    longitude: float,
    location_name: str,
    original_file_path: str,
    processed_output_path: str,
) -> int:
    timestamp = datetime.now().isoformat(timespec="seconds")
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO detections (
                filename, input_type, detected_vehicles, detected_hazards, severity,
                latitude, longitude, location_name, timestamp, original_file_path,
                processed_output_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                filename,
                input_type,
                json.dumps(detected_vehicles),
                json.dumps(detected_hazards),
                severity,
                latitude,
                longitude,
                location_name,
                timestamp,
                _relative_to_backend(original_file_path),
                _relative_to_backend(processed_output_path),
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def list_detection_records() -> list[dict]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM detections ORDER BY id DESC")
        rows = cursor.fetchall()

    records = []
    for row in rows:
        record = dict(row)
        record["detected_vehicles"] = json.loads(record["detected_vehicles"])
        record["detected_hazards"] = json.loads(record["detected_hazards"])
        output_rel = record["processed_output_path"]
        record["processed_output_url"] = f"/static/{output_rel}"
        records.append(record)
    return records


def get_detection_record(record_id: int) -> Optional[dict]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM detections WHERE id = ?", (record_id,))
        row = cursor.fetchone()

    if row is None:
        return None

    record = dict(row)
    record["detected_vehicles"] = json.loads(record["detected_vehicles"])
    record["detected_hazards"] = json.loads(record["detected_hazards"])
    record["processed_output_url"] = f"/static/{record['processed_output_path']}"
    return record
