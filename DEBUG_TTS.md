# Решение проблемы "TTS service unavailable"

## Проблема
Ошибка: `TTS service unavailable: [Errno -2] Name or service not known`

Это означает, что контейнер TTS не запущен или не подключен к сети.

## Решение

### Шаг 1: Проверь статус контейнеров

```bash
cd ~/Downloads/123-claude-phone-campaign-system-0JRfL-2
docker compose ps
```

**Должно быть 4 контейнера в статусе "Up":**
- phone-asterisk
- phone-postgres
- phone-campaign-manager
- phone-tts ← этот должен быть запущен!

### Шаг 2: Если phone-tts отсутствует или остановлен

```bash
# Останови все контейнеры
docker compose down

# Запусти заново с пересборкой (ВАЖНО: --build обязателен!)
docker compose up --build -d
```

Первый запуск займет **3-5 минут**, т.к. будет:
- Скачиваться Piper TTS (~10 MB)
- Скачиваться русская модель (~100 MB)

### Шаг 3: Проверь логи TTS сервиса

```bash
# Смотри логи в реальном времени
docker logs phone-tts -f
```

**Должно быть:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:5000
INFO:     Application startup complete
```

### Шаг 4: Если есть ошибки при сборке

Посмотри полные логи:
```bash
docker compose logs tts-service
```

**Частые проблемы:**

**1. Ошибка скачивания модели**
```
wget: unable to resolve host address
```

**Решение:** Проверь интернет-соединение, повтори:
```bash
docker compose build --no-cache tts-service
docker compose up -d tts-service
```

**2. Ошибка прав доступа**
```
Permission denied: /audio
```

**Решение:** Создай папку audio:
```bash
mkdir -p audio
docker compose up -d
```

### Шаг 5: Проверь доступность TTS

После запуска всех контейнеров:

```bash
# Проверка health endpoint
curl http://localhost:8000/api/tts/health
```

**Должен вернуть:**
```json
{
  "status": "healthy",
  "piper": true,
  "model": true,
  "url": "http://tts-service:5000"
}
```

### Шаг 6: Тестовая генерация

```bash
curl -X POST http://localhost:8000/api/tts/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Привет, это тест"}' | jq
```

**Ожидаемый ответ:**
```json
{
  "success": true,
  "filename": "tts_20250128_123456_abc123.wav",
  "path": "/audio/tts_20250128_123456_abc123.wav",
  "size": 44186,
  "text_length": 17
}
```

---

## Быстрое решение (если что-то пошло не так)

Полная пересборка:

```bash
# Останови все
docker compose down

# Удали volumes (если нужно)
docker volume prune

# Пересобери все с нуля
docker compose build --no-cache

# Запусти
docker compose up -d

# Подожди 3-5 минут, затем проверь
docker compose ps
docker logs phone-tts
```

---

## После успешного запуска

1. Обнови страницу в браузере (http://localhost:8000)
2. Перейди в "Генератор голоса"
3. Справа должен исчезнуть "TTS сервис недоступен"
4. Можешь генерировать голос!

---

## Если проблема остается

Пришли мне вывод команд:

```bash
docker compose ps
docker logs phone-tts
docker logs phone-campaign-manager | tail -20
```
