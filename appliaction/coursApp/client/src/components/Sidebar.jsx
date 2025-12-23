import { NavLink } from "react-router-dom";
import "./Sidebar.css";
export default function Sidebar({ user }) {
  console.log("Успешно:", user);
  const isStaff = user?.role === "staff" || user?.role === "admin";

  return (
    <aside className="sidebar">
      <NavLink to="/products" className="nav-link">
        Ассортимент
      </NavLink>

      {isStaff && (
        <>
          <NavLink to="/staff/products" className="nav-link">Товары</NavLink>
          <NavLink to="/staff/orders" className="nav-link">Заказы</NavLink>
          <NavLink to="/staff/customers" className="nav-link">Клиенты</NavLink>
          <NavLink to="/staff/employees" className="nav-link">Сотрудники</NavLink>
          <NavLink to="/staff/suppliers" className="nav-link">Поставщики</NavLink>
          <NavLink to="/staff/brands" className="nav-link">Бренды</NavLink>
          <NavLink to="/staff/categories" className="nav-link">Категории</NavLink>
          <NavLink to="/staff/supplies" className="nav-link">Поставки</NavLink>
        </>
      )}
    </aside>
  );
}
