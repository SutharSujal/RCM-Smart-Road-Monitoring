export default function SeverityBadge({ severity }) {
  const value = (severity || "Low").toLowerCase();
  return <span className={`severity severity-${value}`}>{severity || "Low"}</span>;
}

