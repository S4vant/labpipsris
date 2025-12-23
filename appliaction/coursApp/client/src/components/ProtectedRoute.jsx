// components/ProtectedRoute.jsx
import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";

export default function ProtectedRoute({ children }) {
  const { user, loading } = useContext(UserContext);

  if (loading) return null;
  if (!user) return <Navigate to="/login" />;

  return children;
}
