import React, { useState, useEffect } from "react";
import axios from "../../api/axios-instance";
import { useProductFilters } from "/src/context/ProductFilterContext";
export default function UserProductsPage() {
  const [products, setProducts] = useState([]);
  const { filters } = useProductFilters();
    const [isLoggedIn, setIsLoggedIn] = useState(false);
  const { name, brand_id, category_id } = filters;

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

  return (
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
          minHeight: "200px",
          
        }}>
          <div style={{ width: "100%", height: "100px", background: "#eaeaea", marginBottom: "10px" }}></div>
          <h3>{p.name}</h3>
          <p>Категория: {p.category?.name}</p>
          <p>Бренд: {p.brand?.name}</p>
        </div>
      ))}
    </div>
  );
}
