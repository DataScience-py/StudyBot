FROM python:3.12-slim

# Устанавливаем Poetry.
# Можно использовать менеджер пакетов системы, например, apt, или установить через pipx.
# Пример установки через pipx (требует установки pipx в базовый образ):
# RUN apt-get update && apt-get install -y pipx
# RUN pipx ensurepath
# RUN pipx install poetry

# Или, более простой вариант, напрямую через pip (если pipx не установлен):
RUN pip install poetry

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем только файл poetry.lock и pyproject.toml, чтобы эффективно использовать кэш Docker
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости с помощью Poetry
RUN poetry install --no-root

# Копируем остальные файлы проекта
COPY src ./src

# Запускаем приложение
CMD ["poetry", "run", "python", "src/main.py"]