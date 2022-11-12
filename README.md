# praktikum_new_diplom


## Установка проекта локально
* Загрузите список ингредиентов:
```bash
docker-compose exec web python manage.py load_ingredients
```
* Загрузите теги:
```bash
docker-compose exec web python manage.py load_tags
```