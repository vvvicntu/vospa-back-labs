from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, jsonify
import hashlib
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
import json
from datetime import datetime

rgz = Blueprint('rgz', __name__)

# Администратор
ADMIN_LOGIN = "vika"
ADMIN_PASSWORD = "111"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
    """Страница регистрации"""
    return render_template('rgz/register.html')

@rgz.route('/rgz/logout')
def logout():
    """Выход из системы"""
    session.clear()
    return redirect('/rgz')

# JSON-RPC API (как в методичке)
@rgz.route('/rgz/api', methods=['POST'])
def api():
    """Обработчик JSON-RPC API (как в методичке)"""
    data = request.json
    
    # Проверяем, что это JSON-RPC 2.0
    if data.get('jsonrpc') != '2.0':
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32600,
                'message': 'Invalid Request'
            },
            'id': data.get('id')
        })
    
    method = data.get('method')
    params = data.get('params', {})
    request_id = data.get('id')
    
    # Обработка методов (как в методичке - через if/elif)
    if method == 'register':
        result = handle_register(params)
    elif method == 'login':
        result = handle_login(params)
    elif method == 'logout':
        result = handle_logout()
    elif method == 'get_users':
        result = handle_get_users()
    elif method == 'get_messages':
        result = handle_get_messages(params)
    elif method == 'send_message':
        result = handle_send_message(params)
    elif method == 'delete_message':
        result = handle_delete_message(params)
    elif method == 'delete_user':
        result = handle_delete_user(params)
    else:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Method not found'
            },
            'id': request_id
        })
    
    return jsonify({
        'jsonrpc': '2.0',
        'result': result,
        'id': request_id
    })

# Обработчики методов
def handle_register(params):
    """Регистрация пользователя"""
    login = params.get('login', '').strip()
    password = params.get('password', '').strip()
    
    if not login or not password:
        raise Exception("Логин и пароль обязательны")
    
    if len(login) < 3:
        raise Exception("Логин должен быть не менее 3 символов")
    
    password_hash = hash_password(password)
    
    conn, cur = db_connect()
    try:
        cur.execute(
            "INSERT INTO users (login, password_hash) VALUES (%s, %s) RETURNING id",
            (login, password_hash)
        )
        user_id = cur.fetchone()['id']
        return {'success': True, 'user_id': user_id}
    except psycopg2.IntegrityError:
        raise Exception("Пользователь с таким логином уже существует")
    finally:
        db_close(conn, cur)

def handle_login(params):
    """Авторизация пользователя"""
    login = params.get('login', '').strip()
    password = params.get('password', '').strip()
    
    password_hash = hash_password(password)
    
    conn, cur = db_connect()
    cur.execute(
        "SELECT id, login FROM users WHERE login = %s AND password_hash = %s",
        (login, password_hash)
    )
    user = cur.fetchone()
    db_close(conn, cur)
    
    if not user:
        raise Exception("Неверный логин или пароль")
    
    # Сохраняем в сессии
    session['user_id'] = user['id']
    session['login'] = user['login']
    
    return {'success': True, 'user': {'id': user['id'], 'login': user['login']}}

def handle_logout():
    """Выход из системы"""
    session.clear()
    return {'success': True}

def handle_get_users():
    """Получение списка пользователей"""
    if 'user_id' not in session:
        raise Exception("Требуется авторизация")
    
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
    
    return users_list

def handle_get_messages(params):
    """Получение сообщений с пользователем"""
    if 'user_id' not in session:
        raise Exception("Требуется авторизация")
    
    user_id = session['user_id']
    other_user_id = params.get('user_id')
    
    if not other_user_id:
        raise Exception("Не указан ID пользователя")
    
    conn, cur = db_connect()
    
    # Получаем сообщения между двумя пользователями
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
            'is_my': msg['sender_id'] == user_id
        })
    
    return messages_list

def handle_send_message(params):
    """Отправка сообщения"""
    if 'user_id' not in session:
        raise Exception("Требуется авторизация")
    
    receiver_id = params.get('receiver_id')
    text = params.get('text', '').strip()
    
    if not receiver_id:
        raise Exception("Не указан получатель")
    
    if not text:
        raise Exception("Сообщение не может быть пустым")
    
    sender_id = session['user_id']
    
    conn, cur = db_connect()
    cur.execute(
        "INSERT INTO messages (sender_id, receiver_id, text) VALUES (%s, %s, %s) RETURNING id",
        (sender_id, receiver_id, text)
    )
    message_id = cur.fetchone()['id']
    db_close(conn, cur)
    
    return {'success': True, 'message_id': message_id}

def handle_delete_message(params):
    """Удаление сообщения"""
    if 'user_id' not in session:
        raise Exception("Требуется авторизация")
    
    message_id = params.get('message_id')
    user_id = session['user_id']
    
    if not message_id:
        raise Exception("Не указан ID сообщения")
    
    conn, cur = db_connect()
    
    # Проверяем, принадлежит ли сообщение пользователю
    cur.execute(
        "SELECT sender_id, receiver_id FROM messages WHERE id = %s",
        (message_id,)
    )
    msg = cur.fetchone()
    
    if not msg:
        raise Exception("Сообщение не найдено")
    
    # Обновляем флаг удаления в зависимости от того, отправитель или получатель
    if msg['sender_id'] == user_id:
        cur.execute(
            "UPDATE messages SET is_deleted_sender = TRUE WHERE id = %s",
            (message_id,)
        )
    elif msg['receiver_id'] == user_id:
        cur.execute(
            "UPDATE messages SET is_deleted_receiver = TRUE WHERE id = %s",
            (message_id,)
        )
    else:
        raise Exception("У вас нет прав на удаление этого сообщения")
    
    db_close(conn, cur)
    return {'success': True}

def handle_delete_user(params):
    """Удаление пользователя (только для администратора)"""
    if session.get('login') != ADMIN_LOGIN:
        raise Exception("Требуются права администратора")
    
    user_id = params.get('user_id')
    
    if not user_id:
        raise Exception("Не указан ID пользователя")
    
    conn, cur = db_connect()
    
    # Проверяем, что не удаляем администратора
    cur.execute("SELECT login FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    
    if user and user['login'] == ADMIN_LOGIN:
        raise Exception("Нельзя удалить администратора")
    
    # Удаляем пользователя
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    
    # Также удаляем все его сообщения (или помечаем как удаленные)
    cur.execute(
        "UPDATE messages SET is_deleted_sender = TRUE WHERE sender_id = %s",
        (user_id,)
    )
    cur.execute(
        "UPDATE messages SET is_deleted_receiver = TRUE WHERE receiver_id = %s",
        (user_id,)
    )
    
    db_close(conn, cur)
    return {'success': True}