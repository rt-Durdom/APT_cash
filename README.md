# Описание проекта




# Запуск проекта - .. пока без контейнеров

docker compose up --build
.. docker compose run web python manage.py migrate - при необходимости
docker compose run web python manage.py createsuperuser
docker compose restart web
админка - http://127.0.0.1:8000/admin