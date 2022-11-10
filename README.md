# praktikum_new_diplom


## Установка проекта локально
* Загрузите ингредиенты:
```bash
docker-compose exec web python manage.py load_ingredients
```
* Загрузите теги:
```bash
docker-compose exec web python manage.py load_tags
```