import { useState } from "react";
import api from "../../api/axios-instance";

export default function BrandsPage() {
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      await api.post("/brands", { name });
      setMessage("Бренд успешно добавлен");
      setName("");
    } catch (err) {
      setMessage(
        err.response?.data?.error || "Ошибка при создании бренда"
      );
    }
  };

  return (
    <div>
      <h2>Регистрация бренда</h2>

      <form onSubmit={handleSubmit} style={{ maxWidth: 400 }}>
        <input
          type="text"
          placeholder="Название бренда"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ width: "100%", padding: 8, marginBottom: 10 }}
        />

        <button type="submit" style={{ padding: 10, width: "100%" }}>
          Зарегистрировать бренд
        </button>
      </form>

      {message && <p style={{ marginTop: 10 }}>{message}</p>}
    </div>
  );
}
