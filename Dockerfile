FROM python:3.13-slim

# Установка системных зависимостей для psycopg2 и Pillow
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.0.0
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

# Собираем статику (необязательно, если есть Nginx, но полезно)
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]