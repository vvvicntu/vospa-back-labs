from flask import Flask, url_for, request, redirect, abort, render_template
from datetime import datetime
app = Flask(__name__) 
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
@app.route("/lab1/index")
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
                          'Content-Type': 'text/csv; charset=utf-8'
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
''', 200, {"Content-Language": "ru-RU",
           "X-Custom-Header": "MyCustomValue",
           "X-Application-Version": "1.0.0",
           "Content-Type": "text/html; charset=utf-8"
          }

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

#Лабораторная работа №2 

@app.route('/lab2/a')
def a1():
    return 'без слеша'

@app.route('/lab2/a/')
def a2():
    return 'со слешем'


flower_list = ['Bud', 'Essa', 'Старый мельник', 'Krone']

# Страница с ID
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return render_template(
            'beer.html',
            flower_name=flower_list[flower_id],
            flower_id=flower_id,
            total_count=len(flower_list)
        )

# Добавление нового пива   
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return  f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлено новое пиво!</h1>
    <p>Марка нового пива: {name}</p>
    <p>Всего бутылок: {len(flower_list)} </p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

# Весь список
@app.route('/lab2/flowers')
def all_flowers():
    return render_template(
        'all.html',
        flower_list=flower_list,
        total_count=len(flower_list)
    )

# Ошибка 400
@app.route('/lab2/add_flower/')
def add_flower_empty():
    style = url_for("static", filename="main.css")
    beer = url_for("static", filename="beer.jpg")
    return '''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="''' + style + '''">
            <style>
                body {
                    text-align: center;
                    font-family: Arial, sans-serif;
                    margin: 50px;
                    font-size: 25px;
                }
                img {
                    margin: 20px auto;
                    max-width: 500px;
                    border-radius: 10px;
                }
            </style>
        </head>
        <body>
            <h1>Ошибка 400</h1>
            <p>Вы не задали марку пива</p>
            <img src="''' + beer + '''" alt="Пиво">
            <p><a href="/lab2/">Вернуться к лабораторной работе</a></p>
        </body>
    </html>
    ''', 400

# Очистка списка
@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Список очищен</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 50px;
                    background-color: rgb(204, 229, 255);
                }
                .success {
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    text-align: center;
                }
                
                .btn {
                    display: inline-block;
                    margin: 10px;
                    padding: 12px 24px;
                    background: #0066cc;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background 0.3s;
                }
            </style>
        </head>
        <body>
            <div class="success">
                <div>
                    <h1>Список пив очищен!</h1>
                    <p>Все бутылки были убраны из коллекции.</p>
                </div>
                <a href="/lab2/flowers" class="btn">Перейти к списку пив</a>
                <a href="/lab2/add_flower/Жигулевское" class="btn"> Добавить Жигулевское</a>
                <a href="/lab2/" class="btn">Назад к лабораторной</a>
            </div>
        </body>
    </html>
    '''

@app.route('/lab2/example')
def example():
    name = 'Воспанчук Виктория'
    group = 'ФБИ-31'
    course = '3 курс'
    lab_num = '2'
    kvami = [
        {'name': 'плаг', 'talisman': 'кот'}, 
        {'name': 'нууру', 'talisman': 'бабочка'},
        {'name': 'тикки', 'talisman': 'божья коровка'}, 
        {'name': 'сасс', 'talisman': 'змея'},
        {'name': 'триккс', 'talisman': 'лиса'}
    ]
    return render_template('example.html', name=name, group=group, course=course, 
                           lab_num=lab_num, kvami=kvami)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

# Перенаправление на /lab2/calc/1/1
@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

# Перенаправление на /lab2/calc/a/1
@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('calc', a=a, b=1))

# Основной обработчик калькулятора
@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    
    operations = {
        'sum': a + b,
        'diff': a - b,
        'mult': a * b,
        'div': a / b if b != 0 else 'деление на ноль',
        'pow': a ** b
    }
    return render_template('calc.html', a=a, b=b, operations=operations)

@app.route('/lab2/books')
def books():
    books_list = [
        {'author': 'Энтони Берджес', 'title': 'Заводной апельсин', 'genre': 'Роман', 'pages': 671},
        {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
        {'author': 'Джейн Остен', 'title': 'Гордость и предубеждение', 'genre': 'Роман', 'pages': 350},
        {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
        {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
        {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
        {'author': 'Уильям Голдинг', 'title': 'Повелитель мух', 'genre': 'Роман', 'pages': 288},
        {'author': 'Кристина Старк', 'title': 'Крылья', 'genre': 'Роман', 'pages': 840},
        {'author': 'Владимир Набоков', 'title': 'Лолита', 'genre': 'Роман', 'pages': 336},
        {'author': 'Джонатан С. Фоер', 'title': 'Жутко громко и запредельно близко', 'genre': 'Драма', 'pages': 624}
    ]
    return render_template('books.html', books=books_list)

@app.route('/lab2/nerves')
def nerves_songs():
    songs_list = [
        {'title': 'Перегорели', 'image': 'peregoreli.jpg', 'description': 'Моя любимая песня', 'year': 2015},
        {'title': 'Нервы', 'image': 'nervy.jpg', 'description': 'Снова праздник, снова ты', 'year': 2016},
        {'title': 'Батареи', 'image': 'baterii.jpg', 'description': 'Батареи заплакали', 'year': 2015},
        {'title': 'Кофе мой друг', 'image': 'kofe_moy_drug.jpg', 'description': 'До 2022 была кофейня с анаогичным названием', 'year': 2016},
        {'title': 'Слишком влюблён', 'image': 'slishkom_vlyublen.webp', 'description': 'Первая песня, которую я сыграла на барабанах', 'year': 2017},
        {'title': 'Родной город', 'image': 'rodnoy_gorod.jpg', 'description': 'Одна из любимых', 'year': 2015},
        {'title': 'Мой друг', 'image': 'moy_drug.jpg', 'description': 'Посвящена дружбе', 'year': 2020},
        {'title': 'Потери', 'image': 'poteri.jpg', 'description': 'Трек из последнего альбома', 'year': 2020},
        {'title': 'Вклочья', 'image': 'vklochia.jpg', 'description': '110%', 'year': 2017},
        {'title': 'Отрицательный герой', 'image': 'geroy.webp', 'description': 'Я падаю вниз, я срываюсь со всех краев', 'year': 2019},
        {'title': 'Ты права', 'image': 'ti_prava.webp', 'description': 'Конечно, я всегда права', 'year': 2018},
        {'title': 'Костёр', 'image': 'koster.webp', 'description': 'Самый старый альбом', 'year': 2016},
        {'title': 'Вороны', 'image': 'vorony.jpg', 'description': 'По моей команте гуляют черные вороны', 'year': 2017},
        {'title': 'Мои демоны', 'image': 'demon.jpg', 'description': 'Ты их сделала!', 'year': 2019},
        {'title': 'Лучшая жизнь', 'image': 'best_life.jpg', 'description': 'Лучшей жизни, чем в моих руках', 'year': 2018},
        {'title': 'На вынос', 'image': 'na_vinos.jpg', 'description': 'Альбом "7"', 'year': 2020},
        {'title': 'Укачу', 'image': 'ukachu.jpg', 'description': 'Я укачу от тебя, да я не шучу', 'year': 2019},
        {'title': 'Этому городу', 'image': 'town.jpg', 'description': 'Ностальгия по 2020', 'year': 2017},
        {'title': 'А А А', 'image': 'a.jpg', 'description': 'АААААААААААААА', 'year': 2018},
        {'title': 'Лампами', 'image': 'lamps.jpeg', 'description': 'Трек Жени и Ромы', 'year': 2021}
    ]
    return render_template('nerves.html', songs=songs_list)