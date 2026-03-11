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
            "price": float(p.price),
            "category": {
                "id": p.category.id,
                "name": p.category.name
            } if p.category else None,
            "brand": {
                "id": p.brand.id,
                "name": p.brand.name
            } if p.brand else None
        }
        for p in products
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
    security:
      - BearerAuth: []
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
    responses:
      201:
        description: Товар добавлен
      400:
        description: Некорректные данные
      500:
        description: Ошибка сервера
    """
    data = request.get_json() or {}

    required_fields = [
        "name",
        "price",
        "category_id",
        "brand_id",
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Отсутствует обязательное поле: {field}"}), 400

    try:
        new_product = Product(
            name=data["name"],
            price=data["price"],
            category_id=data["category_id"],
            brand_id=data["brand_id"],
            size=data["size" if "size" in data else None],
            color=data["color" if "color" in data else None],
            description=data["description" if "description" in data else None],
        )

        db.session.add(new_product)
        resp = commit_or_rollback()
        if resp:
            return resp

        return jsonify({"message": "Товар успешно добавлен"}), 201

    except Exception as e:
        return jsonify({
            "error": "Ошибка при добавлении товара",
            "details": str(e)
        }), 500
@main.route("/products/<int:id>", methods=["PUT"])
@staff_required(role=["admin", "staff"])
def update_product(id):
    """
    Обновить товар
    ---
    tags:
      - Products
    security:
      - BearerAuth: []
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
    responses:
      200:
        description: Товар обновлён
      404:
        description: Товар не найден
    """
    data = request.get_json() or {}

    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Товар не найден"}), 404

    updatable_fields = [
        "name",
        "price",
        "quantity",
        "category_id",
        "brand_id",
    ]

    for field in updatable_fields:
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
    security:
      - BearerAuth: []
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
        new_customer = Customer(**{k: data[k] for k in required_fields}, address=data.get("address"))
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
@main.route("/orders", methods=["POST"])
def create_order():
    """
    Создать корзину (заказ со статусом pending)
    ---
    tags:
      - Orders
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - customer_id
            properties:
              customer_id:
                type: integer
                example: 1
              employee_id:
                type: integer
                example: 2
    responses:
      201:
        description: Корзина успешно создана
      400:
        description: Некорректные данные
    """
    data = request.get_json()

    if "customer_id" not in data:
        return jsonify({"error": "customer_id обязателен"}), 400

    try:
        order = Order(
            customer_id=data["customer_id"],
            employee_id=data.get("employee_id"),
            status="pending"
        )

        db.session.add(order)
        db.session.commit()

        return jsonify({
            "message": "Корзина создана",
            "order_id": order.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@main.route("/orders/<int:order_id>/items", methods=["POST"])
def add_item_to_order(order_id):
    """
    Добавить товар в корзину
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        required: true
        schema:
          type: integer
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - product_id
              - quantity
            properties:
              product_id:
                type: integer
                example: 5
              quantity:
                type: integer
                example: 2
    responses:
      201:
        description: Товар добавлен в корзину
      400:
        description: Ошибка данных или заказ уже оформлен
      404:
        description: Заказ или товар не найден
    """
    data = request.get_json()

    if not all(k in data for k in ["product_id", "quantity"]):
        return jsonify({"error": "product_id и quantity обязательны"}), 400

    order = Order.query.get_or_404(order_id)

    if order.status != "pending":
        return jsonify({"error": "Нельзя изменять оформленный заказ"}), 400

    product = Product.query.get_or_404(data["product_id"])

    item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=data["quantity"],
        price=product.price
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Товар добавлен в корзину"}), 201

@main.route("/orders/items/<int:item_id>", methods=["DELETE"])
def delete_order_item(item_id):
    """
    Удалить товар из корзины
    ---
    tags:
      - Orders
    parameters:
      - name: item_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Товар удалён из корзины
      400:
        description: Заказ уже оформлен
      404:
        description: Элемент заказа не найден
    """

    item = OrderItem.query.get_or_404(item_id)

    if item.order.status != "pending":
        return jsonify({"error": "Нельзя изменять оформленный заказ"}), 400

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Товар удалён из корзины"})

@main.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """
    Получить информацию о заказе (корзине)
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Информация о заказе
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                status:
                  type: string
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      product_id:
                        type: integer
                      product_name:
                        type: string
                      quantity:
                        type: integer
                      price:
                        type: number
      404:
        description: Заказ не найден
    """

    order = Order.query.get_or_404(order_id)

    items = []

    for item in order.items:
        items.append({
            "product_id": item.product_id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price": float(item.price)
        })

    return jsonify({
        "id": order.id,
        "status": order.status,
        "items": items
    })

@main.route("/orders/<int:order_id>/checkout", methods=["POST"])
def checkout_order(order_id):
    """
    Оформить заказ (checkout корзины)
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Заказ успешно оформлен
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                total_amount:
                  type: number
      400:
        description: Недостаточно товара или заказ уже оформлен
      404:
        description: Заказ не найден
    """
    order = Order.query.get_or_404(order_id)

    if order.status != "pending":
        return jsonify({"error": "Заказ уже оформлен"}), 400

    total = 0

    try:

        for item in order.items:

            product = item.product

            if product.stock_quantity < item.quantity:
                return jsonify({
                    "error": f"Недостаточно товара {product.name}"
                }), 400

            product.stock_quantity -= item.quantity
            total += item.price * item.quantity

        order.total_amount = total
        order.status = "paid"

        db.session.commit()

        return jsonify({
            "message": "Заказ оформлен",
            "total_amount": float(total)
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@main.route("/orders/quick", methods=["POST"])
def quick_order():
    """
    Быстрое оформление заказа (без создания корзины)
    ---
    tags:
      - Orders
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - customer_id
              - items
            properties:
              customer_id:
                type: integer
                example: 1
              items:
                type: array
                items:
                  type: object
                  properties:
                    product_id:
                      type: integer
                      example: 3
                    quantity:
                      type: integer
                      example: 2
    responses:
      200:
        description: Заказ успешно оформлен
      400:
        description: Ошибка данных
      404:
        description: Товар не найден
    """

    data = request.get_json()

    if not all(k in data for k in ["customer_id", "items"]):
        return jsonify({"error": "customer_id и items обязательны"}), 400

    try:

        order = Order(
            customer_id=data["customer_id"],
            status="pending"
        )

        db.session.add(order)
        db.session.flush()

        for item in data["items"]:

            product = Product.query.get_or_404(item["product_id"])

            db.session.add(OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item["quantity"],
                price=product.price
            ))

        db.session.commit()

        return checkout_order(order.id)

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
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
@staff_required(role=["admin", "staff"])
def add_category():
    """
    Добавить категорию товара
    ---
    tags:
      - Categories
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
            properties:
              name:
                type: string
    responses:
      201:
        description: Категория добавлена
      400:
        description: Некорректные данные
      409:
        description: Категория уже существует
    """
    data = request.get_json() or {}

    name = data.get("name")
    if not name:
        return jsonify({"error": "Поле name обязательно"}), 400

    existing = Category.query.filter_by(name=name).first()
    if existing:
        return jsonify({"error": "Категория с таким названием уже существует"}), 409

    try:
        category = Category(name=name)
        db.session.add(category)

        resp = commit_or_rollback()
        if resp:
            return resp

        return jsonify({
            "message": "Категория успешно добавлена",
            "id": category.id
        }), 201

    except Exception as e:
        return jsonify({
            "error": "Ошибка при добавлении категории",
            "details": str(e)
        }), 500
@main.route("/categories/<int:id>", methods=["PUT"])
@staff_required(role=["staff", "admin"])
def update_category(id):
    """
    Добавить категорию
    ---
    tags:
      - Categories
    security:
      - BearerAuth: []
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
    security:
      - BearerAuth: []
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
@staff_required(role=["admin", "staff"])
def add_brand():
    """
    Добавить бренд
    ---
    tags:
      - Brands
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
            properties:
              name:
                type: string
    responses:
      201:
        description: Бренд добавлен
      400:
        description: Некорректные данные
      409:
        description: Бренд уже существует
    """
    data = request.get_json() or {}

    name = data.get("name")
    if not name:
        return jsonify({"error": "Поле name обязательно"}), 400

    existing = Brand.query.filter_by(name=name).first()
    if existing:
        return jsonify({"error": "Бренд с таким названием уже существует"}), 409

    try:
        brand = Brand(name=name, country=data.get("country"))
        db.session.add(brand)

        resp = commit_or_rollback()
        if resp:
            return resp

        return jsonify({
            "message": "Бренд успешно добавлен",
            "id": brand.id
        }), 201

    except Exception as e:
        return jsonify({
            "error": "Ошибка при добавлении бренда",
            "details": str(e)
        }), 500

@main.route("/brands/<int:id>", methods=["PUT"])
@staff_required(role=["staff", "admin"])
def update_brand(id):
    """
    Обновить бренд
    ---
    tags:
      - Brands
    security:
      - BearerAuth: []
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
    security:
      - BearerAuth: []
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
    security:
      - BearerAuth: []
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
    supplier = Supplier(name=data["name"], phone=data.get("phone"), email=data.get("email"), address=data.get("address"))
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
    security:
      - BearerAuth: []
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
    if "phone" in data:
        supplier.phone = data["phone"]
    if "email" in data:
        supplier.email = data["email"]
    if "address" in data:
        supplier.address = data["address"]
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
    security:
      - BearerAuth: []
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
    security:
      - BearerAuth: []
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
              employee_id:
                type: integer
              items:
                type: array
                items:
                  type: object
                  required: [product_id, quantity, price]
                  properties:
                    product_id:
                      type: integer
                    quantity:
                      type: integer
                    price:
                      type: number
                      example: 1200.50
    responses:
      201:
        description: Поставка добавлена
      400:
        description: Ошибка данных
    """

    data = request.get_json()

    if not all(k in data for k in ["supplier_id", "items"]):
        return jsonify({"error": "Отсутствуют обязательные поля"}), 400

    try:
        supply = Supply(
            supplier_id=data["supplier_id"],
            employee_id=data.get("employee_id")
        )

        db.session.add(supply)
        db.session.flush()

        for item in data["items"]:

            if not all(k in item for k in ["product_id", "quantity", "price"]):
                db.session.rollback()
                return jsonify({"error": "В items обязательны product_id, quantity, price"}), 400

            product = Product.query.get(item["product_id"])

            if not product:
                db.session.rollback()
                return jsonify({"error": f"Товар с id={item['product_id']} не найден"}), 404

            # увеличиваем склад
            product.stock_quantity += item["quantity"]

            supply_item = SupplyItem(
                supply_id=supply.id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"]
            )

            db.session.add(supply_item)

        db.session.commit()

        return jsonify({
            "message": "Поставка успешно добавлена",
            "supply_id": supply.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Ошибка при добавлении поставки",
            "details": str(e)
        }), 500