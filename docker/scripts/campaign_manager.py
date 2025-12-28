#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Campaign Manager - API для управления телефонными кампаниями
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
import psycopg2.extras
import panoramisk
import asyncio
import csv
import io
import os
from datetime import datetime
import random
import httpx

app = FastAPI(title="Phone Campaign Manager API")

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Конфигурация
DB_CONFIG = {
    'host': os.getenv('DATABASE_URL', 'postgres').split('@')[1].split(':')[0] if '@' in os.getenv('DATABASE_URL', 'postgres') else 'postgres',
    'database': 'phone_campaigns',
    'user': 'phone_user',
    'password': 'phone_pass_2024'
}

AMI_CONFIG = {
    'host': os.getenv('ASTERISK_HOST', 'asterisk'),
    'port': int(os.getenv('ASTERISK_AMI_PORT', 5038)),
    'username': os.getenv('ASTERISK_AMI_USER', 'admin'),
    'secret': os.getenv('ASTERISK_AMI_SECRET', 'asterisk_secret')
}

TTS_SERVICE_URL = os.getenv('TTS_SERVICE_URL', 'http://tts-service:5000')


# ============== MODELS ==============

class Campaign(BaseModel):
    name: str
    description: Optional[str] = None
    audio_file: Optional[str] = None


class CampaignNumbers(BaseModel):
    campaign_id: int
    phone_numbers: List[str]


class CallRequest(BaseModel):
    phone_number: str
    audio_file: Optional[str] = None


class TTSRequest(BaseModel):
    text: str
    filename: Optional[str] = None


# ============== DATABASE ==============

def get_db():
    """Подключение к БД"""
    return psycopg2.connect(**DB_CONFIG)


# ============== ASTERISK AMI ==============

async def make_call_via_ami(phone_number: str, audio_file: Optional[str] = None):
    """
    Инициирует звонок через Asterisk AMI
    """
    try:
        manager = panoramisk.Manager(
            loop=asyncio.get_event_loop(),
            **AMI_CONFIG
        )

        await manager.connect()

        # Originate call
        response = await manager.send_action({
            'Action': 'Originate',
            'Channel': f'Local/{phone_number}@outbound-calls',
            'Context': 'outbound-calls',
            'Exten': phone_number,
            'Priority': '1',
            'Timeout': '60000',
            'CallerID': phone_number,
            'Async': 'true',
            'Variable': f'AUDIO_FILE={audio_file}' if audio_file else ''
        })

        manager.close()

        return {'success': True, 'response': str(response)}

    except Exception as e:
        return {'success': False, 'error': str(e)}


# ============== API ENDPOINTS ==============

@app.get("/")
async def root():
    """Редирект на веб-интерфейс"""
    return RedirectResponse(url="/static/index.html")


@app.get("/api")
async def api_root():
    """Статус API"""
    return {
        "service": "Phone Campaign Manager",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/api/campaigns")
async def list_campaigns():
    """Список всех кампаний"""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT id, name, description, status,
               total_numbers, processed_numbers,
               successful_calls, failed_calls,
               created_at, started_at, completed_at
        FROM campaigns
        ORDER BY created_at DESC
    """)

    campaigns = cur.fetchall()
    cur.close()
    conn.close()

    return {"campaigns": campaigns}


@app.post("/api/campaigns")
async def create_campaign(campaign: Campaign):
    """Создать новую кампанию"""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO campaigns (name, description, audio_file, status)
        VALUES (%s, %s, %s, 'draft')
        RETURNING id
    """, (campaign.name, campaign.description, campaign.audio_file))

    campaign_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return {"campaign_id": campaign_id, "status": "created"}


@app.post("/api/campaigns/{campaign_id}/numbers")
async def add_numbers(campaign_id: int, file: UploadFile = File(...)):
    """
    Загрузить список номеров из CSV файла
    Формат CSV: phone_number (одна колонка)
    """
    contents = await file.read()
    csv_data = io.StringIO(contents.decode('utf-8'))

    reader = csv.DictReader(csv_data)
    phone_numbers = []

    for row in reader:
        if 'phone_number' in row:
            phone_numbers.append(row['phone_number'])

    if not phone_numbers:
        raise HTTPException(status_code=400, detail="Нет номеров в файле")

    conn = get_db()
    cur = conn.cursor()

    # Добавляем номера
    for phone in phone_numbers:
        cur.execute("""
            INSERT INTO campaign_numbers (campaign_id, phone_number, status)
            VALUES (%s, %s, 'pending')
            ON CONFLICT DO NOTHING
        """, (campaign_id, phone))

    # Обновляем счетчик в кампании
    cur.execute("""
        UPDATE campaigns
        SET total_numbers = (
            SELECT COUNT(*) FROM campaign_numbers
            WHERE campaign_id = %s
        )
        WHERE id = %s
    """, (campaign_id, campaign_id))

    conn.commit()
    cur.close()
    conn.close()

    return {
        "campaign_id": campaign_id,
        "numbers_added": len(phone_numbers),
        "status": "success"
    }


@app.post("/api/campaigns/{campaign_id}/start")
async def start_campaign(campaign_id: int):
    """Запустить кампанию"""
    conn = get_db()
    cur = conn.cursor()

    # Обновляем статус кампании
    cur.execute("""
        UPDATE campaigns
        SET status = 'running', started_at = %s
        WHERE id = %s
    """, (datetime.now(), campaign_id))

    conn.commit()
    cur.close()
    conn.close()

    # Запускаем фоновую задачу для обзвона
    asyncio.create_task(process_campaign(campaign_id))

    return {"campaign_id": campaign_id, "status": "started"}


@app.post("/api/campaigns/{campaign_id}/pause")
async def pause_campaign(campaign_id: int):
    """Приостановить кампанию"""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE campaigns
        SET status = 'paused'
        WHERE id = %s
    """, (campaign_id,))

    conn.commit()
    cur.close()
    conn.close()

    return {"campaign_id": campaign_id, "status": "paused"}


@app.get("/api/campaigns/{campaign_id}/stats")
async def get_campaign_stats(campaign_id: int):
    """Статистика кампании"""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT
            c.name,
            c.status,
            c.total_numbers,
            c.processed_numbers,
            c.successful_calls,
            c.failed_calls,
            COUNT(CASE WHEN cn.status = 'pending' THEN 1 END) as pending,
            COUNT(CASE WHEN cn.status = 'answered' THEN 1 END) as answered,
            COUNT(CASE WHEN cn.status = 'no_answer' THEN 1 END) as no_answer,
            COUNT(CASE WHEN cn.status = 'busy' THEN 1 END) as busy,
            COUNT(CASE WHEN cn.status = 'failed' THEN 1 END) as failed
        FROM campaigns c
        LEFT JOIN campaign_numbers cn ON c.id = cn.campaign_id
        WHERE c.id = %s
        GROUP BY c.id
    """, (campaign_id,))

    stats = cur.fetchone()
    cur.close()
    conn.close()

    if not stats:
        raise HTTPException(status_code=404, detail="Кампания не найдена")

    return stats


@app.post("/api/call")
async def make_call(call: CallRequest):
    """Выполнить один звонок"""
    result = await make_call_via_ami(call.phone_number, call.audio_file)

    if result['success']:
        return {"status": "calling", "phone_number": call.phone_number}
    else:
        raise HTTPException(status_code=500, detail=result['error'])


@app.get("/api/sims")
async def get_sims_status():
    """Статус всех SIM-карт"""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT sim_number, operator, phone_number, status,
               calls_today, calls_this_hour,
               daily_call_limit, hourly_call_limit,
               last_call_time
        FROM sim_cards
        ORDER BY sim_number
    """)

    sims = cur.fetchall()
    cur.close()
    conn.close()

    return {"sims": sims}


# ============== TTS ENDPOINTS ==============

@app.post("/api/tts/generate")
async def generate_tts(request: TTSRequest):
    """
    Генерирует голосовое сообщение из текста через TTS сервис

    POST /api/tts/generate
    {
        "text": "Привет, это тестовое сообщение",
        "filename": "message.wav"
    }
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Формируем тело запроса, не отправляем filename если он None
            payload = {"text": request.text}
            if request.filename:
                payload["filename"] = request.filename

            response = await client.post(
                f"{TTS_SERVICE_URL}/api/tts/generate",
                json=payload
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"TTS service error: {response.text}"
                )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"TTS service unavailable: {str(e)}"
        )


@app.get("/api/tts/files")
async def list_tts_files():
    """
    Список всех сгенерированных аудио файлов

    GET /api/tts/files
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{TTS_SERVICE_URL}/api/tts/files")

            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to get file list"
                )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"TTS service unavailable: {str(e)}"
        )


@app.get("/api/tts/audio/{filename}")
async def get_tts_audio(filename: str):
    """
    Получить аудио файл из TTS сервиса

    GET /api/tts/audio/message.wav
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{TTS_SERVICE_URL}/api/tts/audio/{filename}")

            if response.status_code == 200:
                from fastapi.responses import Response
                return Response(
                    content=response.content,
                    media_type="audio/wav",
                    headers={"Content-Disposition": f"inline; filename={filename}"}
                )
            else:
                raise HTTPException(status_code=404, detail="Audio file not found")

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"TTS service unavailable: {str(e)}"
        )


@app.get("/api/tts/health")
async def check_tts_health():
    """
    Проверить доступность TTS сервиса

    GET /api/tts/health
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{TTS_SERVICE_URL}/health")

            if response.status_code == 200:
                data = response.json()
                data['url'] = TTS_SERVICE_URL
                return data
            else:
                return {
                    "status": "unhealthy",
                    "url": TTS_SERVICE_URL,
                    "error": response.text
                }

    except httpx.RequestError as e:
        return {
            "status": "unavailable",
            "url": TTS_SERVICE_URL,
            "error": str(e)
        }


# ============== BACKGROUND TASKS ==============

async def process_campaign(campaign_id: int):
    """
    Фоновая задача для обработки кампании
    С антидетект-логикой (рандомные интервалы)
    """
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    while True:
        # Проверяем статус кампании
        cur.execute("""
            SELECT status, audio_file FROM campaigns WHERE id = %s
        """, (campaign_id,))

        campaign = cur.fetchone()

        if not campaign or campaign['status'] != 'running':
            break

        # Берем следующий номер
        cur.execute("""
            SELECT id, phone_number FROM campaign_numbers
            WHERE campaign_id = %s AND status = 'pending'
            ORDER BY id ASC
            LIMIT 1
        """, (campaign_id,))

        number = cur.fetchone()

        if not number:
            # Кампания завершена
            cur.execute("""
                UPDATE campaigns
                SET status = 'completed', completed_at = %s
                WHERE id = %s
            """, (datetime.now(), campaign_id))
            conn.commit()
            break

        # Выполняем звонок
        cur.execute("""
            UPDATE campaign_numbers
            SET status = 'calling', last_attempt_time = %s, call_attempts = call_attempts + 1
            WHERE id = %s
        """, (datetime.now(), number['id']))

        conn.commit()

        # Звоним
        result = await make_call_via_ami(number['phone_number'], campaign['audio_file'])

        # Обновляем статус (упрощенно)
        new_status = 'answered' if result['success'] else 'failed'

        cur.execute("""
            UPDATE campaign_numbers
            SET status = %s
            WHERE id = %s
        """, (new_status, number['id']))

        # Обновляем счетчики кампании
        cur.execute("""
            UPDATE campaigns
            SET processed_numbers = processed_numbers + 1,
                successful_calls = successful_calls + CASE WHEN %s = 'answered' THEN 1 ELSE 0 END,
                failed_calls = failed_calls + CASE WHEN %s = 'failed' THEN 1 ELSE 0 END
            WHERE id = %s
        """, (new_status, new_status, campaign_id))

        conn.commit()

        # Антидетект: случайная пауза (45 сек - 3 мин)
        delay = random.uniform(45, 180)

        # 15% шанс длинной паузы (5-15 мин)
        if random.random() < 0.15:
            delay += random.uniform(300, 900)

        await asyncio.sleep(delay)

    cur.close()
    conn.close()


# ============== RUN ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
