from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

# Инициализируем экстеншены
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """Фабрика приложений Flask"""
    app = Flask(__name__)

    #Загружаем конфигурацию Нет конфигурации пока
    app.config.from_object(config[config_name])

    # Инициализируем расширения
    db.init_app(app)
    migrate.init_app(app, db)

    # Регистрируем blueprint'ы (маршруты)
    from app import routes
    app.register_blueprint(routes.bp)

    # Создаем таблицы БД (для простоты, в production лучше использовать миграции)
    with app.app_context():
        db.create_all()

    return app