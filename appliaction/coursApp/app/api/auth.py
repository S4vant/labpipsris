# auth.py
from flask import Blueprint, request, jsonify, session
from app.models import Employee
from app import db
from app.config import ADMIN_MASTER_KEY
from werkzeug.security import check_password_hash
from app.decorators import staff_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    """
    Логин
    ----
    tags:
      - Auth
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

    data = request.json
    employee = Employee.query.filter_by(username=data["username"]).first()

    if not employee or not employee.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    session["employee_id"] = employee.id

    return jsonify({
        "employee": {
            "id": employee.id,
            "username": employee.username,
            "role": employee.role
        }
    })


@auth_bp.route("/logout", methods=["POST", "OPTIONS"])
@staff_required(role=["staff", "admin"])
def logout():
    """
    Логаут
    ----
    tags:
      - Auth
    responses:
      200:
        description: Успешный логаут
    """
    if request.method == "OPTIONS":
        return "", 200

    session.pop("employee_id", None)
    return jsonify({"message": "Logged out"}), 200


@auth_bp.route("/me", methods=["GET"])
@staff_required(role=["staff", "admin"])
def me():
    """
    Обо мне
    ----
    tags:
      - Auth
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
    employee_id = session.get("employee_id")

    if not employee_id:
        return jsonify({"employee": None}), 401

    employee = Employee.query.get(employee_id)

    return jsonify({
        "employee": {
            "id": employee.id,
            "username": employee.username,
            "role": employee.role
        }
    })

@auth_bp.route("/create_user", methods=["GET"])
@staff_required(role=["staff", "admin"])
def create_user():
    """
    Создать пользователя
    ----
    tags:
      - Auth
    responses:
      200:
        description: Пользователь создан
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string

    """
    if request.method == "OPTIONS":
        return "", 200

    data = request.json
    employee = Employee.query.filter_by(username=data["username"]).first()

    if employee:
        return jsonify({"error": "User already exists"}), 400
    
    employee = Employee(username=data["username"], role=data["role"])
    employee.set_password(data["password"])

    if data["create_key"]!=ADMIN_MASTER_KEY:
        return jsonify({"error": "Invalid key"}), 400
    
    db.session.add(employee)
    db.session.commit()
    return jsonify({"message": "User created"}), 200