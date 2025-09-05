from flask import Flask, url_for
app = Flask(__name__) 

@app.route("/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
           <body> 
        </html>""" 

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
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
    </body>
</html>
'''
