// получение списка фильмов  
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(data => data.json()) // преобразуем
        .then(films => {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = ''; // очищаем старые данные

            // для каждого фильма создаем новую строку таблицы
            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');

                let tdTitleRu = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                // заполняем
                tdTitleRu.innerText = films[i].title_ru;

                // если есть оригинальное название и оно отличается от русского
                if (films[i].title && films[i].title !== films[i].title_ru) {
                    tdTitle.innerHTML = `<i>(${films[i].title})</i>`;
                } else {
                    tdTitle.innerText = '';
                }

                tdYear.innerText = films[i].year;

                let editBtn = document.createElement('button');
                editBtn.innerText = 'редактировать';
                editBtn.onclick = () => editFilm(films[i].id);  // вызывает editFilm

                let delBtn = document.createElement('button');
                delBtn.innerText = 'удалить';
                delBtn.onclick = () => deleteFilm(films[i].id);  // вызывает deleteFilm

                // добавляем кнопки в ячейку действий
                tdActions.append(editBtn);
                tdActions.append(delBtn);

                tr.append(tdTitleRu, tdTitle, tdYear, tdActions);
                tbody.append(tr);
            }
        });
}

// удаление фильма  
function deleteFilm(id) {
    if (!confirm('Удалить этот фильм?')) return;

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(() => fillFilmList()); // после удаления обновляем список
}

// модальное окно  
function showModal() {
    document.querySelector('.modal').style.display = 'block';

    document.getElementById('title-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

// добавление фильма  (очищаем все поля и показываем модальное окно)
function addFilm() {
    document.getElementById('id').value = "";
    document.getElementById('title').value = "";
    document.getElementById('title-ru').value = "";
    document.getElementById('year').value = "";
    document.getElementById('description').value = "";

    showModal();
}

// Отправка фильма (создание или обновление)  
function sendFilm() {
    // получаем ID
    const id = document.getElementById('id').value;

    // данные из формы
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: Number(document.getElementById('year').value),
        description: document.getElementById('description').value
    };

    // определяем URL и метод в зависимости от ID
    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    // сбрасываем ошибки
    document.getElementById('title-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(film) // преобразуем объект в JSON-строку
    })
        .then(resp => {
            if (resp.ok) {
                fillFilmList(); // обновляет таблицу 
                hideModal();
                return {};
            }
            return resp.json();
        })
        .then(errors => {
            document.getElementById('title-error').innerText = errors.title || '';
            document.getElementById('title-ru-error').innerText = errors.title_ru || '';
            document.getElementById('year-error').innerText = errors.year || '';
            document.getElementById('description-error').innerText = errors.description || '';
        });
}

// редактирование  
function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(data => data.json())
        .then(film => {
            document.getElementById('id').value = id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;

            showModal();
        });
}

// инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();
});