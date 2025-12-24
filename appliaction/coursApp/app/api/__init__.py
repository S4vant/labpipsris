from flask import Blueprint

api_bp = Blueprint("api", __name__)

from .auth import auth_bp
from .routes import main as routes_bp

api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(routes_bp)

__all__ = ["api_bp"]
