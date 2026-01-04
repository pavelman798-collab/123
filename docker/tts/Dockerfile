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

# Скачиваем Piper TTS бинарник (определяем архитектуру)
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then \
        PIPER_ARCH="arm64"; \
    else \
        PIPER_ARCH="amd64"; \
    fi && \
    echo "Downloading Piper for architecture: $PIPER_ARCH" && \
    wget -q https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_${PIPER_ARCH}.tar.gz && \
    tar -xzf piper_${PIPER_ARCH}.tar.gz && \
    rm piper_${PIPER_ARCH}.tar.gz && \
    chmod +x piper/piper

# Скачиваем русские модели голосов (мужские и женский)
RUN mkdir -p /app/models && \
    # Руслан - мужской голос (средний, нейтральный)
    wget -q -O /app/models/ru_RU-ruslan-medium.onnx \
    https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx && \
    wget -q -O /app/models/ru_RU-ruslan-medium.onnx.json \
    https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx.json && \
    # Дмитрий - мужской голос (более энергичный)
    wget -q -O /app/models/ru_RU-dmitri-medium.onnx \
    https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx && \
    wget -q -O /app/models/ru_RU-dmitri-medium.onnx.json \
    https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json && \
    # Ирина - женский голос (приятный, мягкий)
    wget -q -O /app/models/ru_RU-irina-medium.onnx \
    https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx && \
    wget -q -O /app/models/ru_RU-irina-medium.onnx.json \
    https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx.json

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
