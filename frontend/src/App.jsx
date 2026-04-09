import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import HistoryPage from "./pages/HistoryPage";
import HomePage from "./pages/HomePage";
import MapPage from "./pages/MapPage";

export default function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="app-main">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/map" element={<MapPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

