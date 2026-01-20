import { useEffect, useState } from "react";
import axios from "../api/axios-instance";

export default function ProductList() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    axios.get("/products")
      .then(res => setProducts(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2>Продукты</h2>
      <ul>
        {products.map(p => (
          <li key={p.id}>
            {p.name} — {p.price}₽ — Остаток: {p.quantity}
          </li>
        ))}
      </ul>
    </div>
  );
}
