import { useEffect, useState } from "react";
import client from "../api/client";

const SEVERITY_COLORS = {
  low: "#facc15", medium: "#fb923c", high: "#f87171", critical: "#dc2626",
};

export default function AlertTable() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    client.get("/api/alerts/").then((r) => setAlerts(r.data));
  }, []);

  useEffect(() => {
  const ws = new WebSocket("ws://localhost:8000/ws/alerts");
  ws.onmessage = (event) => {
    const newAlert = JSON.parse(event.data);
    setAlerts((prev) => [newAlert, ...prev]); // prepend, newest first
  };
  return () => ws.close();
    }, []);

  return (
    <table>
      <thead><tr><th>Ticker</th><th>Flags</th><th>Severity</th><th>Time</th></tr></thead>
      <tbody>
        {alerts.map((a) => (
          <tr key={a.id} style={{ background: SEVERITY_COLORS[a.severity] }}>
            <td>{a.ticker}</td><td>{a.rule_flags}</td>
            <td>{a.severity}</td><td>{new Date(a.timestamp).toLocaleTimeString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}