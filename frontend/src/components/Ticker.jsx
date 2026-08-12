import { useEffect, useState } from "react";
import client from "../api/client";

export default function Ticker() {
  const [symbols, setSymbols] = useState([]);

  useEffect(() => {
    client.get("/api/symbols/").then((res) => setSymbols(res.data));
  }, []);

  //symbols.map((s) => ...): Loops through the fetched array of stock objects and renders an <li> for each one displaying its ticker and company name (e.g., AAPL — AAPL).

  return (
    <ul>
      {symbols.map((s) => (
        <li key={s.ticker}>{s.ticker} — {s.name}</li>
      ))}
    </ul>
  );
}


// fetches the watchlist once on mount using useEffect, sotres it in state, renders it
