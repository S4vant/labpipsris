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
  value={filters.category_id ?? ""}
  onChange={(e) =>
    setFilters({
      ...filters,
      category_id: e.target.value ? Number(e.target.value) : null,
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
export default function UserLayout() {
  const navigate = useNavigate();
  const location = useLocation();



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
       
          {(
            <div style={{ marginBottom: "20px", padding: "10px", border: "1px solid #ccc', borderRadius: '8px" }}>
              <h3>Фильтр продуктов</h3>
              <ProductFilters />
            </div>
          )}
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
