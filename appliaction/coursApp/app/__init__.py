from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_cors import CORS
from flasgger import Swagger

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    swagger = Swagger(app)

    # Импорт Blueprint после инициализации расширений
    from app.api import api_bp

    # Регистрируем Blueprint
    app.register_blueprint(api_bp, url_prefix="/api")

    # Включаем CORS для всего приложения (в том числе для Blueprint)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    print(app.url_map)  # можно убрать, для отладки

    return app
