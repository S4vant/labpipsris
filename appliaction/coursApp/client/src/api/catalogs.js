import { request } from "./http";

export const getCategories = () => request("/categories");
export const getSuppliers = () => request("/suppliers");
