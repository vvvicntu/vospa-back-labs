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
    {'login': 'macan', 'password': '666'},
    {'login': 'vospa', 'password': '345'},
    {'login': 'miu', 'password': '444'},
    {'login': 'laba', 'password': '100'}
]

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():

    # Если страница запрашивается методом GET, то пользователь 
    # никаких данных ещё не передавал — вернём страницу с формой
    if request.method == 'GET':
        # проверка авторизации
        if 'login' in session:
            authorized = True
            login = session['login']
        else:
            authorized = False 
            login = ''
        return render_template("lab4/login.html", authorized=authorized, login=login)

    login = request.form.get('login')
    password = request.form.get('password')

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login 
            return redirect('/lab4/login')
    
    error = 'Неверные логин или пароль!'
    return render_template('lab4/login.html', error=error, authorized=False)


@lab4.route('/lab4/logout',methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')