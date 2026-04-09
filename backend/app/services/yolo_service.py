from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import cv2
from ultralytics import YOLO

from app.config import HAZARD_MODEL_PATH, PLATE_MODEL_PATH, VEHICLE_MODEL_PATH
from app.utils.file_utils import output_path_from_input
from app.utils.severity import calculate_severity


@dataclass
class FrameResult:
    frame: any
    vehicles: Counter
    hazards: Counter
    hazard_area_ratio_sum: float
    repeated_occurrence_score: int


class YoloService:
    def __init__(self) -> None:
        for model_path in [VEHICLE_MODEL_PATH, PLATE_MODEL_PATH, HAZARD_MODEL_PATH]:
            if not Path(model_path).exists():
                raise FileNotFoundError(f"Model not found: {model_path}")

        self.vehicle_model = YOLO(str(VEHICLE_MODEL_PATH))
        self.plate_model = YOLO(str(PLATE_MODEL_PATH))
        self.hazard_model = YOLO(str(HAZARD_MODEL_PATH))

        self.vehicle_allowed_classes = {
            "car",
            "bus",
            "truck",
            "motorcycle",
            "bicycle",
            "train",
            "van",
        }

    def _xyxy(self, box) -> tuple[int, int, int, int]:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        return int(x1), int(y1), int(x2), int(y2)

    def _safe_crop(self, frame, x1: int, y1: int, x2: int, y2: int):
        h, w = frame.shape[:2]
        x1 = max(0, min(x1, w - 1))
        x2 = max(0, min(x2, w))
        y1 = max(0, min(y1, h - 1))
        y2 = max(0, min(y2, h))
        if x2 <= x1 or y2 <= y1:
            return None, (x1, y1, x2, y2)
        return frame[y1:y2, x1:x2], (x1, y1, x2, y2)

    def _run_pipeline_on_frame(self, frame, previous_hazards: set[str] | None = None) -> FrameResult:
        if previous_hazards is None:
            previous_hazards = set()

        out_frame = frame.copy()
        frame_h, frame_w = out_frame.shape[:2]
        frame_area = max(frame_h * frame_w, 1)

        vehicles = Counter()
        hazards = Counter()
        hazard_area_ratio_sum = 0.0
        repeated_occurrence_score = 0

        # 1) Vehicle detection
        vehicle_results = self.vehicle_model.predict(out_frame, verbose=False)
        for result in vehicle_results:
            names = result.names
            for box in result.boxes:
                class_name = names[int(box.cls[0])]
                if class_name not in self.vehicle_allowed_classes:
                    continue
                vehicles[class_name] += 1
                x1, y1, x2, y2 = self._xyxy(box)
                cv2.rectangle(out_frame, (x1, y1), (x2, y2), (60, 190, 255), 2)
                cv2.putText(
                    out_frame,
                    class_name,
                    (x1, max(y1 - 8, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (60, 190, 255),
                    2,
                )

        # 2) Plate blur
        plate_results = self.plate_model.predict(out_frame, verbose=False)
        for result in plate_results:
            for box in result.boxes:
                x1, y1, x2, y2 = self._xyxy(box)
                crop, (cx1, cy1, cx2, cy2) = self._safe_crop(out_frame, x1, y1, x2, y2)
                if crop is None:
                    continue
                blurred = cv2.GaussianBlur(crop, (41, 41), 0)
                out_frame[cy1:cy2, cx1:cx2] = blurred

        # 3) Hazard detection
        current_hazard_classes = set()
        hazard_results = self.hazard_model.predict(out_frame, verbose=False)
        for result in hazard_results:
            names = result.names
            for box in result.boxes:
                class_name = names[int(box.cls[0])]
                current_hazard_classes.add(class_name)
                hazards[class_name] += 1
                x1, y1, x2, y2 = self._xyxy(box)
                area = max((x2 - x1) * (y2 - y1), 0)
                hazard_area_ratio_sum += area / frame_area
                cv2.rectangle(out_frame, (x1, y1), (x2, y2), (30, 50, 255), 2)
                cv2.putText(
                    out_frame,
                    class_name,
                    (x1, max(y1 - 8, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (30, 50, 255),
                    2,
                )

        repeated_occurrence_score = len(current_hazard_classes.intersection(previous_hazards))
        return FrameResult(
            frame=out_frame,
            vehicles=vehicles,
            hazards=hazards,
            hazard_area_ratio_sum=hazard_area_ratio_sum,
            repeated_occurrence_score=repeated_occurrence_score,
        )

    def process_image(self, image_path: Path) -> dict:
        frame = cv2.imread(str(image_path))
        if frame is None:
            raise ValueError("Failed to read image")

        result = self._run_pipeline_on_frame(frame)
        output_path = output_path_from_input(image_path, prefix="processed_image", suffix=".jpg")
        cv2.imwrite(str(output_path), result.frame)

        total_hazards = sum(result.hazards.values())
        avg_ratio = result.hazard_area_ratio_sum / max(total_hazards, 1)
        severity = calculate_severity(total_hazards, avg_ratio, 0)

        return {
            "output_path": str(output_path),
            "detected_vehicles": dict(result.vehicles),
            "detected_hazards": dict(result.hazards),
            "severity": severity,
            "hazard_area_avg_ratio": avg_ratio,
            "repeated_occurrence_score": 0,
        }

    def process_video(self, video_path: Path) -> dict:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError("Failed to open video")

        fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_path = output_path_from_input(video_path, prefix="processed_video", suffix=".mp4")
        writer = cv2.VideoWriter(
            str(output_path),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height),
        )

        total_vehicles = Counter()
        total_hazards = Counter()
        hazard_area_ratio_total = 0.0
        hazard_box_count_total = 0
        repeated_occurrence_score = 0
        previous_hazard_classes: set[str] = set()

        while True:
            ok, frame = cap.read()
            if not ok:
                break

            frame_result = self._run_pipeline_on_frame(frame, previous_hazard_classes)
            writer.write(frame_result.frame)
            total_vehicles.update(frame_result.vehicles)
            total_hazards.update(frame_result.hazards)
            hazard_area_ratio_total += frame_result.hazard_area_ratio_sum
            hazard_box_count_total += sum(frame_result.hazards.values())
            repeated_occurrence_score += frame_result.repeated_occurrence_score
            previous_hazard_classes = set(frame_result.hazards.keys())

        cap.release()
        writer.release()

        total_hazard_count = sum(total_hazards.values())
        avg_ratio = hazard_area_ratio_total / max(hazard_box_count_total, 1)
        severity = calculate_severity(total_hazard_count, avg_ratio, repeated_occurrence_score)

        return {
            "output_path": str(output_path),
            "detected_vehicles": dict(total_vehicles),
            "detected_hazards": dict(total_hazards),
            "severity": severity,
            "hazard_area_avg_ratio": avg_ratio,
            "repeated_occurrence_score": repeated_occurrence_score,
        }

    def run_vehicle_only_on_image(self, image_path: Path) -> dict:
        frame = cv2.imread(str(image_path))
        if frame is None:
            raise ValueError("Failed to read image")
        vehicle_counts = Counter()
        results = self.vehicle_model.predict(frame, verbose=False)
        for result in results:
            names = result.names
            for box in result.boxes:
                class_name = names[int(box.cls[0])]
                if class_name in self.vehicle_allowed_classes:
                    vehicle_counts[class_name] += 1
        return {"detected_vehicles": dict(vehicle_counts)}

    def run_hazard_only_on_image(self, image_path: Path) -> dict:
        frame = cv2.imread(str(image_path))
        if frame is None:
            raise ValueError("Failed to read image")
        out_frame = frame.copy()
        hazard_counts = Counter()
        results = self.hazard_model.predict(out_frame, verbose=False)
        for result in results:
            names = result.names
            for box in result.boxes:
                class_name = names[int(box.cls[0])]
                hazard_counts[class_name] += 1
        return {"detected_hazards": dict(hazard_counts)}

    def run_plate_blur_only_on_image(self, image_path: Path) -> dict:
        frame = cv2.imread(str(image_path))
        if frame is None:
            raise ValueError("Failed to read image")
        out_frame = frame.copy()
        plate_results = self.plate_model.predict(out_frame, verbose=False)
        blurred_count = 0
        for result in plate_results:
            for box in result.boxes:
                x1, y1, x2, y2 = self._xyxy(box)
                crop, (cx1, cy1, cx2, cy2) = self._safe_crop(out_frame, x1, y1, x2, y2)
                if crop is None:
                    continue
                out_frame[cy1:cy2, cx1:cx2] = cv2.GaussianBlur(crop, (41, 41), 0)
                blurred_count += 1
        output_path = output_path_from_input(image_path, prefix="plate_blur", suffix=".jpg")
        cv2.imwrite(str(output_path), out_frame)
        return {"blurred_plates": blurred_count, "output_path": str(output_path)}
