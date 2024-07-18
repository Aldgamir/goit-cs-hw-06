# Використовуємо базовий образ Python
FROM python:3.8-slim

# Виконуємо інсталювання залежностей
RUN pip install pymongo

# Копіюємо файли проекта
COPY . /app

# Переходимо в робочу директорію
WORKDIR /app

# Запскаємо обидва сервери
CMD ["python", "main.py"]