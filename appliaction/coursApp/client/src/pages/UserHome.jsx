import ProductList from "../components/ProductList";
import OrderForm from "../components/OrderForm";

export default function UserHome() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Главная страница пользователя</h1>
      <ProductList />
      <hr />
      <OrderForm />
    </div>
  );
}
