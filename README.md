# 🚧 RCM (Road Condition Monitoring)

RCM (Road Condition Monitoring) is a full-stack AI-based system that analyzes road images, videos, and live camera feeds to detect vehicles, blur license plates, identify road hazards, and visualize road conditions on a map.

The system runs completely locally with no cloud dependency.

---

## 🔥 Features

- 📷 Image, Video, and Live Camera input  
- 🚗 Vehicle Detection (YOLOv8)  
- 🔒 License Plate Blurring  
- ⚠️ Hazard Detection (Potholes, Debris, Speed Breakers)  
- 📊 Severity Classification (Low / Medium / High)  
- 📍 Location Support (Auto + Manual)  
- 🗺️ Map Visualization (Leaflet)  
- 💾 Local Storage (SQLite + Files)  

---

## 🧠 System Workflow

```
Input (Image / Video / Live)
        ↓
Vehicle Detection (yolov8m.pt)
        ↓
Plate Blur (plate_blur_model.pt)
        ↓
Hazard Detection (best.pt)
        ↓
Severity Calculation
        ↓
Location Capture
        ↓
Save (SQLite + Files)
        ↓
Display + Map
```

---

## 🛠️ Tech Stack

- Frontend: React + Vite  
- Backend: FastAPI  
- Models: YOLOv8 (Ultralytics)  
- Processing: OpenCV  
- Database: SQLite  
- Map: Leaflet  

---

## 🧠 Models

| Model | Purpose |
|------|--------|
| yolov8m.pt | Vehicle Detection |
| plate_blur_model.pt | Plate Detection & Blur |
| best.pt | Hazard Detection |

📂 Location:  
backend/app/models/

---

## 📁 Project Structure

```
RCM/
 ├── backend/
 │   ├── app/
 │   │   ├── models/
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

---

## ⚙️ Setup

### Clone

```
git clone https://github.com/SutharSujal/RCM-Smart-Road-Monitoring.git
cd RCM-Smart-Road-Monitoring
```

---

## Backend

```
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Docs:  
http://127.0.0.1:8001/docs

---

## Frontend

```
cd frontend
npm install
npm run dev
```

App:  
http://localhost:5173

---

## ⚙️ Proxy Config

Edit frontend/vite.config.js:

```
server: {
  proxy: {
    "/api": "http://127.0.0.1:8001",
    "/outputs": "http://127.0.0.1:8001"
  }
}
```

---

## 🔗 API

### Main Pipeline

POST /api/pipeline/run

### Other Routes

Vehicle:
- /api/vehicle/image  
- /api/vehicle/video  
- /api/vehicle/live-frame  

Plate:
- /api/plate/image  
- /api/plate/video  
- /api/plate/live-frame  

Hazard:
- /api/hazard/image  
- /api/hazard/video  
- /api/hazard/live-frame  

History:
- /api/detections  
- /api/detections/{id}  

---

## 🗺️ Map

- 🟢 Green → Safe  
- 🟡 Yellow → Moderate  
- 🔴 Red → Hazardous  

---

## 💾 Storage

Files:
backend/uploads/  
backend/outputs/  

Database:
backend/rcm.db  

---

## ⚠️ Notes

- Ensure models exist in: backend/app/models/
- Backend must run on same port as proxy (default: 8001)

---

## 👨‍💻 Author

Sujal Suthar
