import sqlite3
from contextlib import contextmanager

from app.config import DB_PATH


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                input_type TEXT NOT NULL,
                detected_vehicles TEXT NOT NULL,
                detected_hazards TEXT NOT NULL,
                severity TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                location_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                original_file_path TEXT NOT NULL,
                processed_output_path TEXT NOT NULL
            )
            """
        )
        conn.commit()


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

