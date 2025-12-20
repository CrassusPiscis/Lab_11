from flask import Blueprint, render_template, request, redirect, url_for, flash


bp = Blueprint('main', __name__)


# Временное хранилище книг (будет заменено на БД после feature/models)
temporary_books = [
    {
        'id': 1,
        'title': 'Мастер и Маргарита',
        'author': 'Михаил Булгаков',
        'year': 1967,
        'genre': 'Роман',
        'status': 'read',
        'description': 'Классика русской литературы о добре и зле'
    },
    {
        'id': 2,
        'title': 'Преступление и наказание',
        'author': 'Федор Достоевский',
        'year': 1866,
        'genre': 'Роман',
        'status': 'reading',
        'description': 'Психологический роман о преступлении и наказании'
    }
]


@bp.route('/')
def index():
    """Главная страница"""
    stats = {
        'total_books': len(temporary_books),
        'read_books': len([b for b in temporary_books if b['status'] == 'read']),
        'reading_books': len([b for b in temporary_books if b['status'] == 'reading'])
    }

    return render_template('index.html',
                           title='Главная',
                           stats=stats,
                           recent_books=temporary_books[:2])

@bp.route('/books')
@bp.route('/books')
def books():
    """Страница каталога книг"""
    return render_template('books.html',
                          title='Мои книги',
                          books=temporary_books,
                          book_count=len(temporary_books))


@bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Страница добавления книги"""
    if request.method == 'POST':
        # Получаем данные из формы
        book_data = {
            'id': len(temporary_books) + 1,
            'title': request.form.get('title', '').strip(),
            'author': request.form.get('author', '').strip(),
            'year': request.form.get('year', 'Не указан'),
            'genre': request.form.get('genre', 'Не указан'),
            'status': request.form.get('status', 'reading'),
            'description': request.form.get('description', 'Описание отсутствует')
        }

        # Проверяем обязательные поля
        if not book_data['title'] or not book_data['author']:
            flash('Пожалуйста, заполните название и автора книги', 'warning')
            return render_template('add_book.html', title='Добавить книгу')

        # Добавляем книгу во временное хранилище
        temporary_books.append(book_data)

        # Сообщение об успехе
        flash(f'Книга "{book_data["title"]}" успешно добавлена!', 'success')

        # Перенаправляем на страницу книг
        return redirect(url_for('main.books'))

    # GET запрос - просто показываем форму
    return render_template('add_book.html', title='Добавить книгу')