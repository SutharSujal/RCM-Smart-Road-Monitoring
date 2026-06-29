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
<img width="445" height="266" alt="processed_image_20260417_182911_0eee888a" src="https://github.com/user-attachments/assets/a7c8cbf7-8765-448f-a9b2-36f450d56a0a" />

Hazard:
- /api/hazard/image  
- /api/hazard/video  
- /api/hazard/live-frame  
<img width="886" height="595" alt="processed_image_20260409_232830_73ff8838" src="https://github.com/user-attachments/assets/97366360-6dc2-42e9-9ba3-f31b53d9ba88" />

History:
- /api/detections  
- /api/detections/{id}  
<img width="1884" height="920" alt="Screenshot 2026-04-17 183420" src="https://github.com/user-attachments/assets/3590f19b-bc6f-4fc3-99d7-a9f813e31d07" />

---

## 🗺️ Map

- 🟢 Green → Safe  
- 🟡 Yellow → Moderate  
- 🔴 Red → Hazardous  

---
<img width="1888" height="921" alt="Screenshot 2026-04-17 182812" src="https://github.com/user-attachments/assets/5cc1048f-d576-45a4-a05e-264f6cedd2d3" />

<img width="1893" height="921" alt="Screenshot 2026-04-17 182736" src="https://github.com/user-attachments/assets/4a53121b-bff8-499f-af9c-73c89878aa2e" />


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
