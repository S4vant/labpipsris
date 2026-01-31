import { Outlet, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect, use } from "react";
import axios from "../api/axios-instance";
import { useProductFilters } from "../context/ProductFilterContext";

/* ===== ФИЛЬТРЫ ===== */
function ProductFilters() {
  const { filters, setFilters } = useProductFilters();
  const [brands, setBrands] = useState([]);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    axios.get("/brands").then(res => setBrands(res.data));
    axios.get("/categories").then(res => setCategories(res.data));
  }, []);
  useEffect(() => {
  console.log("FILTERS FROM SIDEBAR:", filters);
}, [filters]);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
      <input
        type="text"
        placeholder="Название"
        value={filters.name}
        onChange={(e) => setFilters({ ...filters, name: e.target.value })}
      />

      <select
        value={filters.categories_id ?? ""}
        onChange={(e) =>
          setFilters({
            ...filters,
            categories_id: e.target.value ? Number(e.target.value) : null,
          })
        }
      >
        <option value="">Все Категории</option>
        {categories.map(b => (
          <option key={b.id} value={b.id}>{b.name}</option>
        ))}
      </select>

      <select
        value={filters.brand_id ?? ""}
        onChange={(e) =>
          setFilters({
            ...filters,
            brand_id: e.target.value ? Number(e.target.value) : null,
          })
        }
      >
        <option value="">Все бренды</option>
        {brands.map(b => (
          <option key={b.id} value={b.id}>{b.name}</option>
        ))}
      </select>
    </div>
  );
}

/* ===== LAYOUT ===== */
export default function StaffLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const isProductsPage = location.pathname === "/staff/products";
  const [username, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [authError, setAuthError] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      const token = localStorage.getItem("token");
      if (!token) { setLoading(false); return; }

      try {
        const res = await axios.get("/auth/me", { headers: { Authorization: `Bearer ${token}` } });
        const role = res.data.employee?.role;
        if (role) { setUserRole(role); setIsLoggedIn(true); }
        else localStorage.removeItem("token");
      } catch { localStorage.removeItem("token"); }
      finally { setLoading(false); }
    };
    checkSession();
  }, []);

  const handleLogout = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      await axios.post("/auth/logout", null, { headers: { Authorization: `Bearer ${token}` } });
    } finally {
      localStorage.removeItem("token");
      setIsLoggedIn(false);
      setUserRole("");
      navigate("/");
    }
  };
  const handleLogin = async (e) => {
  e.preventDefault();
  setAuthError("");

  try {
    const res = await axios.post("/auth/login", {
      username,
      password,
    });

    const token = res.data.token;
    if (!token) throw new Error("No token");

    localStorage.setItem("token", token);

    const me = await axios.get("/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    });

    const role = me.data.employee?.role;
    if (!role) throw new Error("No role");

    setUserRole(role);
    setIsLoggedIn(true);
  } catch {
    setAuthError("Неверный логин или пароль");
    localStorage.removeItem("token");
  }
};

  const staffButtons = [
    { label: "Регистрация продукта", action: () => navigate("/staff/products") },
    { label: "Категории", action: () => navigate("/staff/categories") },
    { label: "Бренды", action: () => navigate("/staff/brands") },
    { label: "Регистрация поставки", action: () => alert("Регистрация поставки") },
    { label: "Регистрация офлайн продажи", action: () => alert("Регистрация офлайн продажи") },
    { label: "Список покупателей", action: () => alert("Список покупателей") },
  ];
  
  if (userRole === "admin") staffButtons.push({ label: "Создать сотрудника", action: () => alert("Создание сотрудника") });

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial, sans-serif" }}>
      {/* SIDEBAR */}
      <aside style={{
        width: "250px",
        padding: "20px",
        borderRight: "1px solid #ccc",
        background: "#f8f8f8",
        display: "flex",
        flexDirection: "column",
      }}>
        {loading ? <p style={{ textAlign: "center" }}>Загрузка...</p> :
         !isLoggedIn ? (
  <form
    onSubmit={handleLogin}
    style={{ display: "flex", flexDirection: "column", gap: "10px" }}
  >
    <h3 style={{ textAlign: "center" }}>Вход для сотрудников</h3>

    <input
      type="text"
      placeholder="Логин"
      value={username}
      onChange={(e) => setLogin(e.target.value)}
      required
    />

    <input
      type="password"
      placeholder="Пароль"
      value={password}
      onChange={(e) => setPassword(e.target.value)}
      required
    />

    {authError && (
      <span style={{ color: "red", fontSize: "14px", textAlign: "center" }}>
        {authError}
      </span>
    )}

    <button type="submit" style={{
      padding: "10px",
      cursor: "pointer"
    }}>
      Войти
    </button>
  </form>
) :
         <>
          <h2>Панель сотрудника</h2>
          {isProductsPage && (
            <div style={{ marginBottom: "20px", padding: "10px", border: "1px solid #ccc', borderRadius: '8px" }}>
              <h3>Фильтр продуктов</h3>
              <ProductFilters />
            </div>
          )}

          {staffButtons.map(btn => (
            <div key={btn.label} onClick={btn.action} style={{
              marginBottom: "10px", padding: "10px", border: "1px solid #000",
              borderRadius: "5px", textAlign: "center", cursor: "pointer", background: "#fff"
            }}>{btn.label}</div>
          ))}

          <button onClick={handleLogout} style={{
            marginTop: "auto", padding: "10px", background: "#f44336",
            color: "#fff", border: "none", borderRadius: "5px", cursor: "pointer"
          }}>Выйти</button>
         </>
        }
      </aside>

      {/* MAIN */}
      <main style={{ flex: 1, padding: "20px", overflowY: "auto" }}>
        <header style={{ marginBottom: "20px", textAlign: "center" }}>
          <h1>MiniCloth Staff</h1>
        </header>
        <Outlet />
      </main>
    </div>
  );
}
