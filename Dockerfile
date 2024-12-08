FROM python:3.10-slim-bullseye as requirements-stage

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Добавляем репозиторий PostgreSQL для установки клиента версии 17
RUN echo "deb http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update && apt-get install -y \
    postgresql-client-17 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

# Устанавливаем Poetry
RUN pip install poetry

# Копируем pyproject и lock-файл
COPY ./pyproject.toml ./poetry.lock* /tmp/

# Экспортируем зависимости из Poetry в requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-slim-bullseye as production-stage

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    curl \
    procps \
    net-tools \
    tini \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Добавляем репозиторий PostgreSQL для установки клиента версии 17
RUN echo "deb http://apt.postgresql.org/pub/repos/apt bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update && apt-get install -y \
    postgresql-client-17 \
    && rm -rf /var/lib/apt/lists/*

# Настраиваем окружение Python
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости из requirements.txt
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Копируем исходный код приложения
COPY . /app/

# Открываем порт для приложения
EXPOSE 8000
