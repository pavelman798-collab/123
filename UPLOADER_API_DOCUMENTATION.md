# Cassandra Uploader - API Documentation

## Обзор

Веб-интерфейс загрузчика данных использует **ZK Framework** (Java) для управления UI и взаимодействия с сервером.

**Базовый URL:** `http://ivr-gui.mbrd.ru:8080/Uploader`

## Архитектура

### ZK Framework
- **Серверный рендеринг**: UI компоненты генерируются на сервере
- **Динамические UUID**: Каждый компонент получает уникальный ID при загрузке страницы
- **AJAX коммуникация**: Все действия отправляются через `/zkau` endpoint
- **Stateful сессии**: Требуется поддержка cookies для сохранения состояния

## Workflow загрузки данных

```
1. Инициализация
   └─> GET /Uploader → Получение HTML с component UUIDs

2. Загрузка ZIP файла
   └─> POST /Uploader/zkau/upload?uuid={upload_component}&dtid={desktop_id}&sid=0
       Content-Type: multipart/form-data
       Body: ZIP file

3. Создание имени нотификации
   └─> POST /Uploader/zkau
       Content-Type: application/x-www-form-urlencoded
       Body: cmd_0=onChange&uuid_0={textbox_id}&data_0={"value":"name",...}
             cmd_1=onClick&uuid_1={add_button_id}&data_1={...}

4. Выполнение загрузки в БД
   └─> POST /Uploader/zkau
       Content-Type: application/x-www-form-urlencoded
       Body: cmd_0=onClick&uuid_0={execute_button_id}&data_0={...}

5. Мониторинг результата
   └─> Логи отображаются в UI компоненте
       "Upload success"
       "start export to database"
       "Remove ANI in first line"
       "success insert"
```

## API Endpoints

### 1. GET /Uploader

**Назначение:** Получение главной страницы с UI компонентами

**Метод:** GET

**Параметры:** Нет

**Ответ:** HTML страница

**Важные элементы в HTML:**
```html
<!-- Textbox для ввода имени нотификации -->
<input id="hG9Pg" class="z-textbox" />

<!-- Кнопка добавления (зеленый плюс) -->
<button id="hG9Pi">Добавить</button>

<!-- Кнопка выполнения -->
<button id="hG9Po">Выполнить</button>

<!-- Desktop ID для ZK Framework -->
<script>
  var dtid = "z_1vi";
</script>
```

**Примечание:** UUID компонентов (`hG9Pg`, `hG9Pi`, `hG9Po`) генерируются динамически и меняются при каждой загрузке страницы.

---

### 2. POST /Uploader/zkau/upload

**Назначение:** Загрузка ZIP архива с CSV файлами

**Метод:** POST

**URL параметры:**
- `uuid` - UUID компонента загрузки файлов (извлекается из HTML)
- `dtid` - Desktop ID (извлекается из HTML)
- `sid` - Session ID (обычно "0")

**Headers:**
```
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary...
```

**Body:** Multipart form с ZIP файлом

**Пример запроса:**
```http
POST /Uploader/zkau/upload?uuid=hG9P9&dtid=z_1vi&sid=0 HTTP/1.1
Host: ivr-gui.mbrd.ru:8080
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="phonelist.zip"
Content-Type: application/zip

[binary ZIP data]
------WebKitFormBoundary--
```

**Ответ:**
```json
{
  "success": true
}
```

**Формат ZIP файла:**
- Содержит один или несколько CSV файлов
- Кодировка: UTF-8
- Формат номеров: `7XXXXXXXXXX` (российский формат с кодом страны)
- Пример содержимого CSV:
  ```
  79991234567
  79991234568
  79991234569
  ```

---

### 3. POST /Uploader/zkau (Создание нотификации)

**Назначение:** Создание нового имени списка (нотификации) и привязка к загруженному файлу

**Метод:** POST

**Headers:**
```
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
```

**Body Parameters:**
```
dtid={desktop_id}
cmd_0=onChange
uuid_0={textbox_uuid}
data_0={"value":"notification_name","start":0}
cmd_1=onClick
uuid_1={add_button_uuid}
data_1={"pageX":511,"pageY":87,"which":1,"x":5,"y":4}
```

**Пример запроса:**
```http
POST /Uploader/zkau HTTP/1.1
Host: ivr-gui.mbrd.ru:8080
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest

dtid=z_1vi&cmd_0=onChange&uuid_0=hG9Pg&data_0=%7B%22value%22%3A%22test_108%22%2C%22start%22%3A0%7D&cmd_1=onClick&uuid_1=hG9Pi&data_1=%7B%22pageX%22%3A511%2C%22pageY%22%3A87%2C%22which%22%3A1%2C%22x%22%3A5%2C%22y%22%3A4%7D
```

**Декодированные параметры:**
```
dtid=z_1vi
cmd_0=onChange
uuid_0=hG9Pg
data_0={"value":"test_108","start":0}
cmd_1=onClick
uuid_1=hG9Pi
data_1={"pageX":511,"pageY":87,"which":1,"x":5,"y":4}
```

**Ответ:**
```json
{
  "rs": [
    ["setAttr", {"$u":"hG9Pg"}, "_value", "test_108"],
    ["setAttr", {"$u":"hG9Pi"}, "disabled", false]
  ],
  "rid": 3
}
```

**Описание команд:**
- `cmd_0: onChange` - Изменение значения в textbox (ввод имени)
- `uuid_0` - ID textbox компонента
- `data_0.value` - Имя нотификации
- `cmd_1: onClick` - Клик на кнопку добавления
- `uuid_1` - ID кнопки добавления
- `data_1` - Координаты клика (можно использовать фиксированные значения)

---

### 4. POST /Uploader/zkau (Выполнение загрузки)

**Назначение:** Запуск процесса загрузки данных в Cassandra

**Метод:** POST

**Headers:**
```
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
```

**Body Parameters:**
```
dtid={desktop_id}
cmd_0=onClick
uuid_0={execute_button_uuid}
data_0={"pageX":100,"pageY":100,"which":1,"x":10,"y":10}
```

**Пример запроса:**
```http
POST /Uploader/zkau HTTP/1.1
Host: ivr-gui.mbrd.ru:8080
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest

dtid=z_1vi&cmd_0=onClick&uuid_0=hG9Po&data_0=%7B%22pageX%22%3A100%2C%22pageY%22%3A100%2C%22which%22%3A1%2C%22x%22%3A10%2C%22y%22%3A10%7D
```

**Ответ:**
```json
{
  "rs": [
    ["setAttr", {"$u":"hG9Pt"}, "_value", "14:43:04.077 success insert\n14:43:03.904 Remove ANI in first line\n14:43:03.904 start export to database\n14:41:54.742 Upload success\n14:41:54.742 Uploading...\n\null"],
    ["setAttr", {"$u":"hG9Po"}, "disabled", true]
  ],
  "rid": 5
}
```

**Логи выполнения:**
```
14:43:04.077 success insert
14:43:03.904 Remove ANI in first line
14:43:03.904 start export to database
14:41:54.742 Upload success
14:41:54.742 Uploading...
```

**Описание:**
- Сервер обрабатывает ZIP → извлекает CSV → удаляет ANI из первой строки → загружает в Cassandra
- Кнопка "Выполнить" блокируется (`disabled: true`) во время обработки
- Логи отображаются в реальном времени через обновления ZK Framework

---

## Извлечение Component UUIDs

### Метод 1: Регулярные выражения

```python
import re

# Textbox для имени нотификации
textbox = re.search(r'<input[^>]*id="([^"]+)"[^>]*class="[^"]*z-textbox', html)

# Кнопки
add_button = re.search(r'<button[^>]*id="([^"]+)"[^>]*>.*?добав', html, re.I)
exec_button = re.search(r'<button[^>]*id="([^"]+)"[^>]*>.*?выполн', html, re.I)

# Desktop ID
dtid = re.search(r'dtid["\s:=]+([a-zA-Z0-9_]+)', html)
```

### Метод 2: Парсинг HTML

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')

# Textbox
textbox = soup.find('input', class_=re.compile('z-textbox'))
textbox_id = textbox['id'] if textbox else None

# Кнопки по тексту
buttons = soup.find_all('button')
for btn in buttons:
    if 'добав' in btn.text.lower():
        add_button_id = btn['id']
    elif 'выполн' in btn.text.lower():
        exec_button_id = btn['id']
```

---

## Управление сессией

### Cookies

ZK Framework требует поддержки cookies для поддержания сессии:

```python
import requests

session = requests.Session()
response = session.get("http://ivr-gui.mbrd.ru:8080/Uploader")

# Session автоматически сохраняет cookies:
# - JSESSIONID
# - ZK Framework специфичные cookies
```

### Headers

Рекомендуемые headers для эмуляции браузера:

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
    'X-Requested-With': 'XMLHttpRequest'  # Для AJAX запросов
}
```

---

## Обработка ошибок

### HTTP Статусы

- `200 OK` - Успешная операция
- `301 Moved Permanently` - Редирект (при обращении к /Uploader без слэша)
- `400 Bad Request` - Неверные параметры
- `403 Forbidden` - Проблемы с аутентификацией/сессией
- `500 Internal Server Error` - Ошибка на сервере

### ZK Framework ошибки

Ответы могут содержать ошибки в JSON:

```json
{
  "error": "Session expired",
  "rid": 1
}
```

**Решение:** Переинициализировать сессию (GET /Uploader)

### Типичные проблемы

1. **Component UUID не найден**
   - Причина: Страница изменилась или неверный парсинг
   - Решение: Обновить регулярные выражения для поиска компонентов

2. **Session expired**
   - Причина: Cookies истекли или не сохранялись
   - Решение: Использовать `requests.Session()` для автоматического управления cookies

3. **Файл не загружается**
   - Причина: Неверный формат ZIP или кодировка CSV
   - Решение: Убедиться что CSV в UTF-8 и номера в формате 7XXXXXXXXXX

4. **Нотификация не создается**
   - Причина: Файл не был загружен перед созданием нотификации
   - Решение: Строго соблюдать порядок: upload → create → execute

---

## Безопасность

### Рекомендации

1. **Не выполнять destructive операции** без подтверждения
2. **Проверять существование списков** перед созданием (избежать дубликатов)
3. **Логировать все операции** для аудита
4. **Использовать timeout** для HTTP запросов

### Тестирование

Перед использованием в продакшн:

1. Тестировать на тестовых данных
2. Проверять логи на сервере после загрузки
3. Верифицировать данные в Cassandra
4. Тестировать обработку ошибок

---

## Примеры использования

### Пример 1: Загрузка одного списка

```python
from cassandra_uploader import CassandraUploader
from pathlib import Path

uploader = CassandraUploader()
zip_file = Path("phonelist_001.zip")
notification_name = "test_list_001"

success = uploader.upload_notification_list(zip_file, notification_name)
print(f"Результат: {'Успех' if success else 'Ошибка'}")
```

### Пример 2: Batch загрузка

```python
from cassandra_uploader import CassandraUploader
from pathlib import Path
import time

uploader = CassandraUploader()

# Список файлов для загрузки
uploads = [
    ("list_region_77.zip", "moscow_region"),
    ("list_region_78.zip", "spb_region"),
    ("list_region_50.zip", "mo_region"),
]

for zip_file, name in uploads:
    print(f"\n--- Загрузка {name} ---")
    success = uploader.upload_notification_list(Path(zip_file), name)

    if success:
        print(f"✓ {name} загружен успешно")
    else:
        print(f"✗ Ошибка загрузки {name}")

    # Задержка между загрузками
    time.sleep(5)
```

### Пример 3: Проверка перед загрузкой

```python
from cassandra_uploader import CassandraUploader
from pathlib import Path

def safe_upload(zip_path: Path, name: str):
    """Безопасная загрузка с проверками"""

    # Проверка файла
    if not zip_path.exists():
        print(f"Файл не найден: {zip_path}")
        return False

    if zip_path.stat().st_size > 100 * 1024 * 1024:  # 100 MB
        print(f"Файл слишком большой: {zip_path.stat().st_size / 1024 / 1024:.1f} MB")
        return False

    # Валидация имени
    if not name or len(name) < 3:
        print("Имя нотификации слишком короткое")
        return False

    # Загрузка
    uploader = CassandraUploader()
    return uploader.upload_notification_list(zip_path, name)

# Использование
safe_upload(Path("data.zip"), "campaign_001")
```

---

## Ограничения и особенности

### ZK Framework

1. **Динамические UUID** - Компоненты меняют ID при каждой загрузке страницы
2. **Stateful** - Требуется поддержка сессий и cookies
3. **AJAX-heavy** - Все операции идут через асинхронные запросы
4. **Серверный рендеринг** - Логика на сервере, клиент только отправляет команды

### Производительность

- **Размер файлов:** Рекомендуется до 50MB на ZIP
- **Количество номеров:** Оптимально до 1M номеров на список
- **Частота загрузок:** Рекомендуется интервал 5+ секунд между загрузками
- **Timeout обработки:** В среднем 2-10 секунд в зависимости от размера

### Cassandra

- **Формат данных:** После загрузки доступны через имя нотификации
- **Дубликаты:** Система не проверяет дубликаты имен автоматически
- **Удаление:** Через UI можно удалить список (кнопка удаления в выпадающем списке)

---

## FAQ

### Q: Можно ли загружать несколько файлов одновременно?

A: Нет, ZK Framework работает в рамках одной сессии. Нужно выполнять загрузки последовательно.

### Q: Как проверить, что данные загрузились в Cassandra?

A: После успешной загрузки имя нотификации появится в выпадающем списке на главной странице. Для прямой проверки в БД нужен доступ к CQL консоли.

### Q: Что делать если сессия истекла?

A: Переинициализировать uploader:
```python
uploader = CassandraUploader()
uploader.initialize()  # Создаст новую сессию
```

### Q: Поддерживаются ли другие форматы кроме ZIP?

A: Нет, система ожидает только ZIP архивы с CSV файлами внутри.

### Q: Какая кодировка должна быть у CSV?

A: Только UTF-8. Другие кодировки могут привести к ошибкам парсинга.

---

## Changelog

### v1.0 (2024-12-17)
- Начальная документация
- Полный анализ API через DevTools
- Python клиент для автоматизации
- Примеры использования

---

## Контакты и поддержка

Для вопросов по API обращайтесь к администраторам системы или в DevOps команду.

**Сервер:** `ivr-gui.mbrd.ru:8080`
**База данных:** Cassandra
**Framework:** ZK Framework (Java)
