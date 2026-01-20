import os
from app.creds import creds
ADMIN_MASTER_KEY = "create-staff-2025"
class Config:
    """
    Базовая конфигурация приложения
    """
    DB_NAME, DB_USER, DB_PASSWORD, DB_PORT, DB_HOST, SECRET_KEY = creds()
    
    SESSION_COOKIE_SAMESITE = "Lax"  # или "None" если фронт на другом домене
    SESSION_COOKIE_HTTPONLY = True

    # DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    DEBUG = True
    # Database (MySQL + SQLAlchemy)
    # DB_USER = os.getenv("DB_USER", "coursapp")
    # DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    # DB_HOST = os.getenv("DB_HOST", "localhost")  
    # DB_PORT = os.getenv("DB_PORT", "3306")
    # DB_NAME = os.getenv("DB_NAME", "coursapp")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SWAGGER = {
    "title": "Course Project API",
    "uiversion": 3,
    "openapi": "3.0.2",
    "description": "API документация курсового проекта",

    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    },

    # ГЛОБАЛЬНАЯ авторизация (чтобы не писать security в каждом роуте)
    "security": [
        {
            "BearerAuth": []
        }
    ]
}

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False

    TIMEZONE = "UTC"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
