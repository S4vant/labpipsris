from flask import Blueprint, jsonify, request, session
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app import db
from app.models import Product, Customer, Order, Employee,Category, Supplier, Brand, SupplyItem, OrderItem, Supply

from app.config import ADMIN_MASTER_KEY
from ..decorators import staff_required


main = Blueprint("api", __name__)

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
    """
    Получить список товаров
    ---
    tags:
      - Products
    responses:
      200:
        description: Список товаров
        content:
          application/json:
            example:
              - id: 1
                name: iPhone
                price: 99990
                quantity: 10
                category_id: 1
                brand_id: 2
                supplier_id: 3
      500:
        description: Ошибка сервера"""
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
    """
    Добавить новый товар
    ---
    tags:
      - Products
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - price
              - quantity
              - category_id
              - brand_id
              - supplier_id
            properties:
              name:
                type: string
              price:
                type: number
              quantity:
                type: integer
              category_id:
                type: integer
              brand_id:
                type: integer
              supplier_id:
                type: integer
    responses:
      201:
        description: Товар добавлен
      400:
        description: Некорректные данные
      500:
        description: Ошибка сервера
    """
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
    """
    Обновить товар
    ---
    tags:
      - Products
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              price:
                type: number
              quantity:
                type: integer
              category_id:
                type: integer
              brand_id:
                type: integer
              supplier_id:
                type: integer
    responses:
      200:
        description: Товар обновлён
      404:
        description: Товар не найден
    """
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
    """
    Удалить товар
    ---
    tags:
      - Products
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Товар удалён
      404:
        description: Товар не найден
    """
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
    """
    Получить список клиентов
    ---
    tags:
      - Customers
    responses:
      200:
        description: Список клиентов
    """
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
    """
    Добавить клиента
    ---
    tags:
      - Customers
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [first_name, last_name, email, phone]
            properties:
              first_name: {type: string}
              last_name: {type: string}
              email: {type: string}
              phone: {type: string}
    responses:
      201:
        description: Клиент добавлен
    """
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
    """
    Создать заказ
    ---
    tags:
      - Orders
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [customer_id, items]
            properties:
              customer_id:
                type: integer
              employee_id:
                type: integer
                nullable: true
              items:
                type: array
                items:
                  type: object
                  properties:
                    product_id:
                      type: integer
                    quantity:
                      type: integer
    responses:
      201:
        description: Заказ создан
      400:
        description: Ошибка данных
    """
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
    """
    Добавить поставку
    ---
    tags:
      - Supplies
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [supplier_id, items]
            properties:
              supplier_id:
                type: integer
              items:
                type: array
                items:
                  type: object
                  properties:
                    product_id:
                      type: integer
                    quantity:
                      type: integer
    responses:
      201:
        description: Поставка добавлена
    """
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

# ===== CATEGORIES =====
@main.route("/categories", methods=["GET"])

def get_categories():
    """
    Получить список категорий
    ---
    tags:
      - Categories
    responses:
      200:
        description: Список категорий
        content:
          application/json:
            example:
              - id: 1
                name: Смартфоны
    """
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])

@main.route("/categories", methods=["POST"])
@staff_required(role=["staff", "admin"])
def add_category():
    """
    Добавить категорию
    ---
    tags:
      - Categories
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [name]
            properties:
              name:
                type: string
    responses:
      201:
        description: Категория добавлена
    """
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
    """
    Добавить категорию
    ---
    tags:
      - Categories
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [name]
            properties:
              name:
                type: string
                example: Аксессуары
    responses:
      201:
        description: Категория добавлена
      400:
        description: Некорректные данные
    """
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
    """
    Обновить категорию
    ---
    tags:
      - Categories
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
    responses:
      200:
        description: Категория обновлена
      404:
        description: Категория не найдена
    """
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Категория не найдена"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Категория удалена"}), 200

# ===== BRANDS =====
@main.route("/brands", methods=["GET"])
def get_brands():
    """
    Получить список брендов
    ---
    tags:
      - Brands
    responses:
      200:
        description: Список брендов
    """
    brands = Brand.query.all()
    return jsonify([{"id": b.id, "name": b.name} for b in brands])

@main.route("/brands", methods=["POST"])
@staff_required(role=["staff", "admin"])
def add_brand():
    """
    Добавить бренд
    ---
    tags:
      - Brands
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [name]
            properties:
              name:
                type: string
    responses:
      201:
        description: Бренд добавлен
    """
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
    """
    Обновить бренд
    ---
    tags:
      - Brands
    parameters:
      - in: path
        name: id
        schema:
          type: integer
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
    responses:
      200:
        description: Бренд обновлён
      404:
        description: Бренд не найден
    """
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
    """
    Удалить бренд
    ---
    tags:
      - Brands
    parameters:
      - in: path
        name: id
        schema:
          type: integer
    responses:
      200:
        description: Бренд удалён
      404:
        description: Бренд не найден
    """
    brand = Brand.query.get(id)
    if not brand:
        return jsonify({"error": "Бренд не найден"}), 404
    db.session.delete(brand)
    db.session.commit()
    return jsonify({"message": "Бренд удален"}), 200

# ===== SUPPLIERS =====
@main.route("/suppliers", methods=["GET"])
def get_suppliers():
    """
    Получить список поставщиков
    ---
    tags:
      - Suppliers
    responses:
      200:
        description: Список поставщиков
    """
    suppliers = Supplier.query.all()
    return jsonify([{"id": s.id, "name": s.name} for s in suppliers])

@main.route("/suppliers", methods=["POST"])
@staff_required(role=["staff", "admin"])
def add_supplier():
    """
    Добавить поставщика
    ---
    tags:
      - Suppliers
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [name]
            properties:
              name:
                type: string
    responses:
      201:
        description: Поставщик добавлен
    """
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
    """
    Обновить поставщика
    ---
    tags:
      - Suppliers
    parameters:
      - in: path
        name: id
        schema:
          type: integer
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
    responses:
      200:
        description: Поставщик обновлён
      404:
        description: Поставщик не найден
    """
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
    """
    Удалить поставщика
    ---
    tags:
      - Suppliers
    parameters:
      - in: path
        name: id
        schema:
          type: integer
    responses:
      200:
        description: Поставщик удалён
      404:
        description: Поставщик не найден
    """
    
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({"error": "Поставщик не найден"}), 404
    db.session.delete(supplier)
    db.session.commit()
    return jsonify({"message": "Поставщик удален"}), 200

# ===== SUPPLIES =====
@main.route("/supplies", methods=["GET"])
def get_supplies():
    """
    Получить поставки
    ---
    tags:
      - Supplies
    responses:
      200:
        description: Список поставок
    """
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
    """
    Оформить поставку
    --- 
    tags:
      - Supplies
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [supplier_id, items]
            properties:
              supplier_id:
                type: integer
              items:
                type: array
                items:
                  type: object
                  required: [product_id, quantity]
                  properties:
                    product_id:
                      type: integer
                    quantity:
                      type: integer
    responses:
      201:
        description: Поставка добавлена
      400:
        description: Отсутствуют обязательные поля
    """
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
