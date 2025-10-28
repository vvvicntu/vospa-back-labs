from flask import Blueprint, render_template, request, session, redirect
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')
 

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1') # получение post-данных
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')
    
    if x2 == '0':
        return render_template('lab4/div.html', error='Деление на ноль невозможно!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2 
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    # если какое-либо из полей пустое, считаем что ввели 0
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mult', methods = ['POST'])
def mult():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    # если какое-либо из полей пустое, считаем что ввели 0
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    
    result = x1 * x2
    return render_template('lab4/mult.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/vichit', methods = ['POST'])
def vichit():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/vichit.html', error = 'Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/vichit.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/step', methods = ['POST'])
def step():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/step.html', error = 'Оба поля должны быть заполнены!')
    
    if x1 == '0' and x2 == '0':
        return render_template('lab4/step.html', error = 'Числа не могут быть равны нулю!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    return render_template('lab4/step.html', x1=x1, x2=x2, result=result)

tree_count = 0


@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count

    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')
    
    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1 
    
    return redirect('/lab4/tree')


users = [
    {'login': 'macan', 'password': '666', 'name': 'Макан'},
    {'login': 'vospa', 'password': '345', 'name': 'Воспа'},
    {'login': 'miu', 'password': '444', 'name': 'Миу Миу'},
    {'login': 'laba', 'password': '100', 'name': 'Поставьте 5 пж'}
]

# Страница регистрации
@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    # Показываем форму регистрации
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    # Получаем данные из формы
    login = request.form.get('login')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    name = request.form.get('name')
    
    # Проверка заполнения полей
    if not all([login, password, confirm_password, name]):
        return render_template('lab4/register.html', error='Все поля должны быть заполнены')
    
    # Проверка совпадения паролей
    if password != confirm_password:
        return render_template('lab4/register.html', error='Пароли не совпадают')
    
    # Проверка уникальности логина
    if any(user['login'] == login for user in users):
        return render_template('lab4/register.html', error='Логин уже занят')
    
    # Добавляем нового пользователя
    users.append({
        'login': login,
        'password': password,
        'name': name
    })
    
    # Автовход после регистрации
    session['login'] = login
    return redirect('/lab4/login')


# Страница списка пользователей
@lab4.route('/lab4/users')
def users_list():
    # Проверяем авторизацию
    if 'login' not in session:
        return redirect('/lab4/login')
    
    # Получаем текущего пользователя
    current_user = next((user for user in users if user['login'] == session['login']), None)
    
    return render_template('lab4/users.html', 
                         users=users, 
                         current_user=current_user)


# Редактирование профиля
@lab4.route('/lab4/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    # Находим текущего пользователя
    current_user = next((user for user in users if user['login'] == session['login']), None)
    
    if request.method == 'GET':
        return render_template('lab4/edit_profile.html', user=current_user)
    
    # Получаем данные из формы
    new_login = request.form.get('login')
    new_name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    # Проверяем обязательные поля
    if not new_login or not new_name:
        return render_template('lab4/edit_profile.html', 
                             user=current_user,
                             error='Заполните все поля')
    
    # Проверяем уникальность логина (если изменился)
    if new_login != current_user['login'] and any(user['login'] == new_login for user in users):
        return render_template('lab4/edit_profile.html',
                             user=current_user,
                             error='Логин уже занят')
    
    # Обновляем данные пользователя
    user_index = next(i for i, user in enumerate(users) if user['login'] == current_user['login'])
    users[user_index]['login'] = new_login
    users[user_index]['name'] = new_name
    
    # Обновляем пароль только если введен новый
    if password:
        if password != confirm_password:
            return render_template('lab4/edit_profile.html',
                                 user=current_user,
                                 error='Пароли не совпадают')
        users[user_index]['password'] = password
    
    # Обновляем сессию если логин изменился
    session['login'] = new_login
    
    return redirect('/lab4/users')


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            # Находим пользователя для получения имени
            user_data = next((user for user in users if user['login'] == session['login']), None)
            name = user_data['name'] if user_data else session['login']
            return render_template("lab4/login.html", authorized=True, name=name)
        else:
            return render_template("lab4/login.html", authorized=False, name='')

    login = request.form.get('login')
    password = request.form.get('password')
    
    # Проверка на пустые поля
    if not login:
        return render_template('lab4/login.html', error='Не введён логин', 
                             login_value=login, authorized=False)
    
    if not password:
        return render_template('lab4/login.html', error='Не введён пароль', 
                             login_value=login, authorized=False)

    # Проверяем логин и пароль
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login 
            return redirect('/lab4/login')
    
    error = 'Неверные логин или пароль!'
    return render_template('lab4/login.html', error=error, login_value=login, authorized=False)


@lab4.route('/lab4/logout',methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    temperature = request.form.get('temperature')
    
    # Проверка на пустое значение
    if not temperature:
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    try:
        temp = int(temperature)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: температура должна быть числом')
    
    # Проверка диапазонов температуры
    if temp < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    
    if temp > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    
    # Определение количества снежинок
    snowflakes = 0
    if -12 <= temp <= -9:
        snowflakes = 3
    elif -8 <= temp <= -5:
        snowflakes = 2
    elif -4 <= temp <= -1:
        snowflakes = 1
    
    return render_template('lab4/fridge.html', 
                         temperature=temp, 
                         snowflakes=snowflakes,
                         success=f'Установлена температура: {temp}°C')


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    if request.method == 'GET':
        return render_template('lab4/grain.html')
    
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    # Цены за тонну
    prices = {
        'barley': 12000,   # ячмень
        'oats': 8500,      # овёс
        'wheat': 9000,     # пшеница
        'rye': 15000       # рожь
    }
    
    # Названия зерна для отображения
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    # Проверка на выбор типа зерна
    if not grain_type:
        return render_template('lab4/grain.html', error='Выберите тип зерна')
    
    # Проверка веса
    if not weight:
        return render_template('lab4/grain.html', error='Введите вес заказа')
    
    try:
        weight_val = float(weight)
    except ValueError:
        return render_template('lab4/grain.html', error='Вес должен быть числом')
    
    if weight_val <= 0:
        return render_template('lab4/grain.html', error='Вес должен быть положительным числом')
    
    # Проверка наличия больших объемов
    if weight_val > 100:
        return render_template('lab4/grain.html', 
                             error='Извините, такого объёма сейчас нет в наличии')
    
    # Расчет стоимости
    price_per_ton = prices[grain_type]
    total = weight_val * price_per_ton
    
    # Применение скидки
    discount = 0
    discount_applied = False
    
    if weight_val > 10:
        discount = total * 0.10  # 10% скидка
        total -= discount
        discount_applied = True # Отметка что скидка применена
    
    grain_name = grain_names[grain_type]
    
    return render_template('lab4/grain.html',
                         success=True,
                         grain_type=grain_name,
                         weight=weight_val,
                         total=total,
                         discount=discount,
                         discount_applied=discount_applied,
                         original_total=weight_val * price_per_ton if discount_applied else None)


