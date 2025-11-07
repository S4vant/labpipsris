from flask import Blueprint, jsonify, request
from app import db
from app.models import Category, Brand, Supplier, Product, Customer, Employee, Order, OrderItem, Supply, SupplyItem
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

main = Blueprint("api", __name__)



@main.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ресурс не найден"}), 404

@main.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Внутренняя ошибка сервера"}), 500


def commit_or_rollback():
    """Безопасная фиксация изменений."""
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка целостности данных", "details": str(e.orig)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка базы данных", "details": str(e)}), 500




@main.route("/products", methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                
                "category_id": p.category_id,
                "brand_id": p.brand_id,
                "supplier_id": p.supplier_id,
            } for p in products
        ])
    except SQLAlchemyError as e:
        return jsonify({"error": "Ошибка при получении товаров", "details": str(e)}), 500


@main.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    required_fields = ["name", "price", "quantity", "category_id", "brand_id", "supplier_id"]

    # Проверка обязательных полей
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Отсутствует обязательное поле: {field}"}), 400

    try:
        new_product = Product(
            name=data["name"],
            price=data["price"],
            quantity=data["quantity"],
            category_id=data["category_id"],
            brand_id=data["brand_id"],
            supplier_id=data["supplier_id"]
        )
        db.session.add(new_product)
        response = commit_or_rollback()
        if response:
            return response
        return jsonify({"message": "Товар успешно добавлен"}), 201
    except Exception as e:
        return jsonify({"error": "Ошибка при добавлении товара", "details": str(e)}), 500


@main.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"error": "Товар не найден"}), 404

        for field in ["name", "price", "quantity", "category_id", "brand_id", "supplier_id"]:
            if field in data:
                setattr(product, field, data[field])

        response = commit_or_rollback()
        if response:
            return response
        return jsonify({"message": "Товар обновлён успешно"}), 200
    except Exception as e:
        return jsonify({"error": "Ошибка при обновлении товара", "details": str(e)}), 500


@main.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"error": "Товар не найден"}), 404

        db.session.delete(product)
        response = commit_or_rollback()
        if response:
            return response
        return jsonify({"message": "Товар удалён"}), 200
    except Exception as e:
        return jsonify({"error": "Ошибка при удалении товара", "details": str(e)}), 500




@main.route("/customers", methods=["GET"])
def get_customers():
    try:
        customers = Customer.query.all()
        return jsonify([{"id": c.id, "first_name": c.first_name, "last_name": c.last_name, "email": c.email, "phone": c.phone} for c in customers])
    except SQLAlchemyError as e:
        return jsonify({"error": "Ошибка при получении клиентов", "details": str(e)}), 500


@main.route("/customers", methods=["POST"])
def add_customer():
    data = request.get_json()
    if not all(k in data for k in ["first_name", "last_name", "email", "phone"]):
        return jsonify({"error": "Необходимо указать name, email и phone"}), 400
    try:
        new_customer = Customer(name=data["name"], email=data["email"], phone=data["phone"])
        db.session.add(new_customer)
        response = commit_or_rollback()
        if response:
            return response
        return jsonify({"message": "Клиент добавлен успешно"}), 201
    except Exception as e:
        return jsonify({"error": "Ошибка при добавлении клиента", "details": str(e)}), 500



@main.route("/orders", methods=["GET"])
def get_orders():
    try:
        orders = Order.query.all()
        return jsonify([
            {
                "id": o.id,
                "customer_id": o.customer_id,
                "employee_id": o.employee_id,
                "date": o.order_date,
                "status": o.status
            } for o in orders
        ])
    except SQLAlchemyError as e:
        return jsonify({"error": "Ошибка при получении заказов", "details": str(e)}), 500


@main.route("/orders", methods=["POST"])
def add_order():
    data = request.get_json()
    if not all(k in data for k in ["customer_id", "employee_id", "status"]):
        return jsonify({"error": "Отсутствуют обязательные поля: customer_id, employee_id, status"}), 400
    try:
        order = Order(customer_id=data["customer_id"], employee_id=data["employee_id"], status=data["status"])
        db.session.add(order)
        response = commit_or_rollback()
        
        if response:
            return response
        return jsonify({"message": "Заказ успешно создан"}), 201
    except Exception as e:
        return jsonify({"error": "Ошибка при создании заказа", "details": str(e)}), 500
