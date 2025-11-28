from flask import Blueprint, render_template, request, abort, jsonify

lab7 = Blueprint('lab7', __name__)

films = [
    {
        "title": "Domohoziayki",
        "title_ru": "Отчаянные домохозяйки",
        "year": 2004,
        "description": "Сериал «Отчаянные домохозяйки» \
         рассказывает о жизни нескольких женщин, живущих на улице Вистерия Лейн, \
         и затрагивает важные проблемы, с которыми они сталкиваются в повседневной \
         жизни. Сюжет начинается с самоубийства Мэри Элис Янг, что шокирует её подруг, \
         и вскоре раскрывает их неидеальные жизни и тайны."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля",
        "year": 1999,
        "description": "Фильм рассказывает историю Пола Эджкомба, надзирателя \
        в тюрьме смертников, и его встречу с Джоном Коффи, необычным заключенным, \
        обладающим сверхъестественными способностями исцеления. Действие разворачивается \
        в 1930-х годах и показывает, как чудеса и несправедливость переплетаются \
        на пороге смерти."
    },
    {
        "title": "The Human Centipede",
        "title_ru": "Человеческая многоножка",
        "year": 2009,
        "description": "Шокирующий фильм ужасов о безумном хирурге докторе Хайтере, \
        который похищает людей и сшивает их вместе в единую пищеварительную систему - \
        создавая 'человеческую многоножку'. Жертвы соединены рот-к-анусу, образуя \
        живую цепь, что приводит к ужасающим физическим и психологическим мучениям. \
        Фильм стал одним из самых противоречивых и шокирующих в истории жанра ужасов."
    },
    {
        "title": "Green Elephant",
        "title_ru": "Зеленый слоник",
        "year": 1999,
        "description": "Культовый российский фильм ужасов, действие которого \
        происходит в закрытом военном учреждении. Два заключенных офицера \
        оказываются в замкнутом пространстве, где сталкиваются с безумием, \
        жестокостью и абсурдом системы."
    },
    {
        "title": "Alice in Wonderland",
        "title_ru": "Алиса в стране чудес с Аней Пересильд",
        "year": 2025,
        "description": "Полный кринж."
    }
]

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
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
    
    year = int(year_raw)
    import datetime
    current_year = datetime.datetime.now().year
    if year < 1895 or year > current_year:
        errors['year'] = f'Год должен быть от 1895 до {current_year}'

    # Описание
    if description == '':
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    if errors:
        return errors, 400

    # Обновляем фильм
    films[id] = {
        'title': title,
        'title_ru': title_ru,
        'year': year,
        'description': description
    }

    return jsonify(films[id])


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json() or {}

    title = str(film.get('title', '') or '').strip()
    title_ru = str(film.get('title_ru', '') or '').strip()
    description = str(film.get('description', '') or '').strip()
    year_raw = film.get('year', None)

    errors = {}

    # Русское название — обязателено (по методичке)
    if title_ru == '':
        errors['title_ru'] = 'Заполните русское название'

    # Если русское пустое — оригинальное обязателено
    if title_ru == '' and title == '':
        errors['title'] = 'Заполните название на оригинальном языке или русское название'

    # Если original пустой, но есть русское — подставляем
    if title == '' and title_ru != '':
        title = title_ru

    # Проверка года
    try:
        year = int(year_raw)
    except (TypeError, ValueError):
        errors['year'] = 'Год должен быть числом'
    else:
        import datetime
        current_year = datetime.datetime.now().year
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'

    # Описание
    if description == '':
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    if errors:
        return errors, 400

    new_film = {
        'title': title,
        'title_ru': title_ru,
        'year': year,
        'description': description
    }

    films.append(new_film)
    return jsonify(len(films) - 1)