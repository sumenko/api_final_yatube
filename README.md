# Спринт 10. Финальный проект по API
#### Общая информация

Проект сделан на **Python 3.7** с использованием [django](https://www.djangoproject.com/) и расширения [Django REST framework](https://www.django-rest-framework.org/)

 Проект предоставляет доступ к API проекта yatube и позволяет:

- публикацию, редактирование постов авторизованным пользователям
- добавлять посты в сообщества
- добавлять и редактировать комментарии
- реализована возможность подписки пользователей друг на друга
- аутентифицировать пользователей для получения токенов

Ответы сервера в формате `json`. Документация к запросам доступна в формате redoc по адресу `/redoc`(только в debug mode: `yatube_api/settings.py`, `DEBUG = True`)

#### Установка

В папке хранения проектов выполнить

```bash
git clone https://github.com/sumenko/api_final_yatube.git
```

Установить зависимости

```bash
pip -r requirements.txt
```

Перед запуском создать и активировать окружение

```bash
python -m venv venv
source venv/scripts/activate
```

Запуск сервера

```bash
python manage.py runserver [PORT]
```

Где `PORT`- номер порта. Если не установлен, по умолчанию 8000

Аутентификация через JWT-token через POST запрос [localhost:8000/api/v1/token/](https://www.djangoproject.com/) в теле запроса передать параметры `username` и `password`

#### Внимание

`SECRET_KEY` - в yatube_api/settings.py необходимо вынести в окружение сервера



#### Примеры запросов

Получить все посты

```
[GET] localhost:8000/api/v1/posts/
```

Ответ

```json
[
    {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
    }
]
```

Опубликовать пост 

```
localhost:8000/api/v1/posts/
```

Ответ - содержимое объекта поста

```json
[
    {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
    }
]
```

Больше примеров в формате redoc: [localhost:8000/redoc](https://www.djangoproject.com/)



Автор: Суменко В.А.

2021