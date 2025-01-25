FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /

# Скопируем список зависимостей и установим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем исходники (включая main.py)
COPY . .

# По умолчанию запускаем main.py
CMD ["python", "main.py"]
