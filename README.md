# Foodgram (Anton Basalaev diplom)


[![Django-app workflow](https://github.com/AnthonyBass/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/AnthonyBass/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
## Адрес проекта:
http://130.193.43.108/

## Данные для входа в admin:
Логин: admin
Пароль: Anton12345

## Эндпоинты для работы через API:
Описаны по адресу: http://130.193.43.108/api/docs/


## Инструкция для работы с проектом в качестве разработчика

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


## Используемые технологии

- Django 2.2.16
- Django-rest-framework 3.12.4
- Simplejwt 5.2.0
- Git Actions
- Docker
- Yandex Cloud

## Автор

- [AnthonyBass](https://github.com/AnthonyBass)