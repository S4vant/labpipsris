import { useState } from "react";
import axios from "../api/axios-instance";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState(""); // admin/staff/user
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post("/auth/login", { username, password });
      if(res.data.role === "user") navigate("/user");
      else navigate("/staff");
    } catch (e) {
      alert(e.response?.data?.error || "Ошибка авторизации");
    }
  };

  return (
    <div>
      <h1>Вход</h1>
      <input placeholder="Логин" value={username} onChange={e => setUsername(e.target.value)} />
      <input placeholder="Пароль" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Войти</button>
    </div>
  )
}
