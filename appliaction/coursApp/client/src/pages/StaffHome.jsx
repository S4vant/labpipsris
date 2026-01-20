import ProductList from "../components/ProductList";
import OrderForm from "../components/OrderForm";
import { useEffect, useState } from "react";
import axios from "../api/axios-instance";

export default function StaffHome() {
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);
  const [suppliers, setSuppliers] = useState([]);

  useEffect(() => {
    axios.get("/categories").then(res => setCategories(res.data));
    axios.get("/brands").then(res => setBrands(res.data));
    axios.get("/suppliers").then(res => setSuppliers(res.data));
  }, []);

  return (
    <div>
      <h1>Панель сотрудника</h1>
      <ProductList />
      <OrderForm />
      {/* CRUD для категорий, брендов, поставщиков — можно добавлять компоненты по аналогии */}
    </div>
  )
}
