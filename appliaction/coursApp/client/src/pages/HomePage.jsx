import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios-instance";

export default function HomePage() {
    const navigate = useNavigate(); // <- важно: должно быть внутри компонента
  const [products, setProducts] = useState([]);
  const [brandFilter, setBrandFilter] = useState("");
  const [nameFilter, setNameFilter] = useState("");
  const [brands, setBrands] = useState([]);

  useEffect(() => {
    axios.get("/products").then(res => setProducts(res.data));
    axios.get("/brands").then(res => setBrands(res.data));
  }, []);

  const filteredProducts = products.filter(p =>
    (brandFilter ? p.brand === brandFilter : true) &&
    (nameFilter ? p.name.toLowerCase().includes(nameFilter.toLowerCase()) : true)
  );

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial, sans-serif" }}>
      {/* Боковая панель */}
      <aside style={{ width: "250px", padding: "20px", borderRight: "1px solid #ccc", background: "#f8f8f8" }}>
        <h2>Меню</h2>
        <button
        style={{ width: "100%", marginBottom: "20px" }}
        onClick={() => navigate("/staff")}
      >
        Для сотрудников
      </button>

        <div>
          <h3>Фильтр по бренду</h3>
          <select value={brandFilter} onChange={e => setBrandFilter(e.target.value)} style={{ width: "100%" }}>
            <option value="">Все бренды</option>
            {brands.map(b => (
              <option key={b.id} value={b.name}>{b.name}</option>
            ))}
          </select>
        </div>

        <div style={{ marginTop: "20px" }}>
          <h3>Фильтр по названию</h3>
          <input
            type="text"
            placeholder="Название продукта"
            value={nameFilter}
            onChange={e => setNameFilter(e.target.value)}
            style={{ width: "100%", padding: "5px" }}
          />
        </div>
      </aside>

      {/* Основная часть */}
      <main style={{ flex: 1, padding: "20px", overflowY: "auto" }}>
        <header style={{ marginBottom: "20px", textAlign: "center" }}>
          <h1>MiniCloth Store</h1>
        </header>

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
              <div style={{ width: "100%", height: "100px", background: "#eaeaea", marginBottom: "10px" }}>
                {/* Здесь место под картинку */}
              </div>
              <h3>{p.name}</h3>
              <p>Категория: {p.category}</p>
              <p>Бренд: {p.brand}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
