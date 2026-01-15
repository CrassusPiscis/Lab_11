from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

bp = Blueprint('main', __name__)

# Временное хранилище книг (будет заменено на БД после feature/models)
temporary_books = [
    {
        'id': 1,
        'title': 'Мастер и Маргарита',
        'author': 'Михаил Булгаков',
        'year': 1967,
        'genre': 'Роман',
        'reading_status': 'прочитана',
        'description': 'Классика русской литературы о добре и зле',
        'timestamp': datetime.utcnow()
    },
    {
        'id': 2,
        'title': 'Преступление и наказание',
        'author': 'Федор Достоевский',
        'year': 1866,
        'genre': 'Роман',
        'reading_status': 'читаю',
        'description': 'Психологический роман о преступлении и наказании',
        'timestamp': datetime.utcnow()
    },
    {
        'id': 3,
        'title': '1984',
        'author': 'Джордж Оруэлл',
        'year': 1949,
        'genre': 'Антиутопия',
        'reading_status': 'не начата',
        'description': 'Роман о тоталитарном обществе будущего',
        'timestamp': datetime.utcnow()
    }
]


# Простая заглушка для формы
class SimpleForm:
    def __init__(self, **kwargs):
        self.data = {}

    def hidden_tag(self):
        return ''


# Создаем простую форму для книг
class BookForm(SimpleForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = type('obj', (object,), {'errors': [], 'data': kwargs.get('title', '')})()
        self.author = type('obj', (object,), {'errors': [], 'data': kwargs.get('author', '')})()
        self.year = type('obj', (object,), {'errors': [], 'data': kwargs.get('year', '')})()
        self.genre = type('obj', (object,), {'errors': [], 'data': kwargs.get('genre', '')})()
        self.description = type('obj', (object,), {'errors': [], 'data': kwargs.get('description', '')})()
        self.reading_status = type('obj', (object,),
                                   {'errors': [], 'data': kwargs.get('reading_status', 'не начата')})()

    def submit(self, **kwargs):
        return ''


@bp.route('/')
def index():
    """Главная страница"""
    stats = {
        'total_books': len(temporary_books),
        'read_books': len([b for b in temporary_books if b['reading_status'] == 'прочитана']),
        'reading_books': len([b for b in temporary_books if b['reading_status'] == 'читаю'])
    }

    return render_template('index.html',
                           title='Главная',
                           stats=stats,
                           recent_books=temporary_books[:2])


@bp.route('/books')
def books():
    """Страница каталога книг"""
    genres = list(set([book['genre'] for book in temporary_books if book.get('genre')]))
    return render_template('books.html',
                           title='Каталог книг',
                           books=temporary_books,
                           genres=genres)


@bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Страница добавления книги"""
    form = BookForm()

    if request.method == 'POST':
        # Получаем данные из формы
        book_data = {
            'id': len(temporary_books) + 1,
            'title': request.form.get('title', '').strip(),
            'author': request.form.get('author', '').strip(),
            'year': request.form.get('year', ''),
            'genre': request.form.get('genre', 'Не указан'),
            'reading_status': request.form.get('reading_status', 'не начата'),
            'description': request.form.get('description', 'Описание отсутствует'),
            'timestamp': datetime.utcnow()
        }

        # Проверяем обязательные поля
        if not book_data['title'] or not book_data['author']:
            flash('Пожалуйста, заполните название и автора книги', 'warning')
            return render_template('add_book.html', title='Добавить книгу', form=form)

        # Добавляем книгу во временное хранилище
        temporary_books.append(book_data)

        # Сообщение об успехе
        flash(f'Книга "{book_data["title"]}" успешно добавлена!', 'success')

        # Перенаправляем на страницу книг
        return redirect(url_for('main.books'))

    # GET запрос - просто показываем форму
    return render_template('add_book.html', title='Добавить книгу', form=form)


@bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    """Страница редактирования книги"""
    # Находим книгу по ID
    book = next((b for b in temporary_books if b['id'] == book_id), None)
    if not book:
        flash('Книга не найдена', 'danger')
        return redirect(url_for('main.books'))

    if request.method == 'POST':
        # Обновляем данные книги
        book['title'] = request.form.get('title', '').strip()
        book['author'] = request.form.get('author', '').strip()
        book['year'] = request.form.get('year', '')
        book['genre'] = request.form.get('genre', 'Не указан')
        book['reading_status'] = request.form.get('reading_status', 'не начата')
        book['description'] = request.form.get('description', 'Описание отсутствует')

        # Проверяем обязательные поля
        if not book['title'] or not book['author']:
            flash('Пожалуйста, заполните название и автора книги', 'warning')
        else:
            flash(f'Книга "{book["title"]}" успешно обновлена!', 'success')
            return redirect(url_for('main.books'))

    # Создаем форму с данными книги (для GET или если были ошибки в POST)
    form = BookForm(
        title=book['title'],
        author=book['author'],
        year=book['year'],
        genre=book['genre'],
        description=book['description'],
        reading_status=book['reading_status']
    )

    return render_template('edit_book.html', title='Редактировать книгу', form=form, book=book)


@bp.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    """Удаление книги"""
    global temporary_books
    book = next((b for b in temporary_books if b['id'] == book_id), None)
    if book:
        temporary_books = [b for b in temporary_books if b['id'] != book_id]
        flash(f'Книга "{book["title"]}" удалена', 'success')
    else:
        flash('Книга не найдена', 'danger')

    return redirect(url_for('main.books'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа"""
    form = SimpleForm()

    if request.method == 'POST':
        # Временная логика - всегда успешный вход
        flash('Вход выполнен успешно!', 'success')
        return redirect(url_for('main.index'))

    return render_template('login.html', title='Вход в систему', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    form = SimpleForm()

    if request.method == 'POST':
        # Временная логика - всегда успешная регистрация
        flash('Регистрация успешна! Теперь войдите в систему.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', title='Регистрация', form=form)


@bp.route('/logout')
def logout():
    """Выход из системы"""
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('main.index'))


@bp.route('/test-flash')
def test_flash():
    """Тестовая страница для проверки flash-сообщений"""
    flash('Это успешное сообщение!', 'success')
    flash('Это предупреждение!', 'warning')
    flash('Это ошибка!', 'danger')
    flash('Это информационное сообщение', 'info')
    return redirect(url_for('main.index'))