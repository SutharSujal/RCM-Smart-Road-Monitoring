import SeverityBadge from "./SeverityBadge";

function SummaryList({ title, data }) {
  const entries = Object.entries(data || {});
  return (
    <div>
      <p className="summary-title">{title}</p>
      {entries.length === 0 ? (
        <p className="muted">None</p>
      ) : (
        <ul className="summary-list">
          {entries.map(([key, count]) => (
            <li key={key}>
              <span>{key}</span>
              <strong>{count}</strong>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default function ResultCard({ result }) {
  if (!result) {
    return null;
  }

  const mediaUrl = result.processed_output_url;
  const isVideo = result.processed_output_path.toLowerCase().endsWith(".mp4");

  return (
    <article className="result-card">
      <div className="result-media">
        {isVideo ? (
          <video controls src={mediaUrl} />
        ) : (
          <img src={mediaUrl} alt="Processed detection output" />
        )}
      </div>
      <div className="result-content">
        <div className="result-head">
          <h3>Detection Result #{result.id}</h3>
          <SeverityBadge severity={result.severity} />
        </div>
        <p>
          <strong>Location:</strong> {result.location_name} ({result.latitude}, {result.longitude})
        </p>
        <p>
          <strong>Input:</strong> {result.input_type} | <strong>Timestamp:</strong> {result.timestamp}
        </p>
        <div className="summary-grid">
          <SummaryList title="Vehicles" data={result.detected_vehicles} />
          <SummaryList title="Hazards" data={result.detected_hazards} />
        </div>
      </div>
    </article>
  );
}
