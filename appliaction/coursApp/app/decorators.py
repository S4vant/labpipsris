# app/decorators.py
from functools import wraps
from flask import session, jsonify

def staff_required(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "employee_id" not in session:
                return jsonify({"error": "Unauthorized"}), 401
            if role and session.get("role") != role:
                return jsonify({"error": "Forbidden"}), 403
            return func(*args, **kwargs)
        wrapper.__name__ = f"{func.__name__}_{role or 'any'}"  # уникальное имя
        return wrapper
    return decorator
