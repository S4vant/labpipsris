from flask import Blueprint, jsonify, request, session
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app import db
from app.models import Product, Customer, Order, Employee,Category, Supplier, Brand, SupplyItem, OrderItem, Supply

from app.config import ADMIN_MASTER_KEY
from ..decorators import staff_required


main = Blueprint("api", __name__, url_prefix="/api")

# ---------------------------
# Error handlers
# ---------------------------
@main.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ресурс не найден"}), 404

@main.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Внутренняя ошибка сервера"}), 500

# ---------------------------
# Функция commit_or_rollback
# ---------------------------
def commit_or_rollback():
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка целостности данных", "details": str(e.orig)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500

# ---------------------------
# Продукты
# ---------------------------
@main.route("/products", methods=['GET', 'OPTIONS'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "quantity": p.quantity,
                "category_id": p.category_id,
                "brand_id": getattr(p, 'brand_id', None),
                "supplier_id": p.supplier_id,
            } for p in products
        ])
    except SQLAlchemyError as e:
        return jsonify({"error": "Ошибка при получении товаров", "details": str(e)}), 500

@main.route("/products", methods=["POST"])
@staff_required(role=["admin", "staff"])
def add_product():
    data = request.get_json()
    required_fields = ["name", "price", "quantity", "category_id", "brand_id", "supplier_id"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Отсутствует обязательное поле: {field}"}), 400

    try:
        new_product = Product(**{k: data[k] for k in required_fields})
        db.session.add(new_product)
        resp = commit_or_rollback()
        if resp:
            return resp
        return jsonify({"message": "Товар успешно добавлен"}), 201
    except Exception as e:
        return jsonify({"error": "Ошибка при добавлении товара", "details": str(e)}), 500

@main.route("/products/<int:id>", methods=["PUT"])
@staff_required(role=["admin", "staff"])
def update_product(id):
    data = request.get_json()
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Товар не найден"}), 404

    for field in ["name", "price", "quantity", "category_id", "brand_id", "supplier_id"]:
        if field in data:
            setattr(product, field, data[field])

    resp = commit_or_rollback()
    if resp:
        return resp
    return jsonify({"message": "Товар обновлён успешно"}), 200

@main.route("/products/<int:id>", methods=["DELETE"])
@staff_required(role=["admin", "staff"])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Товар не найден"}), 404

    db.session.delete(product)
    resp = commit_or_rollback()
    if resp:
        return resp
    return jsonify({"message": "Товар удалён"}), 200

# ---------------------------
# Клиенты
# ---------------------------
@main.route("/customers", methods=["GET"])
def get_customers():
    try:
        customers = Customer.query.all()
        return jsonify([{
            "id": c.id,
            "first_name": getattr(c, "first_name", ""),
            "last_name": getattr(c, "last_name", ""),
            "email": getattr(c, "email", ""),
            "phone": getattr(c, "phone", "")
        } for c in customers])
    except SQLAlchemyError as e:
        return jsonify({"error": "Ошибка при получении клиентов", "details": str(e)}), 500

@main.route("/customers", methods=["POST"])
@staff_required(role=["admin", "staff"])
def add_customer():
    data = request.get_json()
    required_fields = ["first_name", "last_name", "email", "phone"]
    for f in required_fields:
        if f not in data:
            return jsonify({"error": f"Отсутствует обязательное поле: {f}"}), 400

    try:
        new_customer = Customer(**{k: data[k] for k in required_fields})
        db.session.add(new_customer)
        resp = commit_or_rollback()
        if resp:
            return resp
        return jsonify({"message": "Клиент добавлен успешно"}), 201
    except Exception as e:
        return jsonify({"error": "Ошибка при добавлении клиента", "details": str(e)}), 500

# ---------------------------
# Заказы
# ---------------------------
@main.route("/orders", methods=["GET"])

def get_orders():
    try:
        orders = Order.query.all()
        return jsonify([{
            "id": o.id,
            "customer_id": o.customer_id,
            "employee_id": o.employee_id,
            "date": getattr(o, "order_date", ""),
            "status": o.status
        } for o in orders])
    except SQLAlchemyError as e:
        return jsonify({"error": "Ошибка при получении заказов", "details": str(e)}), 500

@main.route("/orders", methods=["POST"])
def add_order():
    data = request.get_json()
    
    # Проверяем обязательные поля
    if not all(k in data for k in ["customer_id", "items"]):
        return jsonify({"error": "Отсутствуют обязательные поля: customer_id, items"}), 400

    try:
        # Для обычного пользователя роль сотрудника не требуется
        employee_id = data.get("employee_id")  # может быть None
        order = Order(customer_id=data["customer_id"], employee_id=employee_id, status=data.get("status", "new"))
        db.session.add(order)
        db.session.flush()  # для получения order.id

        for item in data["items"]:
            product = Product.query.get(item["product_id"])
            if not product:
                db.session.rollback()
                return jsonify({"error": f"Товар с id={item['product_id']} не найден"}), 404

            if product.quantity < item["quantity"]:
                db.session.rollback()
                return jsonify({"error": f"Недостаточно товара на складе для {product.name}"}), 400

            # Уменьшаем количество товара
            product.quantity -= item["quantity"]

            db.session.add(OrderItem(
                order_id=order.id,
                product_id=item["product_id"],
                quantity=item["quantity"]
            ))

        db.session.commit()
        return jsonify({"message": "Заказ успешно создан, остатки обновлены"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка при создании заказа", "details": str(e)}), 500

# ---------------------------
# Справочники
# ---------------------------
# @main.route("/categories", methods=["GET"])
# def get_categories():
#     categories = Category.query.all()
#     return jsonify([{"id": c.id, "name": c.name} for c in categories])

# @main.route("/suppliers", methods=["GET"])
# def get_suppliers():
#     suppliers = Supplier.query.all()
#     return jsonify([{"id": s.id, "name": s.name} for s in suppliers])

# ---------------------------
# Staff
# ---------------------------
@main.route("/staff/login", methods=["POST"])
def staff_login():
    data = request.json
    employee = Employee.query.filter_by(username=data["username"]).first()
    if not employee or not employee.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    session["employee_id"] = employee.id
    session["role"] = employee.role
    return jsonify({"message": "ok"})

@main.route("/staff/logout", methods=["POST"])
def staff_logout():
    session.clear()
    return jsonify({"message": "logged out"})

@main.route("/staff/create", methods=["POST"])
@staff_required(role="admin")
def create_employee():
    data = request.json
    if data.get("master_key") != ADMIN_MASTER_KEY:
        return jsonify({"error": "Invalid master key"}), 403
    if Employee.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User already exists"}), 400
    employee = Employee(
        username=data["username"],
        role=data.get("role", "staff")
    )
    employee.set_password(data["password"])
    db.session.add(employee)
    db.session.commit()
    return jsonify({"message": "Employee created"})

@main.route("/staff/me", methods=["GET"])
def staff_me():
    employee = Employee.query.get(session["employee_id"])
    return jsonify({
        "id": employee.id,
        "username": employee.username,
        "role": employee.role
    })

# ===== CATEGORIES =====
@main.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])

@main.route("/categories", methods=["POST"])
@staff_required(role=["staff", "admin"])
def add_category():
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Отсутствует имя категории"}), 400
    category = Category(name=data["name"])
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": "Категория добавлена"}), 201

@main.route("/categories/<int:id>", methods=["PUT"])
@staff_required(role=["staff", "admin"])
def update_category(id):
    data = request.get_json()
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Категория не найдена"}), 404
    if "name" in data:
        category.name = data["name"]
    db.session.commit()
    return jsonify({"message": "Категория обновлена"}), 200

@main.route("/categories/<int:id>", methods=["DELETE"])
@staff_required(role=["staff", "admin"])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Категория не найдена"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Категория удалена"}), 200

# ===== BRANDS =====
@main.route("/brands", methods=["GET"])
def get_brands():
    brands = Brand.query.all()
    return jsonify([{"id": b.id, "name": b.name} for b in brands])

@main.route("/brands", methods=["POST"])
@staff_required(role=["staff", "admin"])
def add_brand():
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Отсутствует имя бренда"}), 400
    brand = Brand(name=data["name"])
    db.session.add(brand)
    db.session.commit()
    return jsonify({"message": "Бренд добавлен"}), 201

@main.route("/brands/<int:id>", methods=["PUT"])
@staff_required(role=["staff", "admin"])
def update_brand(id):
    data = request.get_json()
    brand = Brand.query.get(id)
    if not brand:
        return jsonify({"error": "Бренд не найден"}), 404
    if "name" in data:
        brand.name = data["name"]
    db.session.commit()
    return jsonify({"message": "Бренд обновлен"}), 200

@main.route("/brands/<int:id>", methods=["DELETE"])
@staff_required(role=["staff", "admin"])
def delete_brand(id):
    brand = Brand.query.get(id)
    if not brand:
        return jsonify({"error": "Бренд не найден"}), 404
    db.session.delete(brand)
    db.session.commit()
    return jsonify({"message": "Бренд удален"}), 200

# ===== SUPPLIERS =====
@main.route("/suppliers", methods=["GET"])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([{"id": s.id, "name": s.name} for s in suppliers])

@main.route("/suppliers", methods=["POST"])
@staff_required(role=["staff", "admin"])
def add_supplier():
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Отсутствует имя поставщика"}), 400
    supplier = Supplier(name=data["name"])
    db.session.add(supplier)
    db.session.commit()
    return jsonify({"message": "Поставщик добавлен"}), 201

@main.route("/suppliers/<int:id>", methods=["PUT"])
@staff_required(role=["staff", "admin"])
def update_supplier(id):
    data = request.get_json()
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({"error": "Поставщик не найден"}), 404
    if "name" in data:
        supplier.name = data["name"]
    db.session.commit()
    return jsonify({"message": "Поставщик обновлен"}), 200

@main.route("/suppliers/<int:id>", methods=["DELETE"])
@staff_required(role=["staff", "admin"])
def delete_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({"error": "Поставщик не найден"}), 404
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({"message": "Поставщик удален"}), 200

# ===== SUPPLIES =====
@main.route("/supplies", methods=["GET"])
def get_supplies():
    supplies = Supply.query.all()
    result = []
    for s in supplies:
        result.append({
            "id": s.id,
            "supplier_id": s.supplier_id,
            "date": s.date.isoformat(),
            "items": [{"product_id": i.product_id, "quantity": i.quantity} for i in s.items]
        })
    return jsonify(result)

# @main.route("/", methods=["options"])
# @staff_required(role=["staff", "admin"])

@main.route("/supplies", methods=["POST"])
@staff_required(role=["staff", "admin"])
def add_supply():
    data = request.get_json()
    if not all(k in data for k in ["supplier_id", "items"]):
        return jsonify({"error": "Отсутствуют обязательные поля"}), 400

    try:
        supply = Supply(supplier_id=data["supplier_id"])
        db.session.add(supply)
        db.session.flush()  # чтобы получить id для SupplyItem

        for item in data["items"]:
            product = Product.query.get(item["product_id"])
            if not product:
                db.session.rollback()
                return jsonify({"error": f"Товар с id={item['product_id']} не найден"}), 404

            # Увеличиваем количество товара
            product.quantity += item["quantity"]

            db.session.add(SupplyItem(
                supply_id=supply.id,
                product_id=item["product_id"],
                quantity=item["quantity"]
            ))

        db.session.commit()
        return jsonify({"message": "Поставка успешно добавлена, остатки обновлены"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка при добавлении поставки", "details": str(e)}), 500
