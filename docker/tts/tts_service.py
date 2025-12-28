#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Piper TTS Service - API для генерации речи из текста
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import os
import uuid
from datetime import datetime

app = FastAPI(title="Piper TTS Service")

# Конфигурация
PIPER_PATH = os.getenv('PIPER_PATH', '/app/piper/piper')
AUDIO_DIR = os.getenv('AUDIO_DIR', '/audio')

# Доступные голосовые модели
VOICE_MODELS = {
    "ruslan": {
        "name": "Руслан",
        "gender": "male",
        "description": "Мужской голос, нейтральный",
        "path": "/app/models/ru_RU-ruslan-medium.onnx"
    },
    "dmitri": {
        "name": "Дмитрий",
        "gender": "male",
        "description": "Мужской голос, энергичный",
        "path": "/app/models/ru_RU-dmitri-medium.onnx"
    },
    "irina": {
        "name": "Ирина",
        "gender": "female",
        "description": "Женский голос, мягкий",
        "path": "/app/models/ru_RU-irina-medium.onnx"
    }
}


class TTSRequest(BaseModel):
    text: str
    filename: str = None  # Опционально: имя файла (иначе генерируется автоматически)
    voice: str = "ruslan"  # Голос: ruslan, dmitri, irina
    speed: float = 1.0  # Скорость: 0.5 (медленно) - 2.0 (быстро)


@app.get("/")
async def root():
    """Статус сервиса"""
    return {
        "service": "Piper TTS",
        "status": "running",
        "version": "2.0.0",
        "voices": list(VOICE_MODELS.keys())
    }


@app.get("/api/tts/voices")
async def get_voices():
    """Список доступных голосов"""
    return {
        "voices": [
            {
                "id": voice_id,
                "name": voice_data["name"],
                "gender": voice_data["gender"],
                "description": voice_data["description"]
            }
            for voice_id, voice_data in VOICE_MODELS.items()
        ]
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    # Проверяем наличие Piper и модели
    piper_exists = os.path.exists(PIPER_PATH)
    model_exists = os.path.exists(MODEL_PATH)

    if not piper_exists:
        raise HTTPException(status_code=500, detail="Piper binary not found")

    if not model_exists:
        raise HTTPException(status_code=500, detail="Model not found")

    return {
        "status": "healthy",
        "piper": piper_exists,
        "model": model_exists
    }


@app.post("/api/tts/generate")
async def generate_speech(request: TTSRequest):
    """
    Генерирует речь из текста и возвращает путь к файлу

    POST /api/tts/generate
    {
        "text": "Привет, это тестовое сообщение",
        "filename": "message.wav"  // опционально
    }
    """
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Текст не может быть пустым")

    # Проверяем валидность голоса
    if request.voice not in VOICE_MODELS:
        raise HTTPException(status_code=400, detail=f"Неизвестный голос: {request.voice}")

    # Проверяем валидность скорости
    if not (0.5 <= request.speed <= 2.0):
        raise HTTPException(status_code=400, detail="Скорость должна быть от 0.5 до 2.0")

    # Выбираем модель голоса
    model_path = VOICE_MODELS[request.voice]["path"]

    # Генерируем имя файла
    if request.filename:
        # Убираем расширение если есть и добавляем .wav
        filename = request.filename.replace('.wav', '') + '.wav'
    else:
        # Автоматическая генерация имени
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"tts_{timestamp}_{unique_id}.wav"

    output_path = os.path.join(AUDIO_DIR, filename)

    try:
        # Вычисляем length_scale (обратно скорости: меньше = быстрее)
        length_scale = 1.0 / request.speed

        # Запускаем Piper для генерации речи
        # echo "текст" | piper --model model.onnx --length_scale 1.0 --output_file output.wav
        piper_command = [
            PIPER_PATH,
            '--model', model_path,
            '--length_scale', str(length_scale),
            '--output_file', output_path
        ]

        process = subprocess.Popen(
            piper_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate(input=request.text)

        if process.returncode != 0:
            raise Exception(f"Piper error: {stderr}")

        # Проверяем что файл создан
        if not os.path.exists(output_path):
            raise Exception("Output file was not created")

        file_size = os.path.getsize(output_path)

        return {
            "success": True,
            "filename": filename,
            "path": output_path,
            "size": file_size,
            "text_length": len(request.text),
            "voice": request.voice,
            "speed": request.speed
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@app.get("/api/tts/audio/{filename}")
async def get_audio_file(filename: str):
    """
    Скачать аудио файл

    GET /api/tts/audio/message.wav
    """
    file_path = os.path.join(AUDIO_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(
        file_path,
        media_type="audio/wav",
        filename=filename
    )


@app.get("/api/tts/files")
async def list_audio_files():
    """
    Список всех сгенерированных аудио файлов

    GET /api/tts/files
    """
    try:
        files = []

        for filename in os.listdir(AUDIO_DIR):
            if filename.endswith('.wav'):
                file_path = os.path.join(AUDIO_DIR, filename)
                file_stat = os.stat(file_path)

                files.append({
                    "filename": filename,
                    "size": file_stat.st_size,
                    "created": datetime.fromtimestamp(file_stat.st_ctime).isoformat()
                })

        # Сортируем по дате создания (новые первыми)
        files.sort(key=lambda x: x['created'], reverse=True)

        return {
            "total": len(files),
            "files": files
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/tts/audio/{filename}")
async def delete_audio_file(filename: str):
    """
    Удалить аудио файл

    DELETE /api/tts/audio/message.wav
    """
    file_path = os.path.join(AUDIO_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    try:
        os.remove(file_path)
        return {"success": True, "message": f"File {filename} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
