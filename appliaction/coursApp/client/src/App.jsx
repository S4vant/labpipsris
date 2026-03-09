import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import StaffPage from "./pages/StaffPage";

import StaffProductsPage from "./pages/staff/ProductsPage";
import CategoriesPage from "./pages/staff/CategoryPage";
import BrandsPage from "./pages/staff/BrandsPage";
import StaffLayout from "./components/StaffLayout";
import UserLayout from "./components/UserLayout";

import { ProductFilterProvider } from "./context/ProductFilterContext";
import UserProductsPage from "./pages/user/ProductPage";
export default function App() {
    const userRole = localStorage.getItem("role"); // например, получаем роль из localStorage
  return (
    <BrowserRouter>
  <ProductFilterProvider>
    <Routes>
      <Route path="/" element={<UserLayout />} >
        <Route index element={<HomePage />} />
      </Route>
      <Route path="/staff" element={<StaffLayout />}>
        <Route index element={<StaffPage />} />
        <Route path="products" element={<StaffProductsPage />} />
        <Route path="categories" element={<CategoriesPage />} />
        <Route path="brands" element={<BrandsPage />} />
      </Route>
    </Routes>
  </ProductFilterProvider>
</BrowserRouter>
  );
}
