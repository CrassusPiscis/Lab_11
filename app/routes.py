from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db
from app.models import User, Book
from app.forms import BookForm, RegistrationForm

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
    """Страница каталога книг"""
    genres = list(set([book['genre'] for book in temporary_books if book.get('genre')]))
    return render_template('books.html',
                           title='Каталог книг',
                           books=temporary_books,
                           genres=genres)
@bp.route('/books')
def books():
    """Просмотр всех книг (для примера)"""
    all_books = Book.query.all()
    return render_template('books.html', title='Все книги', books=all_books)


@bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        # Пока у нас нет полноценного логина, привяжем к первому юзеру в базе
        user = User.query.first()
        if not user:
            flash('Сначала создайте пользователя в базе!')
            return redirect(url_for('main.index'))

        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            year=form.year.data,
            genre=form.genre.data,
            description=form.description.data,
            reading_status=form.status.data,
            owner=user
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Книга успешно добавлена в каталог!')
        return redirect(url_for('main.books'))

    return render_template('add_book.html', title='Добавить книгу', form=form)

@bp.route('/book/<int:id>/edit', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book) # Предзаполняем форму данными книги
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.year = form.year.data
        book.genre = form.genre.data
        book.description = form.description.data
        book.reading_status = form.status.data
        db.session.commit()
        flash('Данные книги обновлены!')
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
