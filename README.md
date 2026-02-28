# Описание проекта APT_cash
Веб-сервис на Django с REST API для групповых денежных сборов.

## Требования
- Docker и Docker Compose
- Файл `.env` в корне проекта (переменные для БД, Redis, email — см. пример ниже)

## Запуск проекта
- `docker compose up --build -d`
- `docker compose exec web python manage.py migrate`
- `docker compose exec web python manage.py createsuperuser`

## URL
Админка	http://127.0.0.1:8000/admin
Swagger	http://127.0.0.1:8000/api/docs/
API	http://127.0.0.1:8000/api/


## API
Доступ по авторизации. Инициатор видит только свои сборы и ленту доноров по ним; донор — только свои платежи.
Сборы: 
- GET/POST /api/collects/
- GET/PUT/PATCH/DELETE /api/collects/{id}/
- GET /api/collects/{id}/donors/ (лента доноров)
Платежи: 
- GET/POST /api/payments/,
- GET/PUT/PATCH/DELETE /api/payments/{id}/

## Файковые данные
Очистка сборов и платежей:
- `docker compose exec web python manage.py clean_db`
Заполнение фейковыми данными (50 пользователей, 1000 сборов, 5000 платежей):
- `docker compose exec web python manage.py fake_data`


## Стек
- Python 3.11, Django 4.2, Django REST Framework
- PostgreSQL 16, Redis
- Docker, docker compose

