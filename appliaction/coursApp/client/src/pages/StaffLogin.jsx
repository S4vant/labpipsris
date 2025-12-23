// pages/StaffLogin.jsx
import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";

export default function StaffLogin() {
  const { saveUser } = useContext(UserContext);
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  async function submit(e) {
    e.preventDefault();
    setError(null);

    const res = await fetch("http://localhost:5000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, password })
    });

    if (!res.ok) {
      setError("Неверный логин или пароль");
      return;
    }

    const data = await res.json();
    saveUser(data.employee);
    navigate("/staff");
  }

  return (
    <form onSubmit={submit}>
      <h2>Staff Login</h2>
      {error && <p>{error}</p>}
      <input value={username} onChange={e => setUsername(e.target.value)} />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button>Login</button>
    </form>
  );
}
