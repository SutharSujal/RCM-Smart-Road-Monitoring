import { useEffect, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import L from "leaflet";
import { api } from "../api";

function markerColorFromSeverity(severity) {
  const value = (severity || "").toLowerCase();
  if (value === "high") return "#d7263d";
  if (value === "medium") return "#f4b400";
  return "#2e9e5b";
}

function markerIcon(color) {
  return L.divIcon({
    className: "custom-marker",
    html: `<div style="background:${color};width:18px;height:18px;border-radius:999px;border:2px solid #fff;box-shadow:0 2px 10px rgba(0,0,0,0.35);"></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9]
  });
}

export default function MapPage() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const response = await api.get("/api/detections");
        setItems(response.data.items || []);
      } catch (e) {
        setError(e.response?.data?.detail || "Failed to load map data.");
      }
    };
    load();
  }, []);

  return (
    <div className="page">
      <section className="panel">
        <h2>Road Condition Map</h2>
        <p className="muted">Green = Safe, Yellow = Moderate, Red = Hazardous</p>
      </section>
      {error && <p className="error">{error}</p>}

      <div className="map-wrap">
        <MapContainer center={[20.5937, 78.9629]} zoom={5} scrollWheelZoom className="map-container">
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {items.map((item) => {
            const mediaUrl = item.processed_output_url;
            const isVideo = item.processed_output_path.toLowerCase().endsWith(".mp4");
            return (
              <Marker
                key={item.id}
                position={[item.latitude, item.longitude]}
                icon={markerIcon(markerColorFromSeverity(item.severity))}
              >
                <Popup maxWidth={300}>
                  <div className="popup-box">
                    <strong>{item.location_name}</strong>
                    <p>Severity: {item.severity}</p>
                    <p>Time: {item.timestamp}</p>
                    <p>Vehicles: {JSON.stringify(item.detected_vehicles)}</p>
                    <p>Hazards: {JSON.stringify(item.detected_hazards)}</p>
                    {isVideo ? (
                      <video controls width="260" src={mediaUrl} />
                    ) : (
                      <img src={mediaUrl} width="260" alt="Processed output" />
                    )}
                  </div>
                </Popup>
              </Marker>
            );
          })}
        </MapContainer>
      </div>
    </div>
  );
}
