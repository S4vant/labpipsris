import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import StaffLogin from "./pages/StaffLogin";
import AdminApp from "../admin/AdminApp";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/staff/login" element={<StaffLogin />} />
      <Route path="/staff/*" element={<AdminApp />} />
      
    </Routes>
  );
}
