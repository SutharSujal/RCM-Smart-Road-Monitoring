import { useMemo, useRef, useState } from "react";
import { api } from "../api";
import ResultCard from "../components/ResultCard";

function buildLocationName(stateName, defaultName = "Unknown Location") {
  return stateName && stateName.trim() ? stateName : defaultName;
}

export default function HomePage() {
  const [inputType, setInputType] = useState("image");
  const [selectedFile, setSelectedFile] = useState(null);
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");
  const [locationName, setLocationName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [cameraOn, setCameraOn] = useState(false);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const acceptType = useMemo(() => (inputType === "video" ? "video/*" : "image/*"), [inputType]);

  const startCamera = async () => {
    setError("");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setCameraOn(true);
    } catch (e) {
      setError("Unable to access webcam. Please allow camera permission.");
    }
  };

  const stopCamera = () => {
    const stream = streamRef.current;
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }
    streamRef.current = null;
    setCameraOn(false);
  };

  const captureLiveFrame = async () => {
    if (!videoRef.current) {
      throw new Error("Webcam is not active.");
    }
    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.videoWidth || 640;
    canvas.height = videoRef.current.videoHeight || 360;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    return new Promise((resolve) => {
      canvas.toBlob((blob) => {
        resolve(new File([blob], "live_frame.jpg", { type: "image/jpeg" }));
      }, "image/jpeg");
    });
  };

  const fetchCurrentLocation = () => {
    if (!navigator.geolocation) {
      setError("Geolocation is not supported in this browser.");
      return;
    }
    setError("");
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLatitude(String(pos.coords.latitude));
        setLongitude(String(pos.coords.longitude));
        if (!locationName.trim()) {
          setLocationName("Auto Live Location");
        }
      },
      () => {
        setError("Failed to read location. Enter manually.");
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (!latitude || !longitude) {
        throw new Error("Latitude and longitude are required.");
      }

      let fileToUpload = selectedFile;
      if (inputType === "live") {
        fileToUpload = await captureLiveFrame();
      }
      if (!fileToUpload) {
        throw new Error("Please select a file or start live camera.");
      }

      const formData = new FormData();
      formData.append("input_type", inputType);
      formData.append("latitude", latitude);
      formData.append("longitude", longitude);
      formData.append("location_name", buildLocationName(locationName, "Manual Location"));
      formData.append("file", fileToUpload);

      const response = await api.post("/api/pipeline/run", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setResult(response.data.result);
    } catch (e) {
      setError(e.response?.data?.detail || e.message || "Detection failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <section className="panel">
        <h2>Road Condition Monitoring</h2>
        <p className="muted">Upload image/video or capture live webcam frame with location.</p>
        <form onSubmit={submit} className="form-grid">
          <label>
            Input Type
            <select value={inputType} onChange={(e) => setInputType(e.target.value)}>
              <option value="image">Uploaded Image</option>
              <option value="video">Uploaded Video</option>
              <option value="live">Live Webcam Frame</option>
            </select>
          </label>

          {inputType !== "live" ? (
            <label>
              Select File
              <input type="file" accept={acceptType} onChange={(e) => setSelectedFile(e.target.files?.[0] || null)} />
            </label>
          ) : (
            <div className="live-box">
              <div className="live-actions">
                {!cameraOn ? (
                  <button type="button" onClick={startCamera}>
                    Start Camera
                  </button>
                ) : (
                  <button type="button" onClick={stopCamera}>
                    Stop Camera
                  </button>
                )}
              </div>
              <video ref={videoRef} autoPlay playsInline muted className="live-video" />
            </div>
          )}

          <div className="location-row">
            <button type="button" onClick={fetchCurrentLocation}>
              Use Auto Live Location
            </button>
          </div>

          <label>
            Latitude
            <input value={latitude} onChange={(e) => setLatitude(e.target.value)} placeholder="e.g. 28.6139" />
          </label>
          <label>
            Longitude
            <input value={longitude} onChange={(e) => setLongitude(e.target.value)} placeholder="e.g. 77.2090" />
          </label>
          <label>
            Location Name
            <input
              value={locationName}
              onChange={(e) => setLocationName(e.target.value)}
              placeholder="Road / Junction name"
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Running Detection..." : "Run Unified Detection Pipeline"}
          </button>
        </form>

        {error && <p className="error">{error}</p>}
      </section>

      <ResultCard result={result} />
    </div>
  );
}

