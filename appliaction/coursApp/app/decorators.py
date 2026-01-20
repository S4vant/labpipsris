# app/decorators.py
from functools import wraps
from flask import request, jsonify, g
from datetime import datetime
from app.models import EmployeeSession

def staff_required(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.method == "OPTIONS":
                return "", 200

            auth = request.headers.get("Authorization")
            print ("""auth: """, auth)
            if not auth or not auth.startswith("Bearer "):
                return jsonify({"error": "Unauthorized"}), 401

            token = auth.split()[1]

            session = EmployeeSession.query.filter_by(
                session_token=token,
                is_active=True
            ).first()

            if not session or session.expires_at < datetime.utcnow():
                return jsonify({"error": "Session expired"}), 401

            employee = session.employee

            if role:
                if isinstance(role, (list, tuple)):
                    if employee.role not in role:
                        return jsonify({"error": "Forbidden"}), 403
                else:
                    if employee.role != role:
                        return jsonify({"error": "Forbidden"}), 403

            g.employee = employee
            return func(*args, **kwargs)
        return wrapper
    return decorator