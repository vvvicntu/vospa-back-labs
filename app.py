from flask import Flask, url_for, request, redirect
from datetime import datetime
app = Flask(__name__) 

@app.errorhandler(404)
def not_found(err):
    return "Нет такой страницы :(", 404

@app.route("/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
           <body> 
        </html>""", 200, {"X-Server": "sample",
                          'Content-Type': 'text/plain; charset=utf-8'
                          }

@app.route("/author")
def author():
    name = 'Воспанчук Виктория Влдаимировна'
    group = 'ФБИ-31'
    faculty = 'ФБ'

    return """<!doctype html>
    <html>
        <body>
            <p>Студент: """ + name + """ </p>
            <p>Группа: """ + group + """ </p>
            <p>Факультет: """ + faculty + """ </p>
            <a href="/web">web</a>
        </body>
    </html>"""

@app.route("/image")
def image():
    path = url_for("static", filename="ledy bag.png")
    return '''
<!doctype html>
<html>
    <body>
        <h1>Леди Баг</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''

count = 0 

@app.route("/counter")
def counter():
    global count
    count += 1
    time = datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
    </body>
</html>
'''
@app.route("/info")
def info():
    return redirect("/author")

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

