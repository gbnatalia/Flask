'''
Задание №7
Написать функцию, которая будет выводить на экран HTML страницу с блоками новостей.
Каждый блок должен содержать заголовок новости, краткое описание и дату публикации.
Данные о новостях должны быть переданы в шаблон через контекст.

Задание №9
Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна
(шапка, меню, подвал), и дочерние шаблоны для страниц категорий товаров и отдельных товаров.
Например, создать страницы "Одежда", "Обувь" и "Куртка", используя базовый шаблон.
'''

from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime as dt


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/Moscow/')
def moscow_news():
    moscow_context = {
        'title':'Новости столицы',
        'header_news': 'Новости столицы',
        'description': 'Краткое описание новостей столицы',
        'date': f'{dt.now()}'
    }
    return render_template('child.html', context = moscow_context)


@app.route('/Per/')
def perifer_news():
    perifer_context = {
    'title': 'Региональные новости',
    'header_news': 'Региональные новости',
    'description': 'Краткое описание региональных новостей',
    'date': f'{dt.now()}'
    }
    return render_template('child.html', context = perifer_context)


@app.route('/Mir/')
def world_news():
    world_context = {
    'title': 'Мировые новости',
    'header_news': 'Что творится на Западе',
    'description': 'Краткое описание новостей',
    'date': f'{dt.now()}'
    }
    return render_template('child.html', context = world_context)


if __name__ == '__main__':
    app.run()
