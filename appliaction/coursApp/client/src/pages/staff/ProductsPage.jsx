import React, { useState, useEffect } from "react";
import axios from "../../api/axios-instance";
import { useProductFilters } from "/src/context/ProductFilterContext";
export default function StaffProductsPage() {
  const [showForm, setShowForm] = useState(false);
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);
  const [products, setProducts] = useState([]);
  const { filters } = useProductFilters();
    const [isLoggedIn, setIsLoggedIn] = useState(false);
  const { name, brand_id, category_id } = filters;
  const [newProduct, setNewProduct] = useState({
    name: "",
    price: "",
    category_id: "",
    brand_id: "",
    stock: "",
  });
    useEffect(() => {
  console.log("FILTERS FROM PAGE:", filters);
}, [filters]);
  useEffect(() => {
  console.log("PRODUCTS:", products);
}, [products]);

  useEffect(() => {
    if (isLoggedIn) {
      axios.get("/products").then(res => setProducts(res.data));
    }
  }, [isLoggedIn]);
  
  // Фильтруем продукты по контексту
const filteredProducts = products.filter(p => {
  if (filters.name && !p.name.toLowerCase().includes(filters.name.toLowerCase())) {
    return false;
  }

  if (filters.brand_id !== null && p.brand?.id !== filters.brand_id) {
    return false;
  }

  if (filters.category_id !== null && p.category?.id !== filters.category_id) {
    return false;
  }

  return true;
});

  // Получаем список продуктов
  const fetchProducts = async () => {
    try {
      const res = await axios.get("/products");
      setProducts(res.data || []);
    } catch (err) {
      console.error("Ошибка получения продуктов", err);
    }
  };

  // Получаем категории и бренды для формы
  const fetchDictionaries = async () => {
    try {
      const [categoriesRes, brandsRes] = await Promise.all([
        axios.get("/categories"),
        axios.get("/brands"),
      ]);
      setCategories(categoriesRes.data || []);
      setBrands(brandsRes.data || []);
    } catch (err) {
      console.error("Ошибка загрузки категорий и брендов", err);
    }
  };

  useEffect(() => {
    fetchProducts();
    fetchDictionaries();
  }, []);

  const handleInputChange = (e) => {
    setNewProduct({ ...newProduct, [e.target.name]: e.target.value });
  };

  const handleAddProduct = async (e) => {
    e.preventDefault();
    if (!newProduct.name || !newProduct.price || !newProduct.category_id || !newProduct.brand_id) {
      alert("Заполните все поля");
      return;
    }
    try {
      await axios.post("/products", {
        ...newProduct,
        price: Number(newProduct.price),
        category_id: Number(newProduct.category_id),
        brand_id: Number(newProduct.brand_id),
      });
      setShowForm(false);
      setNewProduct({ name: "", price: "", category_id: "", brand_id: "" });
      fetchProducts();
    } catch (err) {
      console.error("Ошибка добавления продукта", err);
      alert(err.response?.data?.error || "Ошибка добавления продукта");
    }
  };

  const handleDeleteProduct = async (id) => {
    if (!window.confirm("Удалить этот продукт?")) return;
    try {
      await axios.delete(`/products/${id}`);
      fetchProducts();
    } catch (err) {
      console.error("Ошибка удаления продукта", err);
      alert(err.response?.data?.error || "Ошибка удаления продукта");
    }
  };

  const handleEditProduct = async (id) => {
    const prod = products.find((p) => p.id === id);
    const updatedName = prompt("Новое название:", prod.name);
    if (!updatedName) return;
    try {
      await axios.put(`/products/${id}`, { ...prod, name: updatedName });
      fetchProducts();
    } catch (err) {
      console.error("Ошибка редактирования продукта", err);
      alert(err.response?.data?.error || "Ошибка редактирования продукта");
    }
  };

  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: "20px", padding: "20px" }}>
      {/* Карточка для добавления нового продукта */}
      <div
        onClick={() => setShowForm(true)}
        style={{
          border: "1px dashed #333",
          width: "200px",
          height: "250px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
          fontWeight: "bold",
          textAlign: "center",
        }}
      >
        Регистрация нового продукта
      </div>

      {/* Форма для нового продукта */}
      {showForm && (
        <form
          onSubmit={handleAddProduct}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            display: "flex",
            flexDirection: "column",
            gap: "5px",
            width: "220px",
          }}
        >
          <input
            type="text"
            placeholder="Название"
            name="name"
            value={newProduct.name}
            onChange={handleInputChange}
            required
          />
          <input
            type="number"
            placeholder="Цена"
            name="price"
            value={newProduct.price}
            onChange={handleInputChange}
            required
          />

          {/* Выбор категории */}
          <select
            name="category_id"
            value={newProduct.category_id}
            onChange={handleInputChange}
            required
          >
            <option value="">Выберите категорию</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>

          {/* Выбор бренда */}
          <select
            name="brand_id"
            value={newProduct.brand_id}
            onChange={handleInputChange}
            required
          >
            <option value="">Выберите бренд</option>
            {brands.map((b) => (
              <option key={b.id} value={b.id}>
                {b.name}
              </option>
            ))}
          </select>

          <button type="submit">Добавить</button>
          <button type="button" onClick={() => setShowForm(false)}>
            Отмена
          </button>
        </form>
      )}

      {/* Существующие продукты */}
      {filteredProducts.map((product) => (
        <div
          key={product.id}
          style={{
            border: "1px solid #ccc",
            width: "200px",
            height: "250px",
            padding: "10px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
          }}
        >
          <div>
            <h3>{product.name}</h3>
            <p>Категория: {product.category?.name || "—"}</p>
            <p>Бренд: {product.brand?.name || "—"}</p>
            <div
              style={{
                width: "100%",
                height: "80px",
                background: "#f0f0f0",
                marginTop: "5px",
              }}
            />
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", marginTop: "5px" }}>
            <button onClick={() => handleEditProduct(product.id)}>Редактировать</button>
            <button onClick={() => handleDeleteProduct(product.id)}>Удалить</button>
          </div>
        </div>
      ))}
    </div>
  );
}
