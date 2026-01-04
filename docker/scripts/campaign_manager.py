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

GOIP_CONFIG = {
    'host': os.getenv('GOIP_HOST', '192.168.8.1'),
    'username': os.getenv('GOIP_USER', 'admin'),
    'password': os.getenv('GOIP_PASS', 'admin'),
    'use_ssl': os.getenv('GOIP_SSL', 'false').lower() == 'true'
}


# ============== MODELS ==============

class Campaign(BaseModel):
    name: str
    description: Optional[str] = None
    campaign_type: str = "call"  # call, sms, call_and_sms
    audio_file: Optional[str] = None
    sms_on_no_answer: Optional[str] = None
    sms_on_success: Optional[str] = None
    send_sms_on_no_answer: bool = False
    send_sms_on_success: bool = False
    scheduled_start_time: Optional[str] = None  # ISO format datetime string (UTC)
    use_timezones: bool = False
    timezone_mode: str = "none"  # none, manual, auto


class CampaignNumbers(BaseModel):
    campaign_id: int
    phone_numbers: List[str]


class CallRequest(BaseModel):
    phone_number: str
    audio_file: Optional[str] = None


class TTSRequest(BaseModel):
    text: str
    filename: Optional[str] = None
    voice: str = "ruslan"  # ruslan, dmitri, irina
    speed: float = 1.0  # 0.5 - 2.0


class SMSTemplate(BaseModel):
    name: str
    text: str
    category: Optional[str] = "general"  # no_answer, success, general


class SMSRequest(BaseModel):
    phone_number: str
    message: str
    sim_number: Optional[int] = None


# ============== DATABASE ==============

def get_db():
    """Подключение к БД"""
    return psycopg2.connect(**DB_CONFIG)


def detect_timezone_from_phone(phone_number: str, cursor):
    """
    Определить часовой пояс по префиксу номера телефона

    Args:
        phone_number: Номер в формате 79991234567
        cursor: Database cursor

    Returns:
        str: Timezone name (e.g. 'Europe/Moscow') или None
    """
    # Извлекаем префикс (первые 3 цифры после +7)
    if len(phone_number) >= 4:
        prefix = phone_number[1:4]  # 79991234567 -> 999

        # Ищем в справочнике
        cursor.execute("""
            SELECT timezone FROM phone_prefix_info
            WHERE prefix = %s
            LIMIT 1
        """, (prefix,))

        result = cursor.fetchone()
        if result:
            return result[0]

    return None  # Не найдено - вернём None


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


async def send_sms_via_goip(phone_number: str, message: str, sim_number: int = 1):
    """
    Отправить СМС через GoIP HTTP API

    Args:
        phone_number: Номер телефона (79991234567)
        message: Текст сообщения (кириллица будет закодирована в URL)
        sim_number: Номер SIM-карты (1-4)

    Returns:
        dict: {'success': True/False, 'response': str, 'error': str}
    """
    try:
        protocol = 'https' if GOIP_CONFIG['use_ssl'] else 'http'
        base_url = f"{protocol}://{GOIP_CONFIG['host']}"

        # GoIP SMS API endpoint
        # Формат: /default/en_US/send.html?username=admin&password=admin&smsnum=1&Memo=message&telnum=79991234567
        url = f"{base_url}/default/en_US/send.html"

        params = {
            'username': GOIP_CONFIG['username'],
            'password': GOIP_CONFIG['password'],
            'smsnum': str(sim_number),
            'Memo': message,
            'telnum': phone_number
        }

        async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
            response = await client.get(url, params=params)

            # GoIP возвращает "send success" при успехе
            if response.status_code == 200 and 'success' in response.text.lower():
                return {
                    'success': True,
                    'response': response.text,
                    'sim_number': sim_number
                }
            else:
                return {
                    'success': False,
                    'error': f"GoIP response: {response.text}",
                    'status_code': response.status_code
                }

    except httpx.RequestError as e:
        return {
            'success': False,
            'error': f'GoIP connection error: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'SMS send error: {str(e)}'
        }


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
               created_at, started_at, completed_at,
               scheduled_start_time, use_timezones, timezone_mode
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

    # Определяем статус: если указано время старта - scheduled, иначе - draft
    status = 'scheduled' if campaign.scheduled_start_time else 'draft'

    # Парсим scheduled_start_time из ISO string в datetime если указано
    scheduled_dt = None
    if campaign.scheduled_start_time:
        try:
            scheduled_dt = datetime.fromisoformat(campaign.scheduled_start_time.replace('Z', '+00:00'))
        except:
            scheduled_dt = None

    cur.execute("""
        INSERT INTO campaigns (
            name, description, campaign_type, audio_file,
            sms_on_no_answer, sms_on_success,
            send_sms_on_no_answer, send_sms_on_success,
            scheduled_start_time, use_timezones, timezone_mode,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        campaign.name, campaign.description, campaign.campaign_type,
        campaign.audio_file, campaign.sms_on_no_answer, campaign.sms_on_success,
        campaign.send_sms_on_no_answer, campaign.send_sms_on_success,
        scheduled_dt, campaign.use_timezones, campaign.timezone_mode,
        status
    ))

    campaign_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return {"campaign_id": campaign_id, "status": status}


@app.post("/api/campaigns/{campaign_id}/numbers")
async def add_numbers(campaign_id: int, file: UploadFile = File(...)):
    """
    Загрузить список номеров из CSV файла
    Формат CSV:
    - Обязательная колонка: phone_number
    - Опциональная колонка: timezone (для timezone_mode='manual')
    """
    contents = await file.read()
    csv_data = io.StringIO(contents.decode('utf-8'))

    reader = csv.DictReader(csv_data)
    phone_numbers = []

    conn = get_db()
    cur = conn.cursor()

    # Получаем настройки timezone для кампании
    cur.execute("""
        SELECT timezone_mode, use_timezones FROM campaigns WHERE id = %s
    """, (campaign_id,))
    campaign_settings = cur.fetchone()

    if not campaign_settings:
        raise HTTPException(status_code=404, detail="Кампания не найдена")

    timezone_mode, use_timezones = campaign_settings

    for row in reader:
        if 'phone_number' not in row:
            continue

        phone = row['phone_number'].strip()
        timezone = None

        if use_timezones:
            if timezone_mode == 'manual' and 'timezone' in row:
                # Режим manual - берём timezone из CSV
                timezone = row['timezone'].strip() if row['timezone'] else None
            elif timezone_mode == 'auto':
                # Режим auto - определяем по префиксу
                timezone = detect_timezone_from_phone(phone, cur)

        phone_numbers.append((phone, timezone))

    if not phone_numbers:
        raise HTTPException(status_code=400, detail="Нет номеров в файле")

    # Добавляем номера
    for phone, tz in phone_numbers:
        cur.execute("""
            INSERT INTO campaign_numbers (campaign_id, phone_number, timezone, status)
            VALUES (%s, %s, %s, 'pending')
            ON CONFLICT DO NOTHING
        """, (campaign_id, phone, tz))

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


@app.post("/api/campaigns/{campaign_id}/cancel_schedule")
async def cancel_scheduled_campaign(campaign_id: int):
    """Отменить запланированный запуск кампании"""
    conn = get_db()
    cur = conn.cursor()

    # Проверяем что кампания в статусе scheduled
    cur.execute("""
        SELECT status FROM campaigns WHERE id = %s
    """, (campaign_id,))

    result = cur.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Кампания не найдена")

    if result[0] != 'scheduled':
        raise HTTPException(status_code=400, detail="Кампания не запланирована")

    # Отменяем запуск - переводим в draft и очищаем scheduled_start_time
    cur.execute("""
        UPDATE campaigns
        SET status = 'draft',
            cancelled_at = %s,
            scheduled_start_time = NULL
        WHERE id = %s
    """, (datetime.now(), campaign_id))

    conn.commit()
    cur.close()
    conn.close()

    return {"campaign_id": campaign_id, "status": "cancelled", "message": "Запланированный запуск отменён"}


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
            payload = {
                "text": request.text,
                "voice": request.voice,
                "speed": request.speed
            }
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


@app.get("/api/tts/voices")
async def get_tts_voices():
    """
    Получить список доступных голосов

    GET /api/tts/voices
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{TTS_SERVICE_URL}/api/tts/voices")

            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to get voices"
                )

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


# ============== SMS TEMPLATE ENDPOINTS ==============

@app.get("/api/sms/templates")
async def list_sms_templates(category: Optional[str] = None):
    """
    Получить список шаблонов СМС

    GET /api/sms/templates
    GET /api/sms/templates?category=no_answer
    """
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if category:
        cur.execute("""
            SELECT id, name, text, category, created_at, updated_at
            FROM sms_templates
            WHERE category = %s
            ORDER BY created_at DESC
        """, (category,))
    else:
        cur.execute("""
            SELECT id, name, text, category, created_at, updated_at
            FROM sms_templates
            ORDER BY created_at DESC
        """)

    templates = cur.fetchall()
    cur.close()
    conn.close()

    return {"templates": templates}


@app.post("/api/sms/templates")
async def create_sms_template(template: SMSTemplate):
    """
    Создать новый шаблон СМС

    POST /api/sms/templates
    {
        "name": "Напоминание о записи",
        "text": "Здравствуйте! Напоминаем о записи завтра в 15:00.",
        "category": "no_answer"
    }
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO sms_templates (name, text, category)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (template.name, template.text, template.category))

    template_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return {
        "template_id": template_id,
        "status": "created",
        "name": template.name
    }


@app.put("/api/sms/templates/{template_id}")
async def update_sms_template(template_id: int, template: SMSTemplate):
    """
    Обновить шаблон СМС

    PUT /api/sms/templates/1
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE sms_templates
        SET name = %s, text = %s, category = %s, updated_at = %s
        WHERE id = %s
    """, (template.name, template.text, template.category, datetime.now(), template_id))

    conn.commit()
    affected = cur.rowcount
    cur.close()
    conn.close()

    if affected == 0:
        raise HTTPException(status_code=404, detail="Шаблон не найден")

    return {"template_id": template_id, "status": "updated"}


@app.delete("/api/sms/templates/{template_id}")
async def delete_sms_template(template_id: int):
    """
    Удалить шаблон СМС

    DELETE /api/sms/templates/1
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM sms_templates WHERE id = %s", (template_id,))

    conn.commit()
    affected = cur.rowcount
    cur.close()
    conn.close()

    if affected == 0:
        raise HTTPException(status_code=404, detail="Шаблон не найден")

    return {"template_id": template_id, "status": "deleted"}


# ============== SMS SENDING ENDPOINTS ==============

@app.post("/api/sms/send")
async def send_sms(sms: SMSRequest):
    """
    Отправить СМС через GoIP

    POST /api/sms/send
    {
        "phone_number": "79991234567",
        "message": "Ваше сообщение",
        "sim_number": 1
    }
    """
    # Определяем SIM-карту если не указана
    sim_number = sms.sim_number if sms.sim_number else 1

    # Отправляем СМС через GoIP
    result = await send_sms_via_goip(sms.phone_number, sms.message, sim_number)

    conn = get_db()
    cur = conn.cursor()

    # Определяем статус
    status = 'sent' if result['success'] else 'failed'

    # Логируем в sms_log
    cur.execute("""
        INSERT INTO sms_log (phone_number, sim_number, message, status, sent_at)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (
        sms.phone_number,
        sim_number,
        sms.message,
        status,
        datetime.now() if result['success'] else None
    ))

    sms_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    if result['success']:
        return {
            "sms_id": sms_id,
            "status": "sent",
            "phone_number": sms.phone_number,
            "sim_number": sim_number,
            "goip_response": result.get('response', '')
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка отправки СМС: {result.get('error', 'Unknown error')}"
        )


# ============== BACKGROUND TASKS ==============

async def process_campaign(campaign_id: int):
    """
    Фоновая задача для обработки кампании
    Поддерживает: звонки, СМС, звонки+СМС
    С антидетект-логикой (рандомные интервалы)
    """
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    while True:
        # Проверяем статус кампании
        cur.execute("""
            SELECT status, audio_file, campaign_type,
                   sms_on_no_answer, sms_on_success,
                   send_sms_on_no_answer, send_sms_on_success
            FROM campaigns WHERE id = %s
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

        # Обрабатываем номер в зависимости от типа кампании
        campaign_type = campaign['campaign_type']
        call_success = False
        sms_sent = False

        # ========== ЗВОНКИ ==========
        if campaign_type in ['call', 'call_and_sms']:
            # Выполняем звонок
            cur.execute("""
                UPDATE campaign_numbers
                SET status = 'calling', last_attempt_time = %s, call_attempts = call_attempts + 1
                WHERE id = %s
            """, (datetime.now(), number['id']))
            conn.commit()

            # Звоним
            result = await make_call_via_ami(number['phone_number'], campaign['audio_file'])

            # Обновляем статус звонка
            new_status = 'answered' if result['success'] else 'no_answer'
            call_success = result['success']

            cur.execute("""
                UPDATE campaign_numbers
                SET status = %s
                WHERE id = %s
            """, (new_status, number['id']))

            # Обновляем счетчики звонков
            cur.execute("""
                UPDATE campaigns
                SET processed_numbers = processed_numbers + 1,
                    successful_calls = successful_calls + CASE WHEN %s = 'answered' THEN 1 ELSE 0 END,
                    failed_calls = failed_calls + CASE WHEN %s = 'no_answer' THEN 1 ELSE 0 END
                WHERE id = %s
            """, (new_status, new_status, campaign_id))
            conn.commit()

        # ========== СМС ==========
        # Отправляем СМС если:
        # 1. Тип кампании = 'sms' (только СМС)
        # 2. Тип = 'call_and_sms' + недозвон + включена опция send_sms_on_no_answer
        # 3. Тип = 'call_and_sms' + успешный звонок + включена опция send_sms_on_success

        sms_text = None

        if campaign_type == 'sms':
            # Только СМС кампания - отправляем всегда
            sms_text = campaign['sms_on_no_answer'] or campaign['sms_on_success'] or "SMS-сообщение"

        elif campaign_type == 'call_and_sms':
            # Звонок + СМС
            if not call_success and campaign['send_sms_on_no_answer']:
                # Недозвон -> отправляем СМС при недозвоне
                sms_text = campaign['sms_on_no_answer']
            elif call_success and campaign['send_sms_on_success']:
                # Успешный звонок -> отправляем СМС при успехе
                sms_text = campaign['sms_on_success']

        # Отправляем СМС если есть текст
        if sms_text:
            # Определяем SIM-карту (используем ту же что для звонка, или первую доступную)
            sim_number = 1  # TODO: улучшить выбор SIM по оператору

            sms_result = await send_sms_via_goip(number['phone_number'], sms_text, sim_number)
            sms_sent = sms_result['success']

            # Обновляем статус СМС в campaign_numbers
            cur.execute("""
                UPDATE campaign_numbers
                SET sms_status = %s,
                    sms_sent_at = %s,
                    sms_text = %s
                WHERE id = %s
            """, (
                'sent' if sms_sent else 'failed',
                datetime.now() if sms_sent else None,
                sms_text,
                number['id']
            ))

            # Обновляем счетчики СМС в кампании
            cur.execute("""
                UPDATE campaigns
                SET sms_sent = sms_sent + CASE WHEN %s THEN 1 ELSE 0 END,
                    sms_failed = sms_failed + CASE WHEN NOT %s THEN 1 ELSE 0 END
                WHERE id = %s
            """, (sms_sent, sms_sent, campaign_id))

            # Логируем в sms_log
            cur.execute("""
                INSERT INTO sms_log (campaign_id, phone_number, sim_number, message, status, sent_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                campaign_id,
                number['phone_number'],
                sim_number,
                sms_text,
                'sent' if sms_sent else 'failed',
                datetime.now() if sms_sent else None
            ))

            conn.commit()

        # Если только СМС кампания и мы только что отправили СМС, обновляем счетчик processed
        if campaign_type == 'sms':
            cur.execute("""
                UPDATE campaigns
                SET processed_numbers = processed_numbers + 1
                WHERE id = %s
            """, (campaign_id,))
            conn.commit()

        # Антидетект: случайная пауза (45 сек - 3 мин)
        delay = random.uniform(45, 180)

        # 15% шанс длинной паузы (5-15 мин)
        if random.random() < 0.15:
            delay += random.uniform(300, 900)

        await asyncio.sleep(delay)

    cur.close()
    conn.close()


# ==============================================================================
# ПЛАНИРОВЩИК - Автоматический запуск запланированных кампаний
# ==============================================================================

async def check_scheduled_campaigns():
    """
    Фоновая задача: проверяет каждую минуту запланированные кампании
    и запускает их если пришло время
    """
    while True:
        try:
            conn = get_db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Найти кампании со статусом 'scheduled' и временем запуска <= NOW()
            cur.execute("""
                SELECT id, name, scheduled_start_time
                FROM campaigns
                WHERE status = 'scheduled'
                  AND scheduled_start_time IS NOT NULL
                  AND scheduled_start_time <= NOW()
                ORDER BY scheduled_start_time ASC
            """)

            campaigns_to_start = cur.fetchall()

            if campaigns_to_start:
                print(f"[Scheduler] Найдено {len(campaigns_to_start)} кампаний для запуска")

            for campaign in campaigns_to_start:
                campaign_id = campaign['id']
                campaign_name = campaign['name']
                scheduled_time = campaign['scheduled_start_time']

                print(f"[Scheduler] Запуск кампании #{campaign_id} '{campaign_name}' (запланировано на {scheduled_time})")

                try:
                    # Меняем статус на 'running' и записываем started_at
                    cur.execute("""
                        UPDATE campaigns
                        SET status = 'running',
                            started_at = NOW()
                        WHERE id = %s
                    """, (campaign_id,))

                    conn.commit()

                    print(f"[Scheduler] ✅ Кампания #{campaign_id} успешно запущена")

                    # Запускаем процесс обзвона в фоне
                    asyncio.create_task(process_campaign(campaign_id))

                except Exception as e:
                    print(f"[Scheduler] ❌ Ошибка запуска кампании #{campaign_id}: {e}")
                    conn.rollback()

            cur.close()
            conn.close()

        except Exception as e:
            print(f"[Scheduler] Ошибка в планировщике: {e}")

        # Проверять каждые 60 секунд
        await asyncio.sleep(60)


@app.on_event("startup")
async def startup_event():
    """Запуск фоновых задач при старте приложения"""
    print("[Startup] Запуск планировщика кампаний...")
    asyncio.create_task(check_scheduled_campaigns())
    print("[Startup] ✅ Планировщик запущен (проверка каждые 60 сек)")


# ============== RUN ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
