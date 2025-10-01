from flask import Blueprint, url_for, request, redirect, abort, render_template

lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a')
def a1():
    return 'без слеша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слешем'


flower_list = [
    {'name': 'Bud', 'price': 100},
    {'name': 'Старый мельник', 'price': 60},
    {'name': 'Essa', 'price': 70},
    {'name': 'Krone', 'price': 200}
]


# Страница с ID
@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower = flower_list[flower_id] 
        return render_template(
            'beer.html',
            flower_name=flower['name'],  
            flower_price=flower['price'], 
            flower_id=flower_id,
            total_count=len(flower_list)
        )


# Добавление нового пива   
@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flower_list.lab2end({'name': name, 'price': price})
    return render_template('add.html', 
                         name=name, 
                         price=price,
                         total_count=len(flower_list))


# Удаление пива по номеру
@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        # Удаляем пиво из списка по индексу
        deleted_beer = flower_list.pop(flower_id)
        # Перенаправляем на страницу со списком
        return redirect(url_for('all_flowers'))
    

# Весь список
@lab2.route('/lab2/flowers')
def all_flowers():
    return render_template(
        'all.html',
        flower_list=flower_list,
        total_count=len(flower_list)
    )


@lab2.route('/lab2/add_flower/')
def add_flower_empty():
    name = request.args.get('name')
    price = request.args.get('price', type=int)

    if not name or price is None:
        return '''
        <!doctype html>
        <html>
            <head><title>Ошибка 400</title></head>
            <body>
                <h1>Ошибка 400</h1>
                <p>Вы не задали название или цену пива</p>
                <a href="/lab2/flowers">Вернуться к списку</a>
            </body>
        </html>
        ''', 400

    flower_list.lab2end({'name': name, 'price': price})
    return redirect(url_for('all_flowers'))


# Очистка списка
@lab2.route('/lab2/clear_flowers')
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
                    <h1>Список пива очищен!</h1>
                    <p>Все бутылки были убраны из коллекции.</p>
                </div>
                <a href="/lab2/flowers" class="btn">Перейти к списку пив</a>
                <a href="/lab2/add_flower/Жигулевское/50" class="btn"> Добавить Жигулевское</a>
                <a href="/lab2/" class="btn">Назад к лабораторной</a>
            </div>
        </body>
    </html>
    '''


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)


# Перенаправление на /lab2/calc/1/1
@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))


# Перенаправление на /lab2/calc/a/1
@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('calc', a=a, b=1))


# Основной обработчик калькулятора
@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    
    operations = {
        'sum': a + b,
        'diff': a - b,
        'mult': a * b,
        'div': a / b if b != 0 else 'деление на ноль',
        'pow': a ** b
    }
    return render_template('calc.html', a=a, b=b, operations=operations)


@lab2.route('/lab2/books')
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


@lab2.route('/lab2/nerves')
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