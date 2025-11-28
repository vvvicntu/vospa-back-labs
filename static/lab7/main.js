// Получение списка фильмов  
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(data => data.json())
        .then(films => {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');

                let tdTitleRu = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                tdTitleRu.innerText = films[i].title_ru;

                if (films[i].title && films[i].title !== films[i].title_ru) {
                    tdTitle.innerHTML = `<i>(${films[i].title})</i>`;
                } else {
                    tdTitle.innerText = '';
                }

                tdYear.innerText = films[i].year;

                let editBtn = document.createElement('button');
                editBtn.innerText = 'редактировать';
                editBtn.onclick = () => editFilm(i);

                let delBtn = document.createElement('button');
                delBtn.innerText = 'удалить';
                delBtn.onclick = () => deleteFilm(i);

                tdActions.append(editBtn);
                tdActions.append(delBtn);

                tr.append(tdTitleRu, tdTitle, tdYear, tdActions);
                tbody.append(tr);
            }
        });
}

// Удаление фильма  
function deleteFilm(id) {
    if (!confirm('Удалить этот фильм?')) return;

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(() => fillFilmList());
}

//   Модальное окно  
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

// Добавление фильма  
function addFilm() {
    document.getElementById('id').value = "";
    document.getElementById('title').value = "";
    document.getElementById('title-ru').value = "";
    document.getElementById('year').value = "";
    document.getElementById('description').value = "";

    showModal();
}

// Отправка фильма (POST или PUT)  
function sendFilm() {
    const id = document.getElementById('id').value;

    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: Number(document.getElementById('year').value),
        description: document.getElementById('description').value
    };

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
        body: JSON.stringify(film)
    })
        .then(resp => {
            if (resp.ok) {
                fillFilmList();
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

// Редактирование  
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
