import { useState } from "react";

export default function EmployeesAdmin() {
    const [form, setForm] = useState({
        username: "",
        password: "",
        role: "staff",
        master_key: ""
    });

    async function submit(e) {
        e.preventDefault();

        const res = await fetch("http://localhost:5000/api/staff/create", {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(form)
        });

        if (res.ok) {
            alert("Сотрудник добавлен");
        } else {
            alert("Ошибка");
        }
    }

    return (
        <form onSubmit={submit} className="card">
            <h3>Добавить сотрудника</h3>

            <input placeholder="Логин"
                onChange={e => setForm({ ...form, username: e.target.value })} />

            <input type="password" placeholder="Пароль"
                onChange={e => setForm({ ...form, password: e.target.value })} />

            <input placeholder="Мастер-ключ"
                onChange={e => setForm({ ...form, master_key: e.target.value })} />

            <select
                onChange={e => setForm({ ...form, role: e.target.value })}>
                <option value="staff">Сотрудник</option>
                <option value="admin">Администратор</option>
            </select>

            <button className="btn-primary">Создать</button>
        </form>
    );
}
