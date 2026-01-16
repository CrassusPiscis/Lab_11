from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model): # Наследуем UserMixin
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128)) # Меняем password на хеш
    books = db.relationship('Book', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Функция для загрузки пользователя по ID из сессии
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(64))
    description = db.Column(db.Text)
    # Статус: не начата / читаю / прочитана
    reading_status = db.Column(db.String(20), default='не начата')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Внешний ключ для связи с пользователем
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'