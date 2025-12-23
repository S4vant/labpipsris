import { Routes, Route, Navigate } from "react-router-dom";
import AdminLayout from "./AdminLayout";
import Products from "@/pages/Products";
import Orders from "@/pages/Orders";
import EmployeesAdmin from "@/pages/EmployeesAdmin";
import Customers from "@/pages/Customers";

export default function AdminApp() {
  return (
    <Routes>
      <Route element={<AdminLayout />}>
        <Route index element={<Navigate to="products" />} />
        <Route path="products" element={<Products />} />
        <Route path="orders" element={<Orders />} />
        <Route path="customers" element={<Customers />} />
        <Route path="employees" element={<EmployeesAdmin />} />
      </Route>
    </Routes>
  );
}
