from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config['SECRET_KEY'] =  b'd3971cd68599c7c2b2d03f7481cba48f6dc579d9092a5da7a48e018afe0feee4'
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return 'Hi!'


@app.route('/zd5/', methods=['POST', 'GET'])
@csrf.exempt
def zd5():
    '''
    Задание №5
    Создать страницу, на которой будет форма для ввода двух чисел и выбор операции
    (сложение, вычитание, умножение или деление) и кнопка "Вычислить"
    При нажатии на кнопку будет произведено вычисление результата выбранной операции и
    переход на страницу с результатом.
    '''
    if request.method == 'POST':
        valid_operations = ['+', '*', '/']
        num1 = request.form['num1']
        num2 = request.form['num2']
        op = request.form['op']
        if num1.isdigit() and num2.isdigit() and op in valid_operations:
            if op == "+":
                result = int(num1) + int(num2)
            elif op == "*":
                result = int(num1) * int(num2)
            elif num2 != '0':
                result = int(num1) / int(num2)
            else:
                print('Недопустимая операция!')
                return render_template('zd5.html')
            return render_template("zd5_2.html", result=result)
        else:
            print('Некорректные исходные данные операции')
    return render_template('zd5.html')


@app.route('/zd6/', methods=['POST', 'GET'])
@csrf.exempt
def zd6():
    '''
    Задание №6
    Создать страницу, на которой будет форма для ввода имени и возраста пользователя и
    кнопка "Отправить". При нажатии на кнопку будет произведена проверка возраста и
    переход на страницу с результатом или на страницу с ошибкой в случае некорректного возраста.
    '''
    if request.method == 'POST':
        context = {'name':"", 'age':'0'}
        context['name'] = request.form['name']
        context['age']  = request.form['age']
        if len(context['name']) and context['age'].isdigit() and int(context['age']) > 0:
            return render_template('zd6_2.html', context=context)
        else:
            return render_template('zd6_3.html', context=context)
    return render_template('zd6.html')


@app.route('/zd7/', methods=['POST', 'GET'])
@csrf.exempt
def zd7():
    '''
    Задание №7
    Создать страницу, на которой будет форма для ввода числа и кнопка "Отправить"
    При нажатии на кнопку будет произведено перенаправление на страницу с результатом,
    где будет выведено введенное число и его квадрат.
    '''

    if request.method == 'POST':
        c_num = request.form['num']
        if c_num.isdigit():
            context = {}
            context['num'] = int(c_num)
            context['num2'] = context['num'] * context['num']
            return render_template('zd7_2.html', **context)

    return render_template('zd7.html')


@app.route('/zd8/', methods=['POST', 'GET'])
@csrf.exempt
def zd8():
    '''
    Задание №8
    Создать страницу, на которой будет форма для ввода имени и кнопка "Отправить"
    При нажатии на кнопку будет произведено перенаправление на страницу с flash сообщением,
    где будет выведено "Привет, {имя}!".
    '''
    if request.method == 'POST':
        name = request.form['name']
        flash(f'Привет, {name}!')
        return render_template('zd8_2.html')
    return render_template('zd8.html')


@app.route('/zd9/', methods=['POST', 'GET'])
@csrf.exempt
def zd9():
    '''
    Задание №9
    Создать страницу, на которой будет форма для ввода имени и электронной почты
    При отправке которой будет создан cookie файл с данными пользователя
    Также будет произведено перенаправление на страницу приветствия, где будет
    отображаться имя пользователя. На странице приветствия должна быть кнопка "Выйти"
    При нажатии на кнопку будет удален cookie файл с данными пользователя и
    произведено перенаправление на страницу ввода имени и электронной почты.
    '''
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        if len(session['name']):
            return render_template('zd9_2.html')
    return render_template('zd9.html')

@app.route('/logout/')
def logout():
    session.pop('username', None)
    return render_template('zd9.html')


if __name__ == '__main__':
    app.run()
