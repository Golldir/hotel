FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml poetry.lock ./
# Установка Poetry
RUN pip install --no-cache-dir poetry

# Настройка Poetry для установки зависимостей в системный Python
RUN poetry install --no-root


# Копируем код приложения
COPY app /app/

CMD poetry run python manage.py makemigrations
CMD poetry run python manage.py migrate
