from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, ValidationError
from app.models import User

# Форма добавления/редактирования книги
class BookForm(FlaskForm):
    title = StringField('Название книги', validators=[DataRequired(), Length(min=1, max=128)])
    author = StringField('Автор', validators=[DataRequired(), Length(min=1, max=128)])
    year = IntegerField('Год издания', validators=[NumberRange(min=0, max=2026)])
    genre = StringField('Жанр', validators=[Length(max=64)])
    description = TextAreaField('Краткое описание')
    status = SelectField('Статус чтения', choices=[
        ('не начата', 'Не начата'),
        ('читаю', 'Читаю'),
        ('прочитана', 'Прочитана')
    ])
    submit = SubmitField('Сохранить книгу')

# Форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя уже занято. Выберите другое.')

# Форма входа
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')