import { request } from "./http";

export const getOrders = () => request("/orders");

export const addOrder = (order) =>
    request("/orders", {
        method: "POST",
        body: JSON.stringify(order)
    });

export const deleteOrder = (id) =>
    request(`/orders/${id}`, {
        method: "DELETE"
    });