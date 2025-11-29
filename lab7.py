from flask import Blueprint, render_template, request, abort, jsonify, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

def db_connect():
    # Подключение к postgres
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='vika_vosp',
            user='vika_vosp',
            password='666'
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
    
@lab7.after_request
def add_utf8_header(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films ORDER BY id")
    films = cur.fetchall()
    db_close(conn, cur)
    
    # Конвертируем в обычный список словарей
    films_list = []
    for film in films:
        films_list.append(dict(film))
    
    return jsonify(films_list)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    
    if not film:
        abort(404)
    
    return jsonify(dict(film))

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    film = cur.fetchone()
    
    if not film:
        db_close(conn, cur)
        abort(404)
    
    cur.execute("DELETE FROM films WHERE id = %s", (id,))
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn, cur = db_connect()
    
    # Проверяем существование фильма
    cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    film_exists = cur.fetchone()
    
    if not film_exists:
        db_close(conn, cur)
        abort(404)

    film = request.get_json() or {}

    # берём значения безопасно и обрезаем пробелы
    title = str(film.get('title', '') or '').strip()
    title_ru = str(film.get('title_ru', '') or '').strip()
    description = str(film.get('description', '') or '').strip()
    year_raw = film.get('year', None)

    errors = {}

    # Проверяем русское название — оно должно быть непустым
    if title_ru == '':
        errors['title_ru'] = 'Заполните русское название'

    # Если original пустой, но есть русское — подставляем
    if title == '' and title_ru != '':
        title = title_ru

    # Проверка года — приводим к int и валидируем
    try:
        year = int(year_raw)
        import datetime
        current_year = datetime.datetime.now().year
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'
    except (TypeError, ValueError):
        errors['year'] = 'Год должен быть числом'

    # Описание
    if description == '':
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    if errors:
        db_close(conn, cur)
        return errors, 400

    # Обновляем фильм в БД
    cur.execute("""
        UPDATE films 
        SET title = %s, title_ru = %s, year = %s, description = %s 
        WHERE id = %s
    """, (title, title_ru, year, description, id))
    
    # Получаем обновленный фильм
    cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    updated_film = cur.fetchone()
    
    db_close(conn, cur)
    return jsonify(dict(updated_film))

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json() or {}

    title = str(film.get('title', '') or '').strip()
    title_ru = str(film.get('title_ru', '') or '').strip()
    description = str(film.get('description', '') or '').strip()
    year_raw = film.get('year', None)

    errors = {}

    # Русское название — обязательно (по методичке)
    if title_ru == '':
        errors['title_ru'] = 'Заполните русское название'

    # Если русское пустое — оригинальное обязательно
    if title_ru == '' and title == '':
        errors['title'] = 'Заполните название на оригинальном языке или русское название'

    # Если original пустой, но есть русское — подставляем
    if title == '' and title_ru != '':
        title = title_ru

    # Проверка года
    try:
        year = int(year_raw)
        import datetime
        current_year = datetime.datetime.now().year
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'
    except (TypeError, ValueError):
        errors['year'] = 'Год должен быть числом'

    # Описание
    if description == '':
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    if errors:
        return errors, 400

    conn, cur = db_connect()
    
    # Добавляем фильм в БД
    cur.execute("""
        INSERT INTO films (title, title_ru, year, description) 
        VALUES (%s, %s, %s, %s) 
        RETURNING id
    """, (title, title_ru, year, description))
    
    new_id = cur.fetchone()['id']
    db_close(conn, cur)
    
    return jsonify(new_id)

