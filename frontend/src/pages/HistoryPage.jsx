import { useEffect, useState } from "react";
import { api } from "../api";
import ResultCard from "../components/ResultCard";

export default function HistoryPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const response = await api.get("/api/detections");
        setItems(response.data.items || []);
      } catch (e) {
        setError(e.response?.data?.detail || "Failed to load history.");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div className="page">
      <section className="panel">
        <h2>Detection History</h2>
        <p className="muted">All records saved in local SQLite database.</p>
      </section>
      {loading && <p>Loading history...</p>}
      {error && <p className="error">{error}</p>}
      {!loading && !error && items.length === 0 && <p>No detections found yet.</p>}
      <div className="history-list">
        {items.map((item) => (
          <ResultCard key={item.id} result={item} />
        ))}
      </div>
    </div>
  );
}

