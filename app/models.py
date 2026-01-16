from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    # Связь с книгами: один пользователь может иметь много книг
    books = db.relationship('Book', backref='owner', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

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