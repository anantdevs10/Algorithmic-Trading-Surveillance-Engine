import LiveTicker from "./components/Ticker";
import AlertTable from "./components/AlertTable";
import BacktestPanel from "./components/BacktestPanel";
import PositionsPanel from "./components/PositionsPanel";

export default function App() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", padding: "1rem" }}>
      <LiveTicker symbol="AAPL" />
      <AlertTable />
      <BacktestPanel />
      <PositionsPanel />
    </div>
  );
}