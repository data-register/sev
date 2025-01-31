# Използвайте официалния Python образ
FROM python:3.9-slim

# Настройка на работната директория
WORKDIR /app

# Копиране на изискванията и инсталиране на зависимостите
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копиране на останалата част от кода
COPY . .

# Излагане на порта
EXPOSE 5000

# Команда за стартиране на приложението
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
