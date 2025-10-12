from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    
    if not name:
        name = "aнонимус"
    
    if not age:
        age = "неизвестно"
    
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'My God', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'red')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    
    errors = {}
    if user == '':
        errors['user'] = 'Заполните поле!'
    if age == '':
        errors['age'] = 'Напишите возраст!'

    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 90


    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    # Получаем параметры из GET-запроса
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_weight = request.args.get('font_weight')
    
    # Если есть какие-то параметры - устанавливаем куки и делаем редирект
    if color or bg_color or font_size or font_weight:
        resp = make_response(redirect('/lab3/settings'))
        
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_weight:
            resp.set_cookie('font_weight', font_weight)
            
        return resp
    
    # Если параметров нет - показываем форму с текущими значениями из кук
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_weight = request.cookies.get('font_weight')
    
    resp = make_response(render_template(
        'lab3/settings.html', 
        color=color,
        bg_color=bg_color,
        font_size=font_size,
        font_weight=font_weight
    ))
    return resp


@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    
    # Получаем данные из формы
    fio = request.args.get('fio')
    polka = request.args.get('polka')
    belyo = request.args.get('belyo')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    if fio == '':
        errors['fio'] = 'Заполните поле!'
    if polka == '':
        errors['polka'] = 'Выберите полку!'
    if belyo == '':
        errors['belyo'] = 'Выберите вариант!'
    if luggage == '':
        errors['luggage'] = 'Выберите вариант!'
    if age == '':
        errors['age'] = 'Заполните возраст!'
    elif age:
        try:
            age_int = int(age)
            if age_int < 1 or age_int > 120:
                errors['age'] = 'Возраст должен быть от 1 до 120 лет!'
        except ValueError:
            errors['age'] = 'Возраст должен быть числом!'
    if departure == '':
        errors['departure'] = 'Заполните поле!'
    if destination == '':
        errors['destination'] = 'Заполните поле!'
    if date == '':
        errors['date'] = 'Заполните дату!'
    
    # Если есть ошибки, показываем форму с ошибками
    if errors:
        return render_template('lab3/ticket_form.html', 
                            fio=fio or '',
                            polka=polka or '',
                            belyo=belyo or '',
                            luggage=luggage or '',
                            age=age or '',
                            departure=departure or '',
                            destination=destination or '',
                            date=date or '',
                            insurance=insurance or 'no',
                            errors=errors)
    

    if fio and polka and belyo and luggage and age and departure and destination and date:
        # Расчёт стоимости билета
        age_int = int(age)
        
        if age_int < 18:
            price = 700  
            ticket_type = "Детский билет"
        else:
            price = 1000 
            ticket_type = "Взрослый билет"
        
        # Доплаты
        if polka in ['lower', 'lower-side']:
            price += 100  
        
        if belyo == 'yes':
            price += 75  # Бельё
        
        if luggage == 'yes':
            price += 250  # Багаж
        
        if insurance == 'yes':
            price += 150  # Страховка
        
        return render_template('lab3/ticket_result.html',
                             fio=fio,
                             polka=polka,
                             belyo=belyo,
                             luggage=luggage,
                             age=age,
                             departure=departure,
                             destination=destination,
                             date=date,
                             insurance=insurance,
                             price=price,
                             ticket_type=ticket_type)
    
    # Если форма не отправлена, показываем пустую форму
    return render_template('lab3/ticket_form.html', 
                         fio='',
                         polka='',
                         belyo='',
                         luggage='',
                         age='',
                         departure='',
                         destination='',
                         date='',
                         insurance='no',
                         errors={})


@lab3.route('/lab3/del_settings')
def del_settings():
    # Удаляет все куки, установленные на странице 
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_weight')
    return resp
