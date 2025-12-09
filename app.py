from flask import Flask, url_for, request, redirect, abort, render_template
from datetime import datetime
import os
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from rgz import rgz

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный ключ')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(rgz)

access_log = [] #история посещений сайта

@app.errorhandler(404) #обработчик ошибки 404
def not_found(err):
    path = url_for("static", filename="cat.jpg")
    css_path = url_for("static", filename="lab1.css")
    user_ip = request.remote_addr # IP-адрес пользователя
    access_time = str(datetime.now())
    request_url = request.url

    #добавляет запись в журнал в указанном порядке
    access_log.append(f"[{access_time}] пользователь {user_ip} зашёл на адрес: {request_url}")

    log_html = "<ul>"
    for entry in reversed(access_log): 
        log_html += f"<li>{entry}</li>"
    log_html += "</ul>"

    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
        <style>
            body {
                padding: 20px;
                background-color: #fed8ee;
            }
            img {
                margin-top: 20px;
                max-width: 50%;
                height: auto;
                border-radius: 10px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <h1>Ошибка 404 :(</h1>
        <img src="''' + path + '''" alt="Грустный кот" style="max-width: 300px;"><br><br>
        <div>
            <h3>Супер кот в депрессии, потому что такой страницы не существует</h3>
            Ваш IP: ''' + str(user_ip) + '''<br> 
            Дата доступа: ''' + access_time + '''<br>
            <a href="/lab1/index"> На главную </a>
        </div>
        <div>
            <h2>Журнал посещений</h2>
            ''' + log_html + '''
        </div>
    </body> 
</html>''', 404

@app.route("/")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <style>
            body {
                padding: 20px;
                background-color: #fed8ee;
            }
            .off {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px black;
            }
            header {
                background: #c3418d;;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            footer {
                background: #c3418d;;
                color: white;
                padding: 15px;
                text-align: center;
                border-radius: 5px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="off">
            <header>
                <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            </header>
            
            <nav>
                <a href="/lab1">Лабораторная работа №1</a>
            </nav>

            <nav>
                <a href="/lab2">Лабораторная работа №2</a>
            </nav>

            <nav>
                <a href="/lab3">Лабораторная работа №3</a>
            </nav>

            <nav>
                <a href="/lab4">Лабораторная работа №4</a>
            </nav>

            <nav>
                <a href="/lab5">Лабораторная работа №5</a>
            </nav>

            <nav>
                <a href="/lab6">Лабораторная работа №6</a>
            </nav>

            <nav>
                <a href="/lab7">Лабораторная работа №7</a>
            </nav>

            <nav>
                <a href="/lab8">Лабораторная работа №8</a>
            </nav>

            <nav>
                <a href="/rgz">РГЗ</a>
            </nav>
            
            <footer>
                Воспанчук Виктория Владимировна, ФБИ-31, 3 курс, 2023
            </footer>
        </div>
    </body>
</html>
'''


    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная работа №1</title>
        <style>
            body {
                margin: 20px;
                background-color: #fed8ee;
            }
            .off {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2c3e50;
                text-align: center;
            }
            h2 {
                color: #2c3e50;
                text-align: center;
                margin-top: 30px;
            }
            .menu {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin: 20px 0;
            }
            .menu a {
                display: block;
                padding: 15px;
                background: #c3418d;
                color: white;
                border-radius: 5px;
                text-align: center;
                text-decoration: none;
            }
            
            .routes-list {
                margin: 20px 0;
            }
            .routes-list a {
                display: block;
                padding: 10px;
                margin: 5px 0;
                background: #f8f9fa;
                border-left: 4px solid #c3418d;
                text-decoration: none;
                color: #2c3e50;
            }
        
            .content{
                color: #2c3e50;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="off">
            <h1>Лабораторная работа №1</h1>
            <div class="menu">
                <a href="/lab1/web">Web-сервер</a>
                <a href="/lab1/author">Автор</a>
                <a href="/lab1/image">Изображение</a>
                <a href="/lab1/counter">Сколько раз я открыл холодильник</a>
                <a href="/lab1/info">Информация</a>
                <a href="/lab1/created">Создание</a>
            </div>
            <div class="content">
                Flask — фреймворк для создания веб-приложений на языке
                программирования Python, использующий набор инструментов
                Werkzeug, а также шаблонизатор Jinja2. Отrelativeтся к категории так
                называемых микрофреймворков — минималистичных каркасов
                веб-приложений, сознательно предоставляющих лишь самые ба
                зовые возможности.
            </div><br>

            <a href="/">← На главную</a>

            <h2>Список роутов</h2>
            <div class="routes-list">
                <a href="/index">Главная страница</a>
                <a href="/lab1">Лабораторная работа 1</a>
                <a href="/lab1/web">Web-сервер</a>
                <a href="/lab1/author">Информация об авторе</a>
                <a href="/lab1/image">Изображение</a>
                <a href="/lab1/counter">Сколько раз я открыл холодильник</a>
                <a href="/lab1/clear_counter">Очистка счетчика</a>
                <a href="/lab1/info">Информация (редирект)</a>
                <a href="/lab1/created">Создание (статус 201)</a>
                <a href="/lab1/error400">Ошибка 400 - Bad Request</a>
                <a href="/lab1/error401">Ошибка 401 - Unauthorized</a>
                <a href="/lab1/error402">Ошибка 402 - Payment Required</a>
                <a href="/lab1/error403">Ошибка 403 - Forbidden</a>
                <a href="/lab1/error405">Ошибка 405 - Method Not Allowed</a>
                <a href="/lab1/error418">Ошибка 418 - I'm a teapot</a>
                <a href="/lab1/error500">Ошибка 500 - Internal Server Error</a>
            </div>
        </div>
    </body>
</html>
'''

@app.errorhandler(500)
def internal_server_error(err):
    style = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + style + '''">
        <title>500 - Ошибка сервера</title>
    </head>
    <body>
        <h1>500 - Внутренняя ошибка сервера</h1>
            <a href="/">На главную</a> 
        </div>
    </body>
</html>
''', 500

@app.route("/lab1/error500")
def cause_error_500():
    result = 10 / 0
    return "Эта строка никогда не будет показана"

