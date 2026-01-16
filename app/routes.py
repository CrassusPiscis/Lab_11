from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Book
from app.forms import BookForm, RegistrationForm, LoginForm

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
@login_required # Только залогиненные видят свои книги
def books():
    # Получаем книги только текущего пользователя
    user_books = current_user.books.all()
    return render_template('books.html', title='Мои книги', books=user_books)

@bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        # Пока у нас нет полноценного логина, привяжем к первому юзеру в базе
        user = current_user
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
@login_required
def edit_book(id):
    book = Book.query.get_or_404(id)
    # Защита: нельзя редактировать чужую книгу
    if book.owner != current_user:
        flash('У вас нет прав для редактирования этой книги.')
        return redirect(url_for('main.books'))

    form = BookForm(obj=book) # Предзаполняем форму данными из объекта
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.year = form.year.data
        book.genre = form.genre.data
        book.description = form.description.data
        book.reading_status = form.status.data
        db.session.commit()
        flash('Книга успешно обновлена!')
        return redirect(url_for('main.books'))

    # Чтобы SelectField при загрузке страницы показал текущий статус
    if request.method == 'GET':
        form.status.data = book.reading_status

    return render_template('add_book.html', title='Редактировать книгу', form=form)

@bp.route('/book/<int:id>/delete', methods=['POST'])
@login_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    if book.owner != current_user:
        flash('У вас нет прав для удаления этой книги.')
        return redirect(url_for('main.books'))

    db.session.delete(book)
    db.session.commit()
    flash('Книга удалена из вашего каталога.')
    return redirect(url_for('main.books'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Регистрация', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm() # Создай простую форму с username, password и submit
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Вход', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))