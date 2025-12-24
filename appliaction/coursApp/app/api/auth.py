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
    if request.method == "OPTIONS":
        return "", 200

    session.pop("employee_id", None)
    return jsonify({"message": "Logged out"}), 200


@auth_bp.route("/me", methods=["GET"])
@staff_required(role=["staff", "admin"])
def me():
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

