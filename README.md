## Infra_sp2

#### Контейнер для  проекта "api_yamdb":

Данный контейнер содержит приложение "api_yamdb". Он позволяет развернуть пользователю данное приложение незавсимо от операционной системы и локальных настроек. Разворачивание приложения происходит в соответствии с инструкциями дял сборки образов в Dockerfile. 

### Технологии:

Python, Django, Dockerfile, Docker-compose, Docker

### Запуск проекта:

- Скачать образ с Docker Hub:

```
docker pull dkr3d3/infra_sp2:v1.07.2022

```

- Создать и активировать виртуальное окружение:

```
python -m venv venv 

source venv/bin/activate (Mac, Linux)
source venv/scripts/activate (Windows)
```

- Пересобрать контейнеры и активировать их:

```
docker-compose up -d --build 

```

- Выполнить миграции:

```
docker-compose exec web python manage.py migrate

```

- Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

- Собрать статические файлы:

```
docker-compose exec web python manage.py collectstatic --no-input 
```

### Документация к проекту:

После запуска проекта документация доступна по адресу: [http://localhost/redoc/](http://localhost/redoc/). В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.

### Примеры запросов к API:

- Получение списка всех произведений: доступно без токена.

*Запрос:*

```
GET yamdb.com/api/v1/titles/
```

*Пример ответа:*

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

- Добавление нового отзыва к произведению: доступно аутентифицированным пользователям.

*Запрос:*

```
POST yamdb.com/api/v1/titles/{title_id}/reviews/
```

*Содержимое запроса:*

```
{
  "text": "string",
  "score": 1
}
```

*Пример ответа:*

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 10,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

- Добавление комментария к отзыву: доступно аутентифицированным пользователям.

*Запрос:*

```
POST yamdb.com/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

*Содержимое запроса:*

```
{
  "text": "string"
}
```

*Пример ответа:*

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

- Удаление пользователя по имени пользователя (username): доступно Администратору.

*Запрос:*

```
DELETE yamdb.com/api/v1/users/{username}/
```

### Автор:

Copyright © 2022 Dmitry Koroteev. All rights reserved.
