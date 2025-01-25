FROM python:3.10-slim

WORKDIR /app

# Скопируем зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Скопируем приложение
COPY ./app /app

CMD ["python", "main.py"]
