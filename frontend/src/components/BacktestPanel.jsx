import { useState } from "react";
import client from "../api/client";

export default function BacktestPanel() {
  const [symbol, setSymbol] = useState("AAPL");
  const [result, setResult] = useState(null);

  const runBacktest = async () => {
    const res = await client.post(`/api/backtest/?symbol=${symbol}`);
    setResult(res.data);
  };

  return (
    <div>
      <input value={symbol} onChange={(e) => setSymbol(e.target.value)} />
      <button onClick={runBacktest}>Run Backtest</button>
      {result && (
        <ul>
          <li>Return: {(result.return * 100).toFixed(2)}%</li>
          <li>Win Rate: {(result.win_rate * 100).toFixed(2)}%</li>
          <li>Max Drawdown: {(result.max_drawdown * 100).toFixed(2)}%</li>
        </ul>
      )}
    </div>
  );
}