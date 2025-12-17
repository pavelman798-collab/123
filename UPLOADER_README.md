# Cassandra Uploader - Автоматизация загрузки данных

Автоматизированный клиент для загрузки списков телефонных номеров в Cassandra через веб-интерфейс.

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements_uploader.txt
```

### 2. Подготовка данных

Создайте ZIP архив с CSV файлами:

```bash
# Пример структуры
phonelist.zip
├── list1.csv
├── list2.csv
└── list3.csv
```

**Формат CSV файлов:**
- Кодировка: UTF-8
- Один номер на строку
- Формат номера: `7XXXXXXXXXX` (11 цифр, начинается с 7)

Пример `list.csv`:
```
79991234567
79991234568
79991234569
```

### 3. Запуск

#### Вариант A: Простой пример

```python
from cassandra_uploader import CassandraUploader
from pathlib import Path

uploader = CassandraUploader()
success = uploader.upload_notification_list(
    Path("phonelist.zip"),
    "my_notification_name"
)
```

#### Вариант B: Интерактивный режим

```bash
python uploader_example.py
```

Выберите пункт 5 (Интерактивный режим) и следуйте инструкциям.

#### Вариант C: Прямой запуск

```bash
python cassandra_uploader.py
```

Отредактируйте функцию `main()` в файле, указав свои пути и имена.

## Использование

### Базовый пример

```python
from cassandra_uploader import CassandraUploader
from pathlib import Path

# Создание клиента
uploader = CassandraUploader(
    base_url="http://ivr-gui.mbrd.ru:8080/Uploader"
)

# Загрузка списка
zip_file = Path("data/phonelist_moscow.zip")
notification_name = "moscow_campaign_001"

success = uploader.upload_notification_list(zip_file, notification_name)

if success:
    print("Загрузка успешна!")
else:
    print("Ошибка загрузки")
```

### Пакетная загрузка

```python
from cassandra_uploader import CassandraUploader
from pathlib import Path
import time

uploads = [
    ("region_77.zip", "moscow_list"),
    ("region_78.zip", "spb_list"),
    ("region_50.zip", "mo_list"),
]

for zip_filename, name in uploads:
    uploader = CassandraUploader()
    success = uploader.upload_notification_list(Path(zip_filename), name)

    print(f"{name}: {'OK' if success else 'FAILED'}")
    time.sleep(5)  # Задержка между загрузками
```

### С валидацией

```python
from cassandra_uploader import CassandraUploader
from pathlib import Path
import re

def safe_upload(zip_path: Path, name: str):
    # Проверка файла
    if not zip_path.exists():
        return False, "Файл не найден"

    # Проверка размера (макс 100MB)
    if zip_path.stat().st_size > 100 * 1024 * 1024:
        return False, "Файл слишком большой"

    # Проверка имени (только буквы, цифры, _ и -)
    if not re.match(r'^[a-zA-Z0-9_-]{3,}$', name):
        return False, "Недопустимое имя"

    # Загрузка
    uploader = CassandraUploader()
    success = uploader.upload_notification_list(zip_path, name)

    return success, "OK" if success else "Ошибка загрузки"

# Использование
success, message = safe_upload(Path("data.zip"), "test_list")
print(message)
```

## Workflow загрузки

Процесс состоит из 4 этапов:

```
1. Инициализация
   └─> Загрузка страницы и извлечение component UUIDs

2. Загрузка ZIP файла
   └─> POST /Uploader/zkau/upload

3. Создание имени нотификации
   └─> POST /Uploader/zkau (onChange + onClick)

4. Выполнение загрузки в БД
   └─> POST /Uploader/zkau (onClick execute button)
```

Класс `CassandraUploader` автоматически выполняет все эти шаги.

## Примеры использования

Файл `uploader_example.py` содержит 5 готовых примеров:

1. **Загрузка одного списка** - базовый пример
2. **Пакетная загрузка** - несколько списков подряд
3. **Загрузка с валидацией** - проверка файлов перед загрузкой
4. **Пользовательская конфигурация** - настройка клиента
5. **Интерактивный режим** - запрос параметров у пользователя

Запуск примеров:

```bash
python uploader_example.py
```

## Структура проекта

```
.
├── cassandra_uploader.py        # Основной клиент
├── uploader_example.py          # Примеры использования
├── requirements_uploader.txt    # Зависимости
├── UPLOADER_README.md           # Этот файл
└── UPLOADER_API_DOCUMENTATION.md # Подробная документация API
```

## API клиента

### Класс CassandraUploader

#### `__init__(base_url: str)`

Создает экземпляр клиента.

**Параметры:**
- `base_url` - URL веб-интерфейса (по умолчанию: `http://ivr-gui.mbrd.ru:8080/Uploader`)

```python
uploader = CassandraUploader()
# или
uploader = CassandraUploader(base_url="http://custom-server:8080/Uploader")
```

#### `initialize() -> bool`

Инициализирует сессию и извлекает component UUIDs.

**Возвращает:** `True` если успешно, `False` если ошибка

```python
if uploader.initialize():
    print("Инициализация успешна")
```

#### `upload_file(zip_path: Path) -> Tuple[bool, Optional[str]]`

Загружает ZIP файл на сервер.

**Параметры:**
- `zip_path` - путь к ZIP архиву

**Возвращает:** `(success, upload_uuid)`

```python
success, uuid = uploader.upload_file(Path("data.zip"))
```

#### `create_notification(notification_name: str) -> bool`

Создает новое имя нотификации.

**Параметры:**
- `notification_name` - имя списка

**Возвращает:** `True` если успешно

```python
success = uploader.create_notification("my_list_001")
```

#### `execute_upload() -> bool`

Выполняет загрузку данных в БД.

**Возвращает:** `True` если успешно

```python
success = uploader.execute_upload()
```

#### `upload_notification_list(zip_path: Path, notification_name: str) -> bool`

**Главный метод** - выполняет полный цикл загрузки.

**Параметры:**
- `zip_path` - путь к ZIP файлу
- `notification_name` - имя нотификации

**Возвращает:** `True` если вся загрузка успешна

```python
success = uploader.upload_notification_list(
    Path("phonelist.zip"),
    "campaign_name"
)
```

## Обработка ошибок

```python
from cassandra_uploader import CassandraUploader
from pathlib import Path
import sys

try:
    uploader = CassandraUploader()
    success = uploader.upload_notification_list(
        Path("data.zip"),
        "list_name"
    )

    if not success:
        print("Ошибка загрузки", file=sys.stderr)
        sys.exit(1)

except FileNotFoundError:
    print("Файл не найден", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Неожиданная ошибка: {e}", file=sys.stderr)
    sys.exit(1)
```

## Логирование

Клиент выводит подробные логи в stdout:

```
[*] - информационные сообщения
[+] - успешные операции
[!] - ошибки и предупреждения
```

Пример вывода:

```
[*] Подключение к http://ivr-gui.mbrd.ru:8080/Uploader...
[*] Извлечение component IDs...
[+] Component IDs извлечены успешно:
    notification_textbox: hG9Pg
    add_button: hG9Pi
    execute_button: hG9Po
[+] Desktop ID: z_1vi
[*] Загрузка файла phonelist.zip...
[+] Файл загружен успешно
[*] Создание нотификации 'test_list'...
[+] Нотификация 'test_list' создана
[*] Выполнение загрузки в БД...
[+] Команда выполнения отправлена
[*] Ожидание завершения обработки...
[+] Обработка завершена успешно
[+] Список 'test_list' успешно загружен в БД!
```

## Частые вопросы

### Q: Можно ли загружать несколько списков параллельно?

A: Нет, ZK Framework использует stateful сессии. Загружайте списки последовательно с задержкой 3-5 секунд.

### Q: Какой максимальный размер файла?

A: Рекомендуется до 50-100 MB. Большие файлы могут вызвать timeout.

### Q: Как проверить что данные загрузились?

A: После успешной загрузки имя нотификации появится в выпадающем списке на веб-странице.

### Q: Что делать если загрузка зависла?

A: Перезапустите клиент. ZK Framework автоматически очистит незавершенную сессию.

### Q: Можно ли удалить загруженный список?

A: Да, через веб-интерфейс есть кнопка удаления в выпадающем списке.

## Ограничения

1. **Последовательная загрузка** - нельзя загружать параллельно
2. **Размер файлов** - рекомендуется до 100 MB
3. **Формат данных** - только ZIP с CSV в UTF-8
4. **Формат номеров** - только 7XXXXXXXXXX (11 цифр)
5. **Имена нотификаций** - только латиница, цифры, _, - (без пробелов и спецсимволов)

## Требования

- Python 3.7+
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0 (опционально, для парсинга HTML)
- Доступ к серверу `ivr-gui.mbrd.ru:8080`

## Безопасность

**Важно:**
- Не загружайте тестовые данные в продакшн БД
- Проверяйте содержимое ZIP файлов перед загрузкой
- Используйте уникальные имена нотификаций (избегайте перезаписи)
- Логируйте все операции для аудита

## Поддержка

Для вопросов по использованию:
1. Проверьте `UPLOADER_API_DOCUMENTATION.md` - подробная документация API
2. Изучите примеры в `uploader_example.py`
3. Проверьте логи клиента на наличие ошибок

## Changelog

**v1.0 (2024-12-17)**
- Начальная версия
- Полная автоматизация workflow
- 5 примеров использования
- Подробная документация

---

**Сервер:** http://ivr-gui.mbrd.ru:8080/Uploader
**База данных:** Cassandra
**Framework:** ZK Framework (Java)
