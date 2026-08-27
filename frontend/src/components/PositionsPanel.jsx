import { useEffect, useState } from "react";
import client from "../api/client";

export default function PositionsPanel() {
  const [positions, setPositions] = useState([]);

  const refresh = () => client.get("/api/paper-trade/positions/").then((r) => setPositions(r.data));

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 5000); // poll every 5s
    return () => clearInterval(id);
  }, []);

  return (
    <table>
      <thead><tr><th>Ticker</th><th>Qty</th><th>Avg Price</th><th>Unrealized P&L</th></tr></thead>
      <tbody>
        {positions.map((p) => (
          <tr key={p.ticker}>
            <td>{p.ticker}</td><td>{p.quantity}</td>
            <td>{p.avg_price.toFixed(2)}</td><td>{p.unrealized_pnl.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}