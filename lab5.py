from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

def db_connect():
    # Подключение к postgres
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='vika_vosp',
            user='vika_vosp',
            password='666'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        # Подключение к SQLite
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    # проверяет существование ключа в сессии
    if 'login' in session:
        return render_template('lab5/register.html', login=session['login'], message='Вы не можете зарегистрироваться, находясь в аккаунте. Хотите выйти?')

    if request.method == 'GET':
        return render_template('lab5/register.html', login=session.get('login'))
    
    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name', '')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')
        
    conn, cur = db_connect()
    
    # sql-инъекция
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))
        
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)
    
    # добавление пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users(login, password, real_name) VALUES (%s, %s, %s);", (login, password_hash, real_name))
    else:
        cur.execute("INSERT INTO users(login, password, real_name) VALUES (?, ?, ?);", (login, password_hash, real_name))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if 'login' in session:
        return render_template('lab5/success_login.html', login=session['login'])

    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    # поиск пользователя в базе
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    # вернется одна строка  с параметрами 
    user = cur.fetchone()

    # если пользователь не найден в базе
    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html', login=login)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite', 'off') == 'on'
    is_public = request.form.get('is_public', 'off') == 'on'

    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните все поля', login=login, title=title, article_text=article_text)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) VALUES (%s, %s, %s, %s, %s);",
            (user_id, title, article_text, is_favorite, is_public)
        )
    else:
        cur.execute(
            "INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) VALUES (?, ?, ?, ?, ?);",
            (user_id, title, article_text, is_favorite, is_public)
        )

    db_close(conn, cur)
    return redirect('/lab5/')


@lab5.route('/lab5/list')
def list():

    login = session.get('login')

    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    # получение ID пользователя
    user_id = user["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC;", (user_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=? ORDER BY is_favorite DESC;", (user_id,))
    articles = cur.fetchall()

    if not articles:
        return render_template('lab5/articles.html', message='У вас пока нет ни одной статьи', login=login)

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles, login=login)


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
        
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return redirect('/lab5/list')

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', login=login, article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite', 'off') == 'on' # чекбокс
    is_public = request.form.get('is_public', 'off') == 'on'

    if not title or not article_text:
        return render_template('lab5/edit_article.html', error='Заполните все поля', login=login, article=article)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE articles SET title=%s, article_text=%s, is_favorite=%s, is_public=%s WHERE id=%s;",
            (title, article_text, is_favorite, is_public, article_id)
        )
    else:
        cur.execute(
            "UPDATE articles SET title=?, article_text=?, is_favorite=?, is_public=? WHERE id=?;",
            (title, article_text, is_favorite, is_public, article_id)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
        
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/favorite_articles')
def favorite_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s AND is_favorite=TRUE;", (user_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=? AND is_favorite=?;", (user_id, True))
    favorite_articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/favorite_articles.html', articles=favorite_articles, login=login)


@lab5.route('/lab5/public_articles')
def public_articles():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT a.*, u.login, u.real_name FROM articles a JOIN users u ON a.user_id = u.id WHERE a.is_public=TRUE;")
    else:
        cur.execute("SELECT a.*, u.login, u.real_name FROM articles a JOIN users u ON a.user_id = u.id WHERE a.is_public=?;", (True,))
    public_articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=public_articles, login=session.get('login'))


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/login')


@lab5.route('/lab5/users')
def users():
    login = session.get('login')
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    users = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/users.html', users=users, login=login)


@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login, real_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT login, real_name FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user, login=login)
    
    real_name = request.form.get('real_name')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    
    if new_password:
        if not check_password_hash(user['password'], current_password):
            db_close(conn, cur)
            return render_template('lab5/profile.html', user=user, error="Текущий пароль неверен", login=login)
        
        if new_password != confirm_password:
            db_close(conn, cur)
            return render_template('lab5/profile.html', user=user, error="Новый пароль и подтверждение не совпадают", login=login)
        
        #  в GET мы взяли только login, real_name, а теперь нужен пароль для проверки
        new_password_hash = generate_password_hash(new_password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s, password=%s WHERE login=%s;", (real_name, new_password_hash, login))
        else:
            cur.execute("UPDATE users SET real_name=?, password=? WHERE login=?;", (real_name, new_password_hash, login))
    else:
        # если новый пароль не введён то обновляем только real_name
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s WHERE login=%s;", (real_name, login))
        else:
            cur.execute("UPDATE users SET real_name=? WHERE login=?;", (real_name, login))
    
    conn.commit()
    db_close(conn, cur)
    return redirect('/lab5/profile')