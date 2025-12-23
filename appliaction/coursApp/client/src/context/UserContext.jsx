// src/context/UserContext.jsx
import { createContext, useState, useEffect } from "react";

export const UserContext = createContext(null);

export function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  function saveUser(user) {
    setUser(user);
  }

  function logout() {
    fetch("http://localhost:5000/api/auth/logout", {
      method: "POST",
      credentials: "include"
    });
    setUser(null);
  }

  useEffect(() => {
    fetch("http://localhost:5000/api/auth/me", {
      credentials: "include"
    })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data?.employee) setUser(data.employee);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <UserContext.Provider value={{ user, saveUser, logout, loading }}>
      {children}
    </UserContext.Provider>
  );
}
