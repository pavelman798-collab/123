FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скачиваем Piper TTS бинарник и русскую модель
RUN wget -q https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz && \
    tar -xzf piper_amd64.tar.gz && \
    rm piper_amd64.tar.gz && \
    chmod +x piper/piper

# Скачиваем русскую модель (средне-качественная, оптимальный размер)
RUN mkdir -p /app/models && \
    wget -q -O /app/models/ru_RU-ruslan-medium.onnx \
    https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx && \
    wget -q -O /app/models/ru_RU-ruslan-medium.onnx.json \
    https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx.json

# Копируем сервис
COPY tts_service.py .

# Создаем директорию для аудио
RUN mkdir -p /audio

# Переменные окружения
ENV PIPER_PATH=/app/piper/piper
ENV MODEL_PATH=/app/models/ru_RU-ruslan-medium.onnx
ENV AUDIO_DIR=/audio

EXPOSE 5000

CMD ["python", "tts_service.py"]
