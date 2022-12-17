<a id="anchor"></a>
# CI и CD проекта api_yamdb
![example workflow](https://github.com/ase77/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Описание:
Настройка Continuous Integration и Continuous Deployment для приложения api_yamdb.

Проект YaMDb собирает отзывы пользователей на произведения по категориям: «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр из списка предустановленных.
Пользователи оставляют к произведениям отзывы, оставляют комментарии к отзывам и ставят произведению оценку, из пользовательских оценок формируется рейтинг.
## Используемые технологии:
![https://www.python.org/](https://camo.githubusercontent.com/55e471c50835a4e4b084eafa9a82fd49aa1288bd148ae4c3e276e405db6a7f75/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d507974686f6e2d3436343634363f7374796c653d666c6174266c6f676f3d507974686f6e266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://www.djangoproject.com/](https://camo.githubusercontent.com/7192b5cd049ca04bd028774695bcf790c850e6f3b8fcfd4022daa79d0f183daf/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d446a616e676f2d3436343634363f7374796c653d666c6174266c6f676f3d446a616e676f266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://www.postgresql.org/](https://camo.githubusercontent.com/35940080ac4c53d288ec41ca11367e98b56e34fb1007ec9e8178c0e032407d88/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d506f737467726553514c2d3436343634363f7374796c653d666c6174266c6f676f3d506f737467726553514c266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://nginx.org/ru/](https://camo.githubusercontent.com/6ebc0f3d416cdfd5e6af91c8003745f8b49c3f30741bb5303abe11bc1f93cf27/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d4e47494e582d3436343634363f7374796c653d666c6174266c6f676f3d4e47494e58266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://gunicorn.org/](https://camo.githubusercontent.com/d637e79276a56dfb4531ddc67429ff52af04becc78052d88a6a14ccc08c1c5cd/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d67756e69636f726e2d3436343634363f7374796c653d666c6174266c6f676f3d67756e69636f726e266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://www.docker.com/](https://camo.githubusercontent.com/6e928d8c13895b010c64a37fcc6a1adfa0d5e774146eae485cf8df28abc03093/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d446f636b65722d3436343634363f7374796c653d666c6174266c6f676f3d446f636b6572266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://github.com/features/actions](https://camo.githubusercontent.com/d9698cafacdfcb0e1d80d16ecdbcdc8c58c6fb59914d3cbf5e439f0881157814/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d476974487562253230416374696f6e732d3436343634363f7374796c653d666c6174266c6f676f3d476974487562253230616374696f6e73266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://cloud.yandex.ru/](https://camo.githubusercontent.com/a571043856303345577ffa9977e04a90df121767ecff17fd6d080bb304d9854d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d59616e6465782e436c6f75642d3436343634363f7374796c653d666c6174266c6f676f3d59616e6465782e436c6f7564266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
## Workflow:
  * `tests` - проверка кода на соответствие стандарту PEP8 и запуск pytest;
  * `build_and_push_to_docker_hub` - сборка и доставка докер-образа для контейнера web на Docker Hub;
  * `deploy` - автоматический деплой проекта на боевой сервер;
  * `send_message` - отправка уведомления в Telegram о том, что процесс деплоя успешно завершился.
## Подготовьте сервер:
1. Войдите на свой удаленный сервер в облаке.
2. Остановите службу `nginx`:
```
sudo systemctl stop nginx 
```
3. Установите `docker`:
```
sudo apt install docker.io 
```
4. Установите docker-compose, с этим вам поможет официальная [документация](https://docs.docker.com/compose/install/).
5. Скопируйте файлы `docker-compose.yaml` и `nginx/default.conf` из вашего проекта на сервер 
в `home/<ваш_username>/docker-compose.yaml` и `home/<ваш_username>/nginx/default.conf` соответственно:
```
scp docker-compose.yaml <username>@<host>/home/<username>/
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```
6. В репозитории на Гитхабе добавьте данные в `Settings -> Secrets -> Actions -> New repository secret`:
```
DOCKER_USERNAME - ваш username на dockerhub
DOCKER_PASSWORD - ваш пароль на dockerhub
USER - имя пользователя для подключения к серверу
HOST - IP-адрес вашего сервера
SSH_KEY - скопируйте приватный ключ с компьютера, имеющего доступ к боевому серверу (cat ~/.ssh/id_rsa)
PASSPHRASE - если при создании ssh-ключа вы использовали фразу-пароль, то сохраните её в эту переменную
DB_ENGINE - django.db.backends.postgresql
DB_NAME - postgres
POSTGRES_USER - postgres
POSTGRES_PASSWORD - postgres
DB_HOST - db
DB_PORT - 5432
TELEGRAM_TO - ID своего телеграм-аккаунта (узнать свой ID можно у бота @userinfobot)
TELEGRAM_TOKEN - токен вашего бота (получить токен можно у бота @BotFather)
```
## После деплоя:
1. Выполните миграции в контейнере `web`:
```
docker-compose exec web python manage.py migrate
```
2. Создайте суперпользователя в контейнере `web`:
```
docker-compose exec web python manage.py createsuperuser
```
3. Соберите статику в контейнере `web`:
```
docker-compose exec web python manage.py collectstatic --no-input
```
4. Загрузите начальные данные из файлов `csv` в базу данных:
```
docker-compose exec web python manage.py load_csv
```
___
Докуметация к проекту будет доступна по адресу:
```
http://<host>/redoc/
```
Админка проекта будет доступна по адресу:
```
http://<host>/admin/
```
## Примеры запросов к API:
## Auth:

Регистрация нового пользователя, получение кода подтверждения на переданный `email`:

`POST http://<host>/api/v1/auth/signup/`
```
{
    "email": "string",
    "username": "string"
}
```

Получение JWT-токена в обмен на `username` и `confirmation_code`:

`POST http://<host>/api/v1/auth/token/`
```
{
    "username": "string",
    "confirmation_code": "string"
}
```

## Categories:

Получение списка всех категорий:

`GET http://<host>/api/v1/categories/`
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "name": "string",
                "slug": "string"
            }
        ]
    }
]
```

Добавление новой категории. Поле `slug` каждой категории должно быть уникальным:

`POST http://<host>/api/v1/categories/`
```
{
    "name": "string",
    "slug": "string"
}
```

Удаление категории:

`DELETE http://<host>/api/v1/categories/{slug}/`

## Genres:

Получение списка всех жанров:

`GET http://<host>/api/v1/genres/`
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "name": "string",
                "slug": "string"
            }
        ]
    }
]
```

Добавление жанра. Поле `slug` каждого жанра должно быть уникальным:

`POST http://<host>/api/v1/genres/`
```
{
    "name": "string",
    "slug": "string"
}
```

Удаление жанра:

`DELETE http://<host>/api/v1/genres/{slug}/`

## Titles:

Получение списка всех произведений:

`GET http://<host>/api/v1/titles/`
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "id": 0,
                "name": "string",
                "year": 0,
                "rating": 0,
                "description": "string",
                "genre": [
                    {
                        "name": "string",
                        "slug": "string"
                    }
                ],
                "category": {
                    "name": "string",
                    "slug": "string"
                }
            }
        ]
    }
]
```

Получение информации о произведении:

`GET http://<host>/api/v1/titles/{titles_id}/`
```
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
            "name": "string",
            "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```

Добавление произведения (требуется указать уже существующие категорию и жанр):

`POST http://<host>/api/v1/titles/`
```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```

Частичное обновление информации о произведении:

`PATCH http://<host>/api/v1/titles/{titles_id}/`
```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```

Удаление произведения:

`DELETE http://<host>/api/v1/titles/{titles_id}/`

## Reviews:

Получение списка всех отзывов:

`GET http://<host>/api/v1/titles/{title_id}/reviews/`
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "id": 0,
                "text": "string",
                "author": "string",
                "score": 1,
                "pub_date": "2019-08-24T14:15:22Z"
            }
        ]
    }
]
```

Полуение отзыва по id:

`GET http://<host>/api/v1/titles/{title_id}/reviews/{review_id}/`
```
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
}
```

Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение:

`POST http://<host>/api/v1/titles/{title_id}/reviews/`
```
{
    "text": "string",
    "score": 1
}
```

Частичное обновление отзыва по id:

`PATCH http://<host>/api/v1/titles/{title_id}/reviews/{review_id}/`
```
{
    "text": "string",
    "score": 1
}
```

Удаление отзыва по id:

`DELETE http://<host>/api/v1/titles/{title_id}/reviews/{review_id}/`

## Comments:

Получение списка всех комментариев к отзыву:

`GET http://<host>/api/v1/titles/{title_id}/reviews/{review_id}/comments/`
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "id": 0,
                "text": "string",
                "author": "string",
                "pub_date": "2019-08-24T14:15:22Z"
            }
        ]
    }
]
```

Получение комментария к отзыву по id:

`GET http://<host>/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`
```
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"
}
```

Добавление комментария к отзыву:

`POST http://<host>/api/v1/titles/{title_id}/reviews/{review_id}/comments/`
```
{
    "text": "string"
}
```

Частичное обновление комментария к отзыву по id:

`PATCH http://<host>/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`
```
{
    "text": "string"
}
```

Удаление комментария к отзыву по id:

`DELETE http://<host>/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`

## Users:

Получение данных своей учетной записи:

`GET http://<host>/api/v1/users/me/`
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

Изменение данных своей учетной записи (поля `email` и `username` должны быть уникальными):

`PATCH http://<host>/api/v1/users/me/`
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string"
}
```

Получение списка всех пользователей:

`GET http://<host>/api/v1/users/`
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "username": "string",
                "email": "user@example.com",
                "first_name": "string",
                "last_name": "string",
                "bio": "string",
                "role": "user",
            }
        ]
    }
]
```

Получение пользователя по `username`:

`GET http://<host>/api/v1/users/{username}/`
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

Добавление пользователя (поля `email` и `username` должны быть уникальными):

`POST http://<host>/api/v1/users/`
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

Изменение данных пользователя по `username`:

`PATCH http://<host>/api/v1/users/{username}/`
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

Удаление пользователя по `username`:

`DELETE http://<host>/api/v1/users/{username}/`

### Автор проекта:

Моторин А.В.

[__В начало__](#anchor) :point_up:
