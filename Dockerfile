FROM python:3.10-slim

# Установим рабочую директорию
WORKDIR /app

# Скопируем зависимости и установим их
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем всё приложение в контейнер
COPY ./app /app

# Укажем команду для запуска
CMD ["python", "main.py"]
