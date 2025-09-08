from flask import Flask, url_for, request, redirect
from datetime import datetime
app = Flask(__name__) 

@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename="cat.jpg")
    css_path = url_for("static", filename="lab1.css")
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
        </style>
    </head>
    <body>
        <h1>Ошибка 404 :(</h1>
        <img src="''' + path + '''"><br><br>
        <div>
            Супер кот в депрессии, потому что такой страницы не существует
        </div>
    </body> 
</html>''', 404

@app.route("/")
@app.route("/index")
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
            
            <footer>
                Воспанчук Виктория Владимировна, ФБИ-31, 3 курс, 2023
            </footer>
        </div>
    </body>
</html>
'''

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           <body> 
        </html>""", 200, {"X-Server": "sample",
                          'Content-Type': 'text/plain; charset=utf-8'
                          }

@app.route("/lab1/author")
def author():
    name = 'Воспанчук Виктория Владимировна'
    group = 'ФБИ-31'
    faculty = 'ФБ'

    return """<!doctype html>
    <html>
        <body>
            <p>Студент: """ + name + """ </p>
            <p>Группа: """ + group + """ </p>
            <p>Факультет: """ + faculty + """ </p>
            <a href="/lab1/web">web</a>
            <br>
            <a href="/">На главную</a>
        </body>
    </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="ledy bag.png")
    css_path = url_for("static", filename="lab1.css")
    
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Леди Баг в шоке от back-end</h1>
        <p>(и я тоже)</p>
        <img src="''' + path + '''">
        <br>
        <a href="/">На главную</a>
    </body>
</html>
'''

count = 0 

@app.route("/lab1/counter")
def counter():
    cold = url_for("static", filename="холодильник.jpg")
    css_path = url_for("static", filename="lab1.css")
    global count
    count += 1
    time = datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Сколько раз я открыл холодильник: ''' + str(count) + '''</h1>
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
        <a href="/lab1/clear_counter">Очистить счетчик</a><br><br>
        <img src="''' + cold + '''">
        <br>
        <a href="/">На главную</a>
    </body>
</html>
'''

@app.route("/lab1/clear_counter")
def clear_counter():
    css_path = url_for("static", filename="lab1.css")
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Холодильник закрыт :(</h1>
        <p>Текущее значение счетчика: 0</p>
        <a href="/lab1/counter">Перейти к счетчику</a><br>
        <a href="/">На главную</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
        <a href="/">На главную</a>
    <body>
</html>
''', 201

@app.route("/lab1")
def lab1_index():
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
                Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                называемых микрофреймворков — минималистичных каркасов
                веб-приложений, сознательно предоставляющих лишь самые ба
                зовые возможности.
            </div><br>

            <a href="/">← На главную</a>
        </div>
    </body>
</html>
'''

@app.route("/lab1/error400")
def error400():
    style = url_for("static", filename="lab1.css")
    return '''
<!DOCTYPE html>
<html lang="ru">
    <head>
        <link rel="stylesheet" href="''' + style + '''">
        <title>Bad Request</title>
    </head>
    <body>
        <h1>
            Bad Request <br> 
            400
        </h1>
        <div>
            Ошибка 400 означает некорректный запрос
        </div>
    </body>
</html>
''', 400


@app.route("/lab1/error401")
def error401():
    style = url_for("static", filename="lab1.css")
    return '''
<!DOCTYPE html>
<html lang="ru">
    <head>
        <link rel="stylesheet" href="''' + style + '''">
        <title>Unauthorized</title>
    </head>
    <body>
        <h1>
            Unauthorized<br>
            401   
        </h1>
        <div>
            Ошибка 401 возникает, когда вы не имеете разрешения на доступ к запрашиваемому ресурсу
        </div>
    </body>
</html>
''', 401

@app.route("/lab1/error402")
def error402():
    style = url_for("static", filename="lab1.css")
    return '''
<!DOCTYPE html>
<html lang="ru">
    <head>
        <link rel="stylesheet" href="''' + style + '''">
        <title>Payment Required</title>
    </head>
    <body>
        <h1>
            Payment Required <br>
            402
        </h1>
        <div>
            Требуется оплата
        </div>
    </body>
</html>
''', 402

@app.route("/lab1/error403")
def error403():
    style = url_for("static", filename="lab1.css")
    return '''
<!DOCTYPE html>
<html lang="ru">
    <head>
        <link rel="stylesheet" href="''' + style + '''">
        <title>Forbidden</title>
    </head>
    <body>
        <h1>
            Forbidden <br>
            403
        </h1>
        <div>
            Доступ к запрошенному ресурсу запрещён
        </div>
    </body>
</html>
''', 403

@app.route("/lab1/error405")
def error405():
    style = url_for("static", filename="lab1.css")
    return '''
<!DOCTYPE html>
<html lang="ru">
    <head>
        <link rel="stylesheet" href="''' + style + '''">
        <title>Method Not Allowed</title>
    </head>
    <body>
        <h1>
            Method Not Allowed <br>
            405
        </h1>
        <div>
            Возникает, когда сервер распознает метод запроса, но не разрешает его для указанного ресурса.
        </div>
    </body>
</html>
''', 405

@app.route("/lab1/error418")
def error418():
    style = url_for("static", filename="lab1.css")
    return '''
<!DOCTYPE html>
<html lang="ru">
    <head>
        <link rel="stylesheet" href="''' + style + '''">
        <title>I'm a teapot</title>
    </head>
    <body>
        <h1>
            I'm a teapot <br>
            418
        </h1>
        <div>
            Я чайник
        </div>
    </body>
</html>
''', 418

@app.route("/lab1/error500")
def cause_error_500():
    result = 10 / 0
    return "Эта строка никогда не будет показана"

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