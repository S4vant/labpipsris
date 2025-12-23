import { useEffect, useState } from "react";
import { getOrders } from "../api/orders";

export default function Orders() {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        getOrders().then(setOrders);
    }, []);

    return (
        <>
            <h1 className="page-title">Заказы</h1>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Клиент</th>
                        <th>Сотрудник</th>
                        <th>Статус</th>
                    </tr>
                </thead>
                <tbody>
                    {orders.map(o => (
                        <tr key={o.id}>
                            <td>{o.id}</td>
                            <td>{o.customer_id}</td>
                            <td>{o.employee_id ?? "-"}</td>
                            <td>{o.status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    );
}
