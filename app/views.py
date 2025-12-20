"""
Модуль с view-функциями (контроллерами) для книжной коллекции.
Пока содержит заглушки, которые будут заменены реальной логикой после реализации БД.
"""

from flask import render_template, Blueprint

# Создаем Blueprint для организации маршрутов
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """
    Главная страница приложения.
    Пока отображает статическую информацию.

    Returns:
        Отрендеренный шаблон index.html
    """
    return render_template('index.html',
                           page_title='Главная страница',
                           welcome_message='Добро пожаловать в книжную коллекцию!')


@bp.route('/books')
def books():
    """
    Страница со списком книг (каталог).
    Пока заглушка - будет заменена на реальные данные из БД.

    Returns:
        Отрендеренный шаблон books.html
    """
    # Временные данные для демонстрации
    # После реализации БД здесь будет Book.query.all() или подобное
    sample_books = [
        {
            'id': 1,
            'title': 'Мастер и Маргарита',
            'author': 'Михаил Булгаков',
            'year': 1967,
            'status': 'read'
        },
        {
            'id': 2,
            'title': 'Преступление и наказание',
            'author': 'Федор Достоевский',
            'year': 1866,
            'status': 'reading'
        },
        {
            'id': 3,
            'title': '1984',
            'author': 'Джордж Оруэлл',
            'year': 1949,
            'status': 'read'
        }
    ]

    return render_template('books.html',
                           books=sample_books,
                           page_title='Мои книги',
                           book_count=len(sample_books))


@bp.route('/add-book', methods=['GET', 'POST'])
def add_book():
    """
    Страница добавления новой книги.
    Пока только отображает форму (POST-обработка будет позже).

    Returns:
        Отрендеренный шаблон add_book.html
    """
    # Для GET-запроса просто отображаем форму
    # Для POST-запроса (когда форма будет работать) здесь будет обработка данных

    return render_template('add_book.html',
                           page_title='Добавить книгу',
                           form_action='/add-book')