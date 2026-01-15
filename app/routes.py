from flask import Blueprint, render_template
from app.models import User, Book

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Главная страница: список пользователей и кол-во их книг"""
    users = User.query.all()

    stats = {
        'total_books': Book.query.count(),
        'read_books': Book.query.filter_by(reading_status='прочитана').count(),
        'reading_books': Book.query.filter_by(reading_status='читаю').count()
    }

    return render_template('index.html', title='Главная', users=users, stats=stats)

@bp.route('/books')
def books():
    """Просмотр всех книг (для примера)"""
    all_books = Book.query.all()
    return render_template('books.html', title='Все книги', books=all_books)

@bp.route('/add_book')
def add_book():
    # Пока оставляем заглушкой, тут будет логика формы (WTForms)
    return render_template('add_book.html', title='Добавить книгу')