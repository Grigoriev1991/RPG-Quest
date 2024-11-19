# Используем официальный Python образ
FROM python:3.11.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем точку входа для контейнера
ENTRYPOINT ["python", "-m", "main"]

# По умолчанию запускаем игру
CMD ["game"]
