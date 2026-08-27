import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

export default function LiveTicker({ symbol = "AAPL" }) {
  const [ticks, setTicks] = useState([]);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/live-feed/${symbol}`);
    ws.onmessage = (event) => {
      const tick = JSON.parse(event.data);
      setTicks((prev) => [...prev.slice(-49), tick]); // keep last 50 points
    };
    return () => ws.close();
  }, [symbol]);

  return (
    <LineChart width={600} height={250} data={ticks}>
      <XAxis dataKey="volume" hide />
      <YAxis domain={["auto", "auto"]} />
      <Tooltip />
      <Line type="monotone" dataKey="price" dot={false} />
    </LineChart>
  );
}