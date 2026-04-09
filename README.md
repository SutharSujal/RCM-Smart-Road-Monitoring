# RCM (Road Condition Monitoring)

Full-stack local project for smart road monitoring and hazard reporting using:

- FastAPI + OpenCV + Ultralytics YOLO
- React + Vite + Leaflet
- SQLite (local database)
- Local file storage only (`backend/uploads`, `backend/outputs`)

No Firebase and no cloud dependency.

## Project Structure

```text
RCM/
 ├── backend/
 │   ├── app/
 │   │   ├── models/
 │   │   │   ├── best.pt
 │   │   │   ├── yolov8m.pt
 │   │   │   └── plate_blur_model.pt
 │   │   ├── routes/
 │   │   ├── services/
 │   │   ├── utils/
 │   │   └── main.py
 │   ├── uploads/
 │   ├── outputs/
 │   ├── rcm.db
 │   └── requirements.txt
 │
 ├── frontend/
 │   ├── src/
 │   └── package.json
```

## Backend Setup (Windows)

```powershell
cd C:\Users\sujal\OneDrive\Desktop\RCM\backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

Backend API docs: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

## Frontend Setup (Windows)

```powershell
cd C:\Users\sujal\OneDrive\Desktop\RCM\frontend
npm install
npm run dev
```

Frontend app: [http://127.0.0.1:5173](http://127.0.0.1:5173)

## Unified Pipeline Flow

Main endpoint used by frontend:

- `POST /api/pipeline/run`

Runs in exact order:

1. Vehicle detection (`yolov8m.pt`)
2. License plate blur (`plate_blur_model.pt`)
3. Road hazard detection (`best.pt`)
4. Severity calculation (`Low` / `Medium` / `High`)
5. SQLite save + local output save

## Additional API Routes

- Vehicle:
  - `POST /api/vehicle/image`
  - `POST /api/vehicle/video`
  - `POST /api/vehicle/live-frame`
- Plate blur:
  - `POST /api/plate/image`
  - `POST /api/plate/video`
  - `POST /api/plate/live-frame`
- Hazard:
  - `POST /api/hazard/image`
  - `POST /api/hazard/video`
  - `POST /api/hazard/live-frame`
- History:
  - `GET /api/detections`
  - `GET /api/detections/{id}`

## Notes

- Models are always loaded from `backend/app/models/`.
- Static outputs are served from `http://127.0.0.1:8001/static/...`.
- Map uses OpenStreetMap tiles (internet needed only for tile loading).
- All detection metadata is stored locally in `backend/rcm.db`.

Keep the implementation modular, stable, and fully runnable on Windows using VS Code terminal.
