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
                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                // Заполняем ячейки данными
                tdTitle.innerText = films[i].title == films[i].title_ru ? '' : films[i].title;
                tdTitleRus.innerText = films[i].title_ru;
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
                tr.append(tdTitle);
                tr.append(tdTitleRus);
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
    
    // Показ модального окна
    showModal();
}

// Функция отправки фильма на сервер
function sendFilm() {
    // Получение данных из формы
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

    fetch('/lab7/rest-api/films/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(film)
    })
    .then(function() {
        fillFilmList();
        hideModal();
    });
}