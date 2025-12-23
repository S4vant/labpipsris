import { useEffect, useState } from "react";
import { getCategories, getSuppliers } from "../api/catalogs";

export default function ProductForm({ onSubmit, initialData = {} }) {
    const [name, setName] = useState(initialData.name || "");
    const [price, setPrice] = useState(initialData.price || "");
    const [quantity, setQuantity] = useState(initialData.quantity || "");
    const [categoryId, setCategoryId] = useState(initialData.category_id || "");
    const [supplierId, setSupplierId] = useState(initialData.supplier_id || "");

    const [categories, setCategories] = useState([]);
    const [suppliers, setSuppliers] = useState([]);

    useEffect(() => {
        getCategories().then(setCategories);
        getSuppliers().then(setSuppliers);
    }, []);

    function handleSubmit(e) {
        e.preventDefault();

        onSubmit({
            name,
            price: Number(price),
            quantity: Number(quantity),
            category_id: Number(categoryId),
            supplier_id: Number(supplierId)
        });
        if (!name || !price || !quantity || !categoryId || !supplierId)
            alert(error(error));
    }

    return (
        <form className="card" onSubmit={handleSubmit}>
            <div className="form-group">
                <label>Название</label>
                <input
                    value={name}
                    onChange={e => setName(e.target.value)}
                    required
                />
            </div>

            <div className="form-group">
                <label>Цена</label>
                <input
                    type="number"
                    value={price}
                    onChange={e => setPrice(e.target.value)}
                    required
                />
            </div>

            <div className="form-group">
                <label>Количество</label>
                <input
                    type="number"
                    value={quantity}
                    onChange={e => setQuantity(e.target.value)}
                    required
                />
            </div>
            
            <div className="form-group">
                <label>Категория</label>
                <select
                    value={categoryId}
                    onChange={e => setCategoryId(e.target.value)}
                    disabled={categories.length === 0}
                    required
                >
                    {categories.length === 0 ? (
                        <option>Нет доступных категорий</option>
                    ) : (
                        <>
                            <option value="">Выберите категорию</option>
                            {categories.map(c => (
                                <option key={c.id} value={c.id}>
                                    {c.name}
                                </option>
                            ))}
                        </>
                    )}
                </select>
            </div>

            <div className="form-group">
                <label>Поставщик</label>
                <select
                    value={supplierId}
                    onChange={e => setSupplierId(e.target.value)}
                    disabled={suppliers.length === 0}
                    required
                >
                    {suppliers.length === 0 ? (
                        <option>Нет доступных поставщиков</option>
                    ) : (
                        <>
                            <option value="">Выберите поставщика</option>
                            {suppliers.map(s => (
                                <option key={s.id} value={s.id}>
                                    {s.name}
                                </option>
                            ))}
                        </>
                    )}
                </select>
            </div>

            <button className="btn-primary">
                Сохранить
            </button>
        </form>
    );
}
