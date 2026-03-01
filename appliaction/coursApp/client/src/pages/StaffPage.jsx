import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios-instance";


export default function StaffPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState("");
  useEffect(() => {
    const checkSession = async () => {
      const token = localStorage.getItem("token");
      if (!token) return;

      try {
        const res = await axios.get("/auth/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const role = res.data.employee?.role;
        if (role) setUserRole(role), setIsLoggedIn(true);
      } catch {
        localStorage.removeItem("token");
      }
    };
    checkSession();
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
          minHeight: "200px"
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