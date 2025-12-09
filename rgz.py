from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, jsonify
import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

rgz = Blueprint('rgz', __name__)

ADMIN_LOGIN = "vika"
ADMIN_PASSWORD = "111"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ф-я ошибок
def make_error(code, msg, request_id=None):
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': code,
            'message': msg
        },
        'id': request_id
    }

def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='vika_rgz',
            user='vika_rgz',
            password='123'
        )
        conn.set_client_encoding('UTF8')
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
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

@rgz.route('/rgz/')
def main():
    if 'user_id' not in session:
        return render_template('rgz/rgz.html')
    return render_template('rgz/main.html', login=session.get('login'), is_admin=session.get('login') == ADMIN_LOGIN)

@rgz.route('/rgz/login')
def login_page():
    return render_template('rgz/login.html')

@rgz.route('/rgz/register')
def register_page():
    return render_template('rgz/register.html')

@rgz.route('/rgz/logout')
def logout():
    session.clear()
    return redirect('/rgz')

@rgz.route('/rgz/api', methods=['POST'])
def api():
    data = request.json
    request_id = data.get('id')

    if data.get('jsonrpc') != '2.0':
        return jsonify(make_error(-32600, 'Invalid Request', request_id))

    method = data.get('method')
    params = data.get('params', {})

    if method == 'register':
        return jsonify(handle_register(params, request_id))
    elif method == 'login':
        return jsonify(handle_login(params, request_id))
    elif method == 'logout':
        return jsonify(handle_logout(request_id))
    elif method == 'get_users':
        return jsonify(handle_get_users(request_id))
    elif method == 'get_messages':
        return jsonify(handle_get_messages(params, request_id))
    elif method == 'send_message':
        return jsonify(handle_send_message(params, request_id))
    elif method == 'delete_message':
        return jsonify(handle_delete_message(params, request_id))
    elif method == 'delete_user':
        return jsonify(handle_delete_user(params, request_id))
    else:
        return jsonify(make_error(-32601, 'Method not found', request_id))

# ф-и для каждого из методов
def handle_register(params, request_id):

    # убираем лишние пробелы
    login = params.get('login', '').strip()
    password = params.get('password', '').strip()

    if not login or not password:
        return make_error(2, "Логин и пароль обязательны", request_id)

    if len(login) < 3:
        return make_error(2, "Логин должен быть не менее 3 символов", request_id)

    password_hash = hash_password(password)

    conn, cur = db_connect()
    try:
        # добавляем пользователя (RETURNING id возвращает ID)
        cur.execute(
            "INSERT INTO users (login, password_hash) VALUES (%s, %s) RETURNING id",
            (login, password_hash)
        )
        user_id = cur.fetchone()['id'] # извлекает ID созданного пользователя
        return {'jsonrpc': '2.0', 'result': {'success': True, 'user_id': user_id}, 'id': request_id}

    except psycopg2.IntegrityError:
        return make_error(2, "Пользователь с таким логином уже существует", request_id)

    finally:
        db_close(conn, cur)


def handle_login(params, request_id):
    login = params.get('login', '').strip()
    password = params.get('password', '').strip()
    password_hash = hash_password(password)

    conn, cur = db_connect()

    # находим пользователя в бд
    cur.execute(
        "SELECT id, login FROM users WHERE login = %s AND password_hash = %s",
        (login, password_hash)
    )
    user = cur.fetchone()
    db_close(conn, cur)

    if not user:
        return make_error(2, "Неверный логин или пароль", request_id)

    # создаем сессию
    session['user_id'] = user['id']
    session['login'] = user['login']

    return {'jsonrpc': '2.0', 'result': {'success': True, 'user': {'id': user['id'], 'login': user['login']}}, 'id': request_id}


def handle_logout(request_id):
    session.clear()
    return {'jsonrpc': '2.0', 'result': {'success': True}, 'id': request_id}


def handle_get_users(request_id):
    # существует ли user_id в сессии
    if 'user_id' not in session:
        return make_error(1, "Требуется авторизация", request_id)

    conn, cur = db_connect()
    cur.execute(
        "SELECT id, login, created_at FROM users WHERE id != %s ORDER BY login",
        (session['user_id'],)
    )
    users = cur.fetchall()
    db_close(conn, cur)

    users_list = []
    for user in users:
        users_list.append({
            'id': user['id'],
            'login': user['login'],
            'created_at': user['created_at'].isoformat() if user['created_at'] else None
        })

    return {'jsonrpc': '2.0', 'result': users_list, 'id': request_id}


def handle_get_messages(params, request_id):
    if 'user_id' not in session:
        return make_error(1, "Требуется авторизация", request_id)
    
    # params приходит от фронта, получаем ID с кем показать переписку
    other_user_id = params.get('user_id')

    if not other_user_id:
        return make_error(2, "Не указан ID пользователя", request_id)

    # текущий ID
    user_id = session['user_id']

    conn, cur = db_connect()
    cur.execute('''
        SELECT m.id, m.sender_id, m.receiver_id, m.text, m.created_at,
               u1.login as sender_login, u2.login as receiver_login
        FROM messages m
        JOIN users u1 ON m.sender_id = u1.id
        JOIN users u2 ON m.receiver_id = u2.id
        WHERE ((m.sender_id = %s AND m.receiver_id = %s) OR 
               (m.sender_id = %s AND m.receiver_id = %s))
          AND NOT (m.sender_id = %s AND m.is_deleted_sender)
          AND NOT (m.receiver_id = %s AND m.is_deleted_receiver)
        ORDER BY m.created_at
    ''', (user_id, other_user_id, other_user_id, user_id, user_id, user_id))

    messages = cur.fetchall()
    db_close(conn, cur)

    messages_list = []
    for msg in messages:
        messages_list.append({
            'id': msg['id'],
            'sender_id': msg['sender_id'],
            'sender_login': msg['sender_login'],
            'receiver_id': msg['receiver_id'],
            'receiver_login': msg['receiver_login'],
            'text': msg['text'],
            'created_at': msg['created_at'].isoformat() if msg['created_at'] else None,
            'is_my': msg['sender_id'] == user_id #мое ли сообщение
        })

    return {'jsonrpc': '2.0', 'result': messages_list, 'id': request_id}


def handle_send_message(params, request_id):
    if 'user_id' not in session:
        return make_error(1, "Требуется авторизация", request_id)

    receiver_id = params.get('receiver_id')
    text = params.get('text', '').strip()

    if not receiver_id:
        return make_error(2, "Не указан получатель", request_id)

    if not text:
        return make_error(2, "Сообщение не может быть пустым", request_id)

    sender_id = session['user_id']

    conn, cur = db_connect()
    cur.execute(
        "INSERT INTO messages (sender_id, receiver_id, text) VALUES (%s, %s, %s) RETURNING id",
        (sender_id, receiver_id, text)
    )
    message_id = cur.fetchone()['id']
    db_close(conn, cur)

    return {'jsonrpc': '2.0', 'result': {'success': True, 'message_id': message_id}, 'id': request_id}


def handle_delete_message(params, request_id):
    if 'user_id' not in session:
        return make_error(1, "Требуется авторизация", request_id)

    #получаем id сообщения
    message_id = params.get('message_id')
    user_id = session['user_id']

    conn, cur = db_connect()
    cur.execute(
        "SELECT sender_id, receiver_id FROM messages WHERE id = %s",
        (message_id,)
    )
    msg = cur.fetchone()

    if not msg:
        db_close(conn, cur)
        return make_error(3, "Сообщение не найдено", request_id)

    if msg['sender_id'] == user_id:
        cur.execute("UPDATE messages SET is_deleted_sender = TRUE WHERE id = %s", (message_id,))
    elif msg['receiver_id'] == user_id:
        cur.execute("UPDATE messages SET is_deleted_receiver = TRUE WHERE id = %s", (message_id,))
    else:
        db_close(conn, cur)
        return make_error(2, "У вас нет прав на удаление этого сообщения", request_id)

    db_close(conn, cur)
    return {'jsonrpc': '2.0', 'result': {'success': True}, 'id': request_id}


def handle_delete_user(params, request_id):
    if session.get('login') != ADMIN_LOGIN:
        return make_error(1, "Требуются права администратора", request_id)

    user_id = params.get('user_id')
    if not user_id:
        return make_error(2, "Не указан ID пользователя", request_id)

    conn, cur = db_connect()
    cur.execute("SELECT login FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()

    if user and user['login'] == ADMIN_LOGIN:
        db_close(conn, cur)
        return make_error(2, "Нельзя удалить администратора", request_id)

    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    cur.execute("UPDATE messages SET is_deleted_sender = TRUE WHERE sender_id = %s", (user_id,))
    cur.execute("UPDATE messages SET is_deleted_receiver = TRUE WHERE receiver_id = %s", (user_id,))

    db_close(conn, cur)
    return {'jsonrpc': '2.0', 'result': {'success': True}, 'id': request_id}
