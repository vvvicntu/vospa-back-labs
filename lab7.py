from flask import Blueprint, render_template, request, session, current_app, abort

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

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

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films[id]


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
    
    film = request.get_json()
    
    films[id] = film
    return films[id]

