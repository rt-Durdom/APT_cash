# Описание проекта




# Запуск проекта - .. пока без контейнеров

docker compose up --build \n
.. docker compose run web python manage.py migrate - при необходимости \n
docker compose run web python manage.py createsuperuser \n
docker compose restart web \n
админка - http://127.0.0.1:8000/admin \n
        - http://127.0.0.1:8000/api/docs - swagger \n