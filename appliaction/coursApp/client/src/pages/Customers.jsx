import { useEffect, useState } from "react";
import { getCustomers } from "../api/customer";

export default function Customers() {
    const [customers, setCustomers] = useState([]);

    useEffect(() => {
        getCustomers().then(setCustomers);
    }, []);

    return (
        <>
            <h1 className="page-title">Клиенты</h1>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Имя</th>
                        <th>Email</th>
                        <th>Телефон</th>
                    </tr>
                </thead>
                <tbody>
                    {customers.map(c => (
                        <tr key={c.id}>
                            <td>{c.id}</td>
                            <td>{c.first_name} {c.last_name}</td>
                            <td>{c.email}</td>
                            <td>{c.phone}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    );
}
