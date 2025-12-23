import { Link } from "react-router-dom";

export default function Header() {
    return (
        <nav className="header">
            <h1>Магазин одежды</h1>
            <div>
                <Link to="/">Товары</Link>
                <Link to="/customers">Клиенты</Link>
                <Link to="/orders">Заказы</Link>
            </div>
        </nav>
    );
}
