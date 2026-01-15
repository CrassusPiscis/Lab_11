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

    # Чтобы SelectField правильно выбрал текущий статус
    form.status.data = book.reading_status
    return render_template('add_book.html', title='Редактировать книгу', form=form)

@bp.route('/book/<int:id>/delete', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Книга удалена.')
    return redirect(url_for('main.books'))