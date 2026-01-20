import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import StaffPage from "./pages/StaffPage";
import Login from "./pages/Login";
import UserHome from "./pages/UserHome";
import StaffProductsPage from "./pages/staff/ProductsPage";
import CategoriesPage from "./pages/staff/CategoryPage";
import BrandsPage from "./pages/staff/BrandsPage";
import StaffLayout from "./components/StaffLayout";

import { ProductFilterProvider } from "./context/ProductFilterContext";
export default function App() {
    const userRole = localStorage.getItem("role"); // например, получаем роль из localStorage
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/user" element={<UserHome />} />
              <Route path="/staff"
                    element={
                        <ProductFilterProvider>
                        <StaffLayout />
                        </ProductFilterProvider>
                    }>
  <Route path="products" element={<StaffProductsPage />} />
  <Route path="categories" element={<CategoriesPage />} />
  <Route path="brands" element={<BrandsPage />} />
</Route>
      </Routes>
    </BrowserRouter>
  );
}
