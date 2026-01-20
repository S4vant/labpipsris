import { useState, useEffect } from "react";
import axios from "../api/axios-instance";

export default function OrderForm() {
  const [products, setProducts] = useState([]);
  const [customerId, setCustomerId] = useState("");
  const [items, setItems] = useState([]);

  useEffect(() => {
    axios.get("/products").then(res => setProducts(res.data));
  }, []);

  const addItem = (productId) => {
    setItems([...items, { product_id: productId, quantity: 1 }]);
  };

  const handleSubmit = () => {
    axios.post("/orders", { customer_id: customerId, items })
      .then(() => alert("Заказ создан"))
      .catch(err => alert(err.response?.data?.error || "Ошибка создания заказа"));
  };

  return (
    <div>
      <h2>Оформление заказа</h2>
      <input
        placeholder="ID клиента"
        value={customerId}
        onChange={e => setCustomerId(e.target.value)}
      />
      <div>
        {products.map(p => (
          <button key={p.id} onClick={() => addItem(p.id)} style={{ margin: "5px" }}>
            {p.name}
          </button>
        ))}
      </div>
      <button onClick={handleSubmit} style={{ marginTop: "10px" }}>Создать заказ</button>
    </div>
  );
}
