// Функция заполнения таблицы фильмов
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';
            
            for(let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');
                let tdTitleRus = document.createElement('td'); 
                let tdTitle = document.createElement('td');   
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                tdTitleRus.innerText = films[i].title_ru;
                
                if (films[i].title && films[i].title !== films[i].title_ru) {
                    tdTitle.innerHTML = `<i>(${films[i].title})</i>`;
                } else {
                    tdTitle.innerText = ''; 
                }
                
                tdYear.innerText = films[i].year;

                // Создаем кнопки действий
                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать';
                editButton.onclick = function() {
                    editFilm(i);
                };

                let delButton = document.createElement('button');
                delButton.innerText = 'удалить';
                delButton.onclick = function() {
                    deleteFilm(i);
                };

                // Добавляем кнопки в ячейку действий
                tdActions.append(editButton);
                tdActions.append(delButton);

                // Добавляем ячейки в строку 
                tr.append(tdTitleRus); 
                tr.append(tdTitle);   
                tr.append(tdYear);
                tr.append(tdActions);

                // Добавляем строку в таблицу
                tbody.append(tr);
            }
        });
}

// Функция удаления фильма
function deleteFilm(id) {
    if(!confirm('Вы точно хотите удалить фильм?')) {
        return;
    }

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList();
        });
}

// Функции для работы с модальным окном
function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

// Функция добавления фильма
function addFilm() {
    // Очистка полей формы
    document.getElementById('id').value = "";
    document.getElementById('title').value = "";
    document.getElementById('title-ru').value = "";
    document.getElementById('year').value = "";
    document.getElementById('description').value = "";
    document.getElementById('description-error').innerText = '';
    showModal();
}

// Функция отправки фильма на сервер
function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };
    
    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    document.getElementById('description-error').innerText = '';

    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        if(errors.description)
            document.getElementById('description-error').innerText = errors.description;
    })
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function (data) {
            return data.json();
        })
        .then(function (film) {
            document.getElementById('id').value = id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            document.getElementById('description-error').innerText = '';
            showModal();
        });
}