import { useEffect, useState } from "react";
import client from "../api/client";

export default function Ticker() {
  const [symbols, setSymbols] = useState([]);

  useEffect(() => {
    client.get("/api/symbols/").then((res) => setSymbols(res.data));
  }, []);

  return (
    <ul>
      {symbols.map((s) => (
        <li key={s.ticker}>{s.ticker} — {s.name}</li>
      ))}
    </ul>
  );
}