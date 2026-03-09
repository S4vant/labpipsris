import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios-instance";
import UserProductsPage from "./user/ProductPage";
import { useProductFilters } from "../context/ProductFilterContext";
export default function HomePage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState("");
    const [categories, setCategories] = useState([]);
    const [brands, setBrands] = useState([]);
    const [products, setProducts] = useState([]);
    const { filters } = useProductFilters();
 
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

  return (
    <div style={{
      display: "grid",

      gap: "20px"
    }}>
      
      <UserProductsPage />
    </div>
    
  );
}