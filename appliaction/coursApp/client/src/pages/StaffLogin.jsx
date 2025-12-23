import { useState } from "react";

export default function StaffLogin() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    async function login(e) {
        e.preventDefault();

        fetch("http://localhost:5000/staff/login", {
  method: "POST",
  credentials: "include", // чтобы куки сессии шли
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ username, password })
})

        if (res.ok) {
            window.location.href = "/staff";
        } else {
            alert("Ошибка входа");
        }
    }

    return (
        <form className="card" onSubmit={login}>
            <h2>Вход для сотрудников</h2>

            <input
                placeholder="Логин"
                value={username}
                onChange={e => setUsername(e.target.value)}
            />

            <input
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={e => setPassword(e.target.value)}
            />

            <button className="btn-primary">Войти</button>
        </form>
    );
}
