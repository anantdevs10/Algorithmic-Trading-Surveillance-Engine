import { useState } from "react";
import LiveTicker from "./components/Ticker";
import AlertTable from "./components/AlertTable";
import BacktestPanel from "./components/BacktestPanel";
import PositionsPanel from "./components/PositionsPanel";
import Login from "./components/Login";

export default function App() {
  const [token, setToken] = useState(null);

  if (!token) return <Login onLogin={setToken} />;

  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
      <LiveTicker symbol="AAPL" />
      <AlertTable />
      <BacktestPanel />
      <PositionsPanel />
    </div>
  );
}