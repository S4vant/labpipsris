import { request } from "./http";

export const getProducts = () => request("/products");

export const addProduct = (data) =>
    request("/products", {
        method: "POST",
        body: JSON.stringify(data)
    });

export const updateProduct = (id, data) =>
    request(`/products/${id}`, {
        method: "PUT",
        body: JSON.stringify(data)
    });

export const deleteProduct = (id) =>
    request(`/products/${id}`, {
        method: "DELETE"
    });

    export const createProduct = (product) =>
    request("/products", {
        method: "POST",
        body: JSON.stringify(product)
    });
