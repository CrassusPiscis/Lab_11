from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

# Инициализируем экстеншены
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name='default'):
    """Фабрика приложений Flask"""
    app = Flask(__name__)

    # Загружаем конфигурацию
    app.config.from_object(config[config_name])

    # Инициализируем расширения
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Настройка Flask-Login
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

    # Регистрируем blueprint'ы (маршруты)
    from app import routes
    app.register_blueprint(routes.bp)

    # Загрузчик пользователя (заглушка)
    @login_manager.user_loader
    def load_user(user_id):
        # Временная заглушка - всегда возвращает None
        return None

    # Создаем таблицы БД
    with app.app_context():
        db.create_all()

    return app