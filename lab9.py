from flask import Blueprint, render_template, session, jsonify, request

lab9 = Blueprint('lab9', __name__)

# общее количество подарков
total_gifts = 10

# глобальное состояние коробок (общее для всех пользователей)
opened_boxes = set()

# подарки только для авторизованных
auth_only_gifts = {8, 9, 10}

# уникальные поздравления
congratulations = [
    "с новой годой!",
    "не забывай про сессию!",
    "завтра можешь выспаться!",
    "шаман и мизулина поздравляют тебя с новым годом",
    "макан в армии закурил",
    "хэпи нью э",
    "осталось учится всего 3 семестра",
    "эщкере",
    "лалалала все будет хорошо",
    "подарок от деда мороза ждет тебя под елкой"
]

# фиксированные позиции коробок
gift_positions = [
    {'top': '10%', 'left': '5%'},
    {'top': '5%', 'left': '20%'},
    {'top': '15%', 'left': '35%'},
    {'top': '8%', 'left': '55%'},
    {'top': '12%', 'left': '75%'},
    {'top': '40%', 'left': '10%'},
    {'top': '50%', 'left': '30%'},
    {'top': '45%', 'left': '50%'},
    {'top': '55%', 'left': '70%'},
    {'top': '65%', 'left': '85%'}
]


@lab9.route('/lab9/')
def index():
    # инициализация счётчика подарков в сессии
    if 'opened_count' not in session:
        session['opened_count'] = 0

    return render_template('lab9/lab9.html')


@lab9.route('/lab9/get_gifts_info', methods=['post'])
def get_gifts_info():
    return jsonify({
        'opened_boxes': list(opened_boxes),
        'opened_count': session.get('opened_count', 0),
        'remaining': total_gifts - len(opened_boxes),
        'positions': gift_positions,
        'authorized': 'login' in session
    })


@lab9.route('/lab9/open_gift', methods=['post'])
def open_gift():
    data = request.get_json()
    gift_id = int(data.get('gift_id', 0))

    # проверка корректности id
    if gift_id < 1 or gift_id > total_gifts:
        return jsonify({'error': 'некорректный подарок'})

    # проверка авторизации для закрытых подарков
    if gift_id in auth_only_gifts and 'login' not in session:
        return jsonify({'error': 'этот подарок доступен только авторизованным'})

    # проверка, открыт ли подарок глобально
    if gift_id in opened_boxes:
        return jsonify({'error': 'этот подарок уже забрали'})

    # проверка лимита из сессии
    if session.get('opened_count', 0) >= 3:
        return jsonify({'error': 'можно открыть не более 3 подарков'})

    # открываем подарок
    opened_boxes.add(gift_id)
    session['opened_count'] += 1

    return jsonify({
        'success': True,
        'congratulation': congratulations[gift_id - 1],
        'image': f'c{gift_id}.jpg',
        'opened_count': session['opened_count'],
        'remaining': total_gifts - len(opened_boxes)
    })


@lab9.route('/lab9/reset_gifts', methods=['post'])
def reset_gifts():
    # сброс доступен только авторизованным
    if 'login' not in session:
        return jsonify({'error': 'доступ запрещён'})

    opened_boxes.clear()
    session['opened_count'] = 0

    return jsonify({'success': True})
