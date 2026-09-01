import { useState } from "react";
import client from "../api/client";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const form = new URLSearchParams({ username, password });
    const res = await client.post("/api/auth/login/", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    client.defaults.headers.common["Authorization"] = `Bearer ${res.data.access_token}`;
    onLogin(res.data.access_token);
  };

  return (
    <div>
      <input placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
      <input placeholder="Password" type="password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Log in</button>
    </div>
  );
}   