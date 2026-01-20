import { Outlet, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "../api/axios-instance";
import { useProductFilters } from "../context/ProductFilterContext";

/* ===== ФИЛЬТРЫ (НЕ default export!) ===== */
function ProductFilters() {
  const { filters, setFilters } = useProductFilters();

   return (
    <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
      <input
        type="text"
        placeholder="Название"
        value={filters.name}
        onChange={(e) => setFilters({ ...filters, name: e.target.value })}
      />

      <select
        value={filters.category_id}
        onChange={(e) => setFilters({ ...filters, category_id: e.target.value })}
      >
        <option value="">Все категории</option>
        {categories.map((c) => (
          <option key={c.id} value={c.id}>
            {c.name}
          </option>
        ))}
      </select>

      <select
        value={filters.brand_id}
        onChange={(e) => setFilters({ ...filters, brand_id: e.target.value })}
      >
        <option value="">Все бренды</option>
        {brands.map((b) => (
          <option key={b.id} value={b.id}>
            {b.name}
          </option>
        ))}
      </select>
    </div>
  );
}

/* ===== ОСНОВНОЙ LAYOUT ===== */
export default function StaffLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  const isProductsPage = location.pathname === "/staff/products";

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState("");
  const [loading, setLoading] = useState(true);

  /* === Проверка сессии === */
  useEffect(() => {
    const checkSession = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const res = await axios.get("/auth/me", {
          headers: { Authorization: `Bearer ${token}` },
        });

        const role = res.data.employee?.role;
        if (role) {
          setUserRole(role);
          setIsLoggedIn(true);
        } else {
          localStorage.removeItem("token");
        }
      } catch {
        localStorage.removeItem("token");
      } finally {
        setLoading(false);
      }
    };

    checkSession();
  }, []);

  /* === ЛОГАУТ === */
  const handleLogout = async () => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      await axios.post("/auth/logout", null, {
        headers: { Authorization: `Bearer ${token}` },
      });
    } finally {
      localStorage.removeItem("token");
      setIsLoggedIn(false);
      setUserRole("");
      navigate("/");
    }
  };

  /* === КНОПКИ === */
  const staffButtons = [
    { label: "Регистрация продукта", action: () => navigate("/staff/products") },
    { label: "Категории", action: () => navigate("/staff/categories") },
    { label: "Бренды", action: () => navigate("/staff/brands") },
    { label: "Регистрация поставки", action: () => alert("Регистрация поставки") },
    { label: "Регистрация офлайн продажи", action: () => alert("Регистрация офлайн продажи") },
    { label: "Список покупателей", action: () => alert("Список покупателей") },
  ];

  if (userRole === "admin") {
    staffButtons.push({
      label: "Создать сотрудника",
      action: () => alert("Создание сотрудника"),
    });
  }

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial, sans-serif" }}>
      {/* ===== SIDEBAR ===== */}
      <aside
        style={{
          width: "250px",
          padding: "20px",
          borderRight: "1px solid #ccc",
          background: "#f8f8f8",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {loading ? (
          <p style={{ textAlign: "center" }}>Загрузка...</p>
        ) : !isLoggedIn ? (
          <p style={{ textAlign: "center" }}>Войдите, чтобы видеть панель</p>
        ) : (
          <>
            <h2>Панель сотрудника</h2>

            {/* ===== ФИЛЬТРЫ ТОЛЬКО НА /staff/products ===== */}
            {isProductsPage && (
              <div
                style={{
                  marginBottom: "20px",
                  padding: "10px",
                  border: "1px solid #ccc",
                  borderRadius: "8px",
                }}
              >
                <h3>Фильтр продуктов</h3>
                <ProductFilters />
              </div>
            )}

            {/* ===== КНОПКИ ===== */}
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
                  background: "#fff",
                }}
              >
                {btn.label}
              </div>
            ))}

            <button
              onClick={handleLogout}
              style={{
                marginTop: "auto",
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

      {/* ===== MAIN ===== */}
      <main style={{ flex: 1, padding: "20px", overflowY: "auto" }}>
        <header style={{ marginBottom: "20px", textAlign: "center" }}>
          <h1>MiniCloth Staff</h1>
        </header>

        <Outlet />
      </main>
    </div>
  );
}
