from flask import Blueprint, render_template


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Главная страница"""
    return render_template('index.html', title='Главная')

@bp.route('/books')
def books():
    """Страница каталога книг"""
    return render_template('books.html', title='Каталог книг')

@bp.route('/add_book')
def add_book():
    """Страница добавления книги"""
    return render_template('add_book.html', title='Добавить книгу')