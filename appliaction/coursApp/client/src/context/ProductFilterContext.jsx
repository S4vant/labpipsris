import { createContext, useContext, useState } from "react";

// Контекст фильтров
const ProductFilterContext = createContext(null);

export function ProductFilterProvider({ children }) {
  // Добавляем фильтры по category_id и brand_id
const [filters, setFilters] = useState({
  name: "",
  brand_id: null,
  category_id: null,
});

  return (
    <ProductFilterContext.Provider value={{ filters, setFilters }}>
      {children}
    </ProductFilterContext.Provider>
  );
}

// Хук для использования фильтров в компонентах
export function useProductFilters() {
  return useContext(ProductFilterContext);
}
