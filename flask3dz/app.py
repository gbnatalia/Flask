'''
8. Создать форму для регистрации пользователей на сайте.
    Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
    При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован
'''

import wtforms.csrf.core
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from .models import db, User8
from .form import LoginForm
from .form import RegistrationForm
'''
Генерация секретного ключа:
>>> import secrets
>>> secrets.token_hex()
'''
secret_key = b'd3971cd68599c7c2b2d03f7481cba48f6dc579d9092a5da7a48e018afe0feee4'

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///home_database.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('base.html')


#@app.route('/form', methods=['GET', 'POST'])
#@csrf.exempt
#def my_form():
#    return 'No CSRF protection!'


# Авторизация
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        pass
    return render_template('login.html', form=form)


# Регистрация
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        first_name = form.fisrt_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        if User8.query.filter(User8.email == email).first():
            flash(f'Пользователь с e-mail {email} уже существует')
            return redirect(url_for('register'))
        user = User8(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash(f'Вы успешно зарегистрировались!')
        return redirect(url_for('register'))
    return render_template('register.html', form=form)


@app.route('/users/')
def all_users():
    users = User8.query.all()
    context = {'users': users}
    return render_template('child.html', **context)


#######################################
# Команды для формирования БД
#######################################
@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


if __name__ == '__main__':
    app.run(debug=True)
