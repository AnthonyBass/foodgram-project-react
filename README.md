# Foodgram (Anton Basalaev diplom)


[![Django-app workflow](https://github.com/AnthonyBass/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/AnthonyBass/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

## Описание проекта
Foodgram - это продуктовый помошник для возможности делиться рецептами своих любимых блюд, а также для того чтобы упростить процесс создания списка покупок, если вы решили сготовить что-то, что вам приглянулось.
Функции, доступные зарегистрированному пользователю:
- Создание рецепта, с указанием конкретных ингридиентов, их количества и добавлением фото вашего шедевра.
- Подписка на полюбившихся авторов.
- Возможность сортировки по тегам (завтрак, обед, ужин) на главной странице со всеми представленными рецептами
- Добавление рецепта в избранное. Как чужого, так и своего.
- Добавления рецепта в список покупок с возможностью получения списка необходимых ингредиентов в pdf формате, чтобы упростить поход за продуктами
## Адрес проекта:
http://130.193.43.108/

## Данные для входа в admin:
Логин: admin
Пароль: Anton12345

## Эндпоинты для работы через API:
auth - Регистрация пользователей и выдача токенов
auth/signup/ - Регистрация нового пользователя
auth/token/ - Получение JWT-токена
recipes/ - Список всех рецептов или получение информации о конкретном рецепте
recipes/create/ - создание рецепта
tags/ - Список тегов
subscriptions/ - Список рецептов, добавленных в избранное
cart/ - Список покупок
user/{user_id}/ - список всех рецептов конкретного автора

## Инструкция для запуска проекта

##### Скачать репозиторий на локальную машину для разработки
```
git clone https://github.com/AnthonyBass/foodgram-project-react.git
```

##### Перейти в папку проекта
```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

##### Выпонить push в удаленный репозиторий после внесения изменений

```
git add .
```

```
git commit -m 'comment'
```

```
git push
```
##### С помощью технологии Git Actions код будет проверен на соответсвие стандартов PEP8, создадутся образы backend и фронтенд, будут размещены на Docker Hub и далее контейнеры будут заново развернуты на сервере с внесенными изменениями.

## Примеры запросов к API

Ниже придставлены только несколько примеров для ознакомления,
ознакомиться с полным списком эндпоинтов можно по адресу: http://130.193.43.108/api/docs/

### Регистрация нового пользователя

```
POST http://130.193.43.108/api/users/
```

Request Body schema

```
{
    "email" : string,
    "username": string,
    "first_name": string,
    "last_name": string,
    "password": string
}
```

### Получение списка всех рецептов

```
GET http://130.193.43.108/api/recipes/
```

Authorizations: jwt-token

### Добавление нового рецепта

```
POST http://130.193.43.108/api/recipes/
```

Authorizations: jwt-token

Request Body schema

```
{
    "ingredients": [
        {
            "id": id,
            "amount": integer
        }
    ],
    "tags": [
        id (array)
    ],
    "image": BASE64 string,
    "name": "string" <= 200 characters,
    "text": "string",
    "cooking_time": integer >= 1
}
```

### Полуение списка рецептов конкретного автора по id

```
GET http://130.193.43.108/api/users/{id}/
```

PATH parameters

```
{
    id (required): integer (ID автора))
}
```

## Используемые технологии

- Python 3.7
- Django 2.2.16
- Django-rest-framework 3.12.4
- Simplejwt 5.2.0
- Git
- Git Actions
- NGINX
- Gunicorn
- React
- PostrgersSQL
- Docker
- Docker Hub
- Yandex Cloud

## Автор
Студент образовательной программы Яндекс Практикум, специальность "Python backend разработчик"
- [AnthonyBass](https://github.com/AnthonyBass)
