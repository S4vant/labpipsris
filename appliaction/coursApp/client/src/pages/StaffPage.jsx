// src/pages/StaffPage.jsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios-instance";

export default function StaffPage() {
        const navigate = useNavigate(); // <- важно: должно быть внутри компонента
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState(""); // "staff" или "admin"
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [products, setProducts] = useState([]);
  const [brands, setBrands] = useState([]);
  const [brandFilter, setBrandFilter] = useState("");
  const [nameFilter, setNameFilter] = useState("");

  // === Проверка токена при загрузке страницы ===
 useEffect(() => {
  const checkSession = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const res = await axios.get("/auth/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const role = res.data.employee?.role;
      if (role) {
        setUserRole(role);
        setIsLoggedIn(true);
      }
    } catch (err) {
      console.log("Сессия недействительна", err);
      localStorage.removeItem("token");
    }
  };

  checkSession();
}, []);

  // Получение продуктов и брендов (только если залогинен)
  useEffect(() => {
    if (isLoggedIn) {
      axios.get("/products").then(res => setProducts(res.data));
      axios.get("/brands").then(res => setBrands(res.data));
    }
  }, [isLoggedIn]);

  // === Логин ===
 const handleLogin = async (e) => {
  e.preventDefault();
  try {
    const res = await axios.post("/auth/login", { username, password });
    const token = res.data.token;
    const role = res.data.employee?.role;

    if (token && role) {
      // сохраняем токен в localStorage
      localStorage.setItem("token", token);
      setUserRole(role);
      setIsLoggedIn(true);
    }
  } catch (err) {
    alert("Неверный логин или пароль");
  }
};

  // === Логаут ===
const handleLogout = async () => {
  const token = localStorage.getItem("token");
  if (!token) return;

  try {
    // POST на сервер, чтобы деактивировать сессию
    await axios.post("/auth/logout", null, {
      headers: { Authorization: `Bearer ${token}` }
    });
  } catch (err) {
    console.error("Ошибка логаута на сервере:", err);
  } finally {
    // Сбрасываем локально
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    setUserRole("");
  }
};

  const filteredProducts = products.filter(p =>
    (brandFilter ? p.brand === brandFilter : true) &&
    (nameFilter ? p.name.toLowerCase().includes(nameFilter.toLowerCase()) : true)
  );

  // Кнопки панели сотрудника
  const staffButtons = [
    { label: "Регистрация продукта", action: () => navigate("/staff/products") },
    { label: "Регистрация поставки", action: () => alert("Регистрация поставки") },
    { label: "Регистрация офлайн продажи", action: () => alert("Регистрация офлайн продажи") },
    { label: "Список покупателей", action: () => alert("Список покупателей") },
  ];

  if (userRole === "admin") {
    staffButtons.push({ label: "Создать сотрудника", action: () => alert("Создание сотрудника") });
  }

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial, sans-serif" }}>
      {/* Боковая панель */}
      <aside style={{ width: "250px", padding: "20px", borderRight: "1px solid #ccc", background: "#f8f8f8" }}>
        {!isLoggedIn ? (
          <form onSubmit={handleLogin}>
            <h2>Вход для сотрудников</h2>
            <input
              type="text"
              placeholder="Логин"
              value={username}
              onChange={e => setUsername(e.target.value)}
              style={{ width: "100%", marginBottom: "10px", padding: "5px" }}
            />
            <input
              type="password"
              placeholder="Пароль"
              value={password}
              onChange={e => setPassword(e.target.value)}
              style={{ width: "100%", marginBottom: "10px", padding: "5px" }}
            />
            <button type="submit" style={{ width: "100%", padding: "10px" }}>Войти</button>
          </form>
        ) : (
          <>
            <h2>Панель сотрудника</h2>
            <div style={{ marginBottom: "20px", padding: "10px", border: "1px solid #ccc", borderRadius: "8px" }}>
              <h3>Фильтр продуктов</h3>
              <select value={brandFilter} onChange={e => setBrandFilter(e.target.value)} style={{ width: "100%", marginBottom: "10px" }}>
                <option value="">Все бренды</option>
                {brands.map(b => <option key={b.id} value={b.name}>{b.name}</option>)}
              </select>
              <input
                type="text"
                placeholder="Название продукта"
                value={nameFilter}
                onChange={e => setNameFilter(e.target.value)}
                style={{ width: "100%", padding: "5px" }}
              />
            </div>

            {staffButtons.map(btn => (
              <div
                key={btn.label}
                onClick={btn.action}
                style={{
                  marginBottom: "10px",
                  padding: "10px",
                  border: "1px solid #000",
                  borderRadius: "5px",
                  textAlign: "center",
                  cursor: "pointer",
                  background: "#fff"
                }}
              >
                {btn.label}
              </div>
            ))}

            {/* Кнопка логаута */}
            <button
              onClick={handleLogout}
              style={{
                width: "100%",
                marginTop: "20px",
                padding: "10px",
                background: "#f44336",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
            >
              Выйти
            </button>
          </>
        )}
      </aside>

      {/* Основная часть */}
      <main style={{ flex: 1, padding: "20px", overflowY: "auto" }}>
        <header style={{ marginBottom: "20px", textAlign: "center" }}>
          <h1>MiniCloth Staff</h1>
        </header>

        {isLoggedIn && (
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))",
            gap: "20px"
          }}>
            {filteredProducts.map(p => (
              <div key={p.id} style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "10px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                minHeight: "200px"
              }}>
                <div style={{ width: "100%", height: "100px", background: "#eaeaea", marginBottom: "10px" }}></div>
                <h3>{p.name}</h3>
                <p>Категория: {p.category}</p>
                <p>Бренд: {p.brand}</p>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
