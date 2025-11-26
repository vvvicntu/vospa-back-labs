from flask import Blueprint, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

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

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    method = data.get('method')
    request_id = data.get('id')
    
    conn, cur = db_connect()

    try:
        if method == 'info':
            cur.execute("SELECT * FROM offices ORDER BY number::integer;")
            offices = cur.fetchall()
            
            # получаем значения
            offices_data = []
            for office in offices:
                offices_data.append({
                    "number": office["number"], 
                    "tenant": office["tenant"] if office["tenant"] else "", #JavaScript проще обрабатывать "" чем null
                    "price": office["price"]
                })
            
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0', # версия протокола
                'result': offices_data, 
                'id': request_id # копия ID из запроса для сопоставления
            }

        login = session.get('login')
        if not login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': request_id # должен совпадать с ID запроса
            }

        if method == 'total_cost':
            cur.execute("SELECT SUM(price) AS total FROM offices WHERE tenant = %s;", (login,))
            result = cur.fetchone()
            total_cost = result["total"] if result and result["total"] else 0

            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'result': total_cost,
                'id': request_id
            }

        if method == 'booking':
            # преобразуем номер офиса в строку
            office_number = str(data['params'])
            # находит офис по номеру
            cur.execute("SELECT * FROM offices WHERE number = %s;", (office_number,))
            office = cur.fetchone()

            # проверка существования офиса
            if not office:
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 5,
                        'message': 'Office not found'
                    },
                    'id': request_id
                }
            # проверка доступности офиса
            if office["tenant"]:
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 2,
                        'message': 'Already booked'
                    },
                    'id': request_id
                }

            # устанавливаем арендатора
            cur.execute("UPDATE offices SET tenant = %s WHERE number = %s;", (login, office_number))
            db_close(conn, cur)

            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': request_id
            }

        if method == 'cancellation':
            # Преобразуем номер офиса в строку
            office_number = str(data['params'])
            cur.execute("SELECT * FROM offices WHERE number = %s;", (office_number,))
            office = cur.fetchone()

            if not office:
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 5,
                        'message': 'Office not found'
                    },
                    'id': request_id
                }


            if office["tenant"] != login:
                db_close(conn, cur)
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 4,
                        'message': 'You can only cancel your own booking'
                    },
                    'id': request_id
                }

            # выполнение отмены бронирования
            cur.execute("UPDATE offices SET tenant = NULL WHERE number = %s;", (office_number,))
            db_close(conn, cur)

            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': request_id
            }

        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Method not found'
            },
            'id': request_id
        }

    except Exception as e:
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 6,
                'message': f'Database error: {str(e)}'
            },
            'id': request_id
        }