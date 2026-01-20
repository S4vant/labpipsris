# app/routes/auth.py
from flask import Blueprint, request, jsonify, g
from datetime import datetime
from app import db
from app.models import Employee, EmployeeSession
from app.config import ADMIN_MASTER_KEY
from app.decorators import staff_required


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    """
    Логин
    ----
    tags:
      - Auth
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [username, password]
            properties:
              username:
                type: string
              password:
                type: string
    responses:
      200:
        description: Успешный логин
    """
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Invalid request"}), 400

    username = data["username"]
    password = data["password"]

    employee = Employee.query.filter_by(username=username).first()

    if not employee or not employee.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Проверяем, есть ли уже активная сессия
    session = EmployeeSession.query.filter_by(employee_id=employee.id, is_active=True).first()

    if session:
        # Перезаписываем токен и продлеваем время действия
        session.session_token = EmployeeSession.generate_token()
        session.expires_at = EmployeeSession.default_expiration(days=7)
    else:
        # Создаём новую сессию
        session = EmployeeSession(
            session_token=EmployeeSession.generate_token(),
            employee_id=employee.id,
            expires_at=EmployeeSession.default_expiration(days=7)
        )
        db.session.add(session)

    db.session.commit()

    return jsonify({
        "token": session.session_token,
        "employee": {
            "id": employee.id,
            "username": employee.username,
            "role": employee.role
        }
    }), 200


@auth_bp.route("/logout", methods=["POST", "OPTIONS"])
@staff_required(role=["staff", "admin"])
def logout():
    """
    Логаут
    ----
    tags:
      - Auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: Успешный логаут
    """
    if request.method == "OPTIONS":
        return "", 200

    auth = request.headers.get("Authorization")
    token = auth.split()[1]

    session = EmployeeSession.query.filter_by(
        session_token=token,
        is_active=True
    ).first()

    if session:
        session.is_active = False
        db.session.commit()

    return jsonify({"message": "Logged out"}), 200


@auth_bp.route("/me", methods=["GET"])
@staff_required(role=["staff", "admin"])
def me():
    """
    Обо мне
    ----
    tags:
      - Auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: Обо мне
        content:
          application/json:
            schema:
              type: object
              properties:
                employee:
                  type: object
                  properties:
                    id:
                      type: integer
                    username:
                      type: string
                    role:
                      type: string
    """
    employee = g.employee

    return jsonify({
        "employee": {
            "id": employee.id,
            "username": employee.username,
            "role": employee.role
        }
    }), 200

@auth_bp.route("/create_user", methods=["POST", "OPTIONS"])
@staff_required(role=["staff", "admin"])
def create_user():
    """
    Создать пользователя
    ---
    tags:
      - Auth
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - password
              - role
            properties:
              username:
                type: string
              password:
                type: string
              role:
                type: string
                enum: ["staff", "admin"]
    responses:
      201:
        description: Пользователь создан
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      400:
        description: Ошибка запроса (пользователь существует или поля отсутствуют)
      403:
        description: Forbidden (только admin может создавать admin)
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    # Проверка обязательных полей
    required_fields = {"username", "password", "role"}
    if not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    # Проверка роли: обычный staff не может создать admin
    if data["role"] == "admin" and g.employee.role != "admin":
        return jsonify({"error": "Forbidden: only admin can create admin users"}), 403

    # Проверка, что пользователь с таким username ещё не существует
    if Employee.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User already exists"}), 400

    # Создание пользователя
    employee = Employee(
        username=data["username"],
        role=data["role"]
    )
    employee.set_password(data["password"])

    db.session.add(employee)
    db.session.commit()

    return jsonify({"message": f"User '{employee.username}' created"}), 201
