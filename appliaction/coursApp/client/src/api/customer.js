import { request } from "./http";

export const getCustomers = () => request("/customers");

export const addCustomer = (customer) =>
    request("/customers", {
        method: "POST",
        body: JSON.stringify(customer)
    });

export const deleteCustomer = (id) =>
    request(`/customers/${id}`, {
        method: "DELETE"
    });