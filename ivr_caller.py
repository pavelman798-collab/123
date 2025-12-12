#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IVR Caller v4 — приложение для оповещения по IVR
С загрузкой сотрудников из PostgreSQL или PHP-страницы
"""

import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import urllib.error
import urllib.parse
import json
import os
import ssl
import re
import configparser
import http.cookiejar
from datetime import datetime

# Попытка импорта psycopg2
try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False
    print("⚠️ psycopg2 не установлен. БД недоступна.")


# ============== ПУТИ К ФАЙЛАМ ==============
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.ini")
CONNID_FILE = os.path.join(BASE_DIR, "connid.txt")
LOG_FILE = os.path.join(BASE_DIR, "ivr_log.txt")
HISTORY_FILE = os.path.join(BASE_DIR, "campaigns_history.json")
# ===========================================


# ============== ТИПЫ ОПОВЕЩЕНИЙ ==============
ALERT_TYPES = {
    "call": {
        "name": "📞 Позвонить",
        "service": "MONITOR_BANK",
        "monitor_bank_id": "1"
    },
    "call_sms": {
        "name": "📞📱 Позвонить и отправить СМС",
        "service": "MONITOR_BANK",
        "monitor_bank_id": "1"
    },
    "sms": {
        "name": "📱 Отправить СМС",
        "service": "MONITOR_BANK",
        "monitor_bank_id": "1"
    },
}
# =============================================


# ============== БЫСТРЫЕ СЦЕНАРИИ ==============
QUICK_SCENARIOS = {
    "critical_sboy": {
        "name": "🔴 Критичный сбой",
        "description": "Руководство + IT",
        "color": "#e74c3c",
        "alert_type": "sboy",
        "employee_ids": [531, 533, 534]  # ID из БД/PHP
    },
    "daily_metrics": {
        "name": "📊 Ежедневные метрики",
        "description": "Аналитики",
        "color": "#3498db",
        "alert_type": "metrika",
        "employee_ids": [535, 536]
    },
    "tech_maintenance": {
        "name": "🔧 Плановые работы",
        "description": "IT-отдел полностью",
        "color": "#f39c12",
        "alert_type": "tech_work",
        "employee_ids": [531, 533, 537, 538]
    },
    "security_alert": {
        "name": "🔒 Инцидент ИБ",
        "description": "Безопасность + Рук-во",
        "color": "#9b59b6",
        "alert_type": "security",
        "employee_ids": [539, 540, 531]
    },
}
# =============================================


# ============== ТЕСТОВЫЕ ДАННЫЕ ==============
FALLBACK_EMPLOYEES = {
    531: {"name": "Горбачев Иван Геннадиевич", "phone": "+79991111111"},
    533: {"name": "Петрова Анна Сергеевна", "phone": "+79992222222"},
    534: {"name": "Сидоров Петр Михайлович", "phone": "+79993333333"},
    535: {"name": "Козлова Мария Александровна", "phone": "+79994444444"},
    536: {"name": "Смирнов Алексей Владимирович", "phone": "+79995555555"},
    537: {"name": "Кузнецова Елена Игоревна", "phone": "+79996666666"},
    538: {"name": "Новиков Дмитрий Олегович", "phone": "+79997777777"},
    539: {"name": "Морозова Ольга Викторовна", "phone": "+79998888888"},
    540: {"name": "Волков Сергей Николаевич", "phone": "+79999999999"},
}
# =============================================


class Config:
    """Работа с конфигурацией"""

    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config_path = config_path
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            self.config.read(self.config_path, encoding='utf-8')
        else:
            print(f"⚠️ Конфиг не найден: {self.config_path}")
            self._create_default()

    def _create_default(self):
        self.config['database'] = {
            'host': 'localhost', 'port': '5432',
            'database': 'monitoring', 'user': 'user', 'password': 'password'
        }
        self.config['php_source'] = {
            'base_url': 'https://help-monitoring.mbrd.ru',
            'login_url': '/admin/index.php',
            'employees_url': '/admin/people.php',
            'username': 'admin', 'password': 'password'
        }
        self.config['api'] = {'url': 'https://your-api/call'}
        self.config['settings'] = {
            'data_source': 'auto', 'db_timeout': '10',
            'api_timeout': '30', 'php_timeout': '30', 'verify_ssl': 'false'
        }
        with open(self.config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)
        print(f"✅ Создан конфиг: {self.config_path}")

    @property
    def db_params(self):
        return {
            'host': self.config.get('database', 'host'),
            'port': self.config.getint('database', 'port'),
            'database': self.config.get('database', 'database'),
            'user': self.config.get('database', 'user'),
            'password': self.config.get('database', 'password'),
        }

    @property
    def php_params(self):
        return {
            'base_url': self.config.get('php_source', 'base_url'),
            'login_url': self.config.get('php_source', 'login_url'),
            'employees_url': self.config.get('php_source', 'employees_url'),
            'username': self.config.get('php_source', 'username'),
            'password': self.config.get('php_source', 'password'),
        }

    @property
    def api_url(self):
        return self.config.get('api', 'url')

    @property
    def data_source(self):
        return self.config.get('settings', 'data_source', fallback='auto')

    @property
    def api_timeout(self):
        return self.config.getint('settings', 'api_timeout', fallback=30)

    @property
    def php_timeout(self):
        return self.config.getint('settings', 'php_timeout', fallback=30)

    @property
    def verify_ssl(self):
        return self.config.getboolean('settings', 'verify_ssl', fallback=False)


class DatabaseManager:
    """Работа с PostgreSQL"""

    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        if not HAS_PSYCOPG2:
            return False
        try:
            self.connection = psycopg2.connect(
                host=self.config.db_params['host'],
                port=self.config.db_params['port'],
                database=self.config.db_params['database'],
                user=self.config.db_params['user'],
                password=self.config.db_params['password'],
                connect_timeout=10
            )
            print("✅ PostgreSQL подключен")
            return True
        except Exception as e:
            print(f"❌ PostgreSQL ошибка: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def load_employees(self):
        if not self.connection:
            return {}

        employees = {}
        try:
            cursor = self.connection.cursor()

            # ========== SQL ЗАПРОС — ПОПРАВЬТЕ ПОД ВАШУ СТРУКТУРУ ==========
            query = """
                SELECT
                    id,
                    surname,
                    name,
                    patronymic,
                    phone
                FROM employees
                WHERE is_active = true
                  AND phone IS NOT NULL
                  AND phone != ''
                ORDER BY surname, name
            """
            # ================================================================

            cursor.execute(query)
            for row in cursor.fetchall():
                emp_id, surname, name, patronymic, phone = row
                fio = ' '.join(filter(None, [surname, name, patronymic]))
                phone = self._normalize_phone(phone)
                if fio and phone:
                    employees[emp_id] = {"name": fio, "phone": phone}

            cursor.close()
            print(f"✅ Из БД загружено: {len(employees)} сотрудников")
        except Exception as e:
            print(f"❌ Ошибка загрузки из БД: {e}")

        return employees

    def _normalize_phone(self, phone):
        if not phone:
            return ""
        phone = re.sub(r'[^\d+]', '', phone)
        if phone.startswith('8') and len(phone) == 11:
            phone = '+7' + phone[1:]
        elif phone.startswith('7') and len(phone) == 11:
            phone = '+' + phone
        return phone


class PHPParser:
    """Парсинг сотрудников с PHP-страницы"""

    def __init__(self, config):
        self.config = config
        self.cookies = http.cookiejar.CookieJar()
        self.opener = None
        self.debug_log = []  # Лог для отладки
        self._setup_opener()

    def _log(self, message):
        """Добавление в лог"""
        print(message)
        self.debug_log.append(message)

    def _setup_opener(self):
        """Настройка opener с поддержкой cookies и SSL"""
        cookie_handler = urllib.request.HTTPCookieProcessor(self.cookies)

        # SSL контекст
        ssl_context = ssl.create_default_context()
        if not self.config.verify_ssl:
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        https_handler = urllib.request.HTTPSHandler(context=ssl_context)
        self.opener = urllib.request.build_opener(cookie_handler, https_handler)

    def _login(self):
        """Авторизация на PHP-странице"""
        params = self.config.php_params

        self._log("=" * 50)
        self._log("🔐 ЭТАП 1: Авторизация")
        self._log("=" * 50)
        self._log(f"   Base URL: {params['base_url']}")
        self._log(f"   Login URL: {params['login_url']}")
        self._log(f"   Полный URL: {params['base_url'] + params['login_url']}")
        self._log(f"   Username: {params['username']}")
        self._log(f"   Password: {'*' * len(params['password'])}")

        login_url = params['base_url'] + params['login_url']

        # Сначала GET запрос на страницу логина (ОБЯЗАТЕЛЬНО для получения PHPSESSID)
        self._log("")
        self._log("📡 Шаг 1.1: GET запрос на страницу логина (получение PHPSESSID)...")
        phpsessid = None
        try:
            get_request = urllib.request.Request(
                login_url,
                method='GET',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'ru,en;q=0.9',
                }
            )
            get_response = self.opener.open(get_request, timeout=self.config.php_timeout)
            get_status = get_response.getcode()
            get_url_final = get_response.geturl()
            get_response.read()  # Читаем ответ чтобы закрыть соединение

            self._log(f"   ✅ GET успешен")
            self._log(f"   Статус: {get_status}")
            self._log(f"   Итоговый URL: {get_url_final}")
            self._log(f"   Cookies получены: {len(self.cookies)}")
            for cookie in self.cookies:
                self._log(f"      - {cookie.name}: {cookie.value}")
                if cookie.name == 'PHPSESSID':
                    phpsessid = cookie.value

            if phpsessid:
                self._log(f"   ✅ PHPSESSID получен: {phpsessid}")
            else:
                self._log(f"   ⚠️ PHPSESSID не найден в cookies!")

        except urllib.error.HTTPError as e:
            self._log(f"   ❌ GET ошибка HTTP: {e.code} {e.reason}")
            self._log(f"   URL: {e.geturl()}")
            return False
        except Exception as e:
            self._log(f"   ❌ GET ошибка: {type(e).__name__}: {e}")
            return False

        # Данные для логина
        login_data = urllib.parse.urlencode({
            'client_name': params['username'],
            'client_pass': params['password']
        }).encode('utf-8')

        self._log("")
        self._log("📡 Шаг 1.2: POST запрос для авторизации...")
        self._log(f"   Данные: client_name={params['username']}&client_pass=***")

        try:
            request = urllib.request.Request(
                login_url,
                data=login_data,
                method='POST',
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'ru,en;q=0.9',
                    'Origin': params['base_url'],
                    'Referer': login_url,
                    'Cache-Control': 'max-age=0',
                }
            )

            response = self.opener.open(request, timeout=self.config.php_timeout)
            status = response.getcode()
            final_url = response.geturl()
            html = response.read().decode('utf-8', errors='ignore')

            self._log(f"   ✅ POST успешен")
            self._log(f"   Статус: {status}")
            self._log(f"   Итоговый URL (после редиректа): {final_url}")
            self._log(f"   Размер ответа: {len(html)} символов")
            self._log(f"   Cookies после логина: {len(self.cookies)}")

            # Показываем все cookies
            for cookie in self.cookies:
                self._log(f"      - {cookie.name}: {cookie.value}")

            # Показываем начало HTML ответа для диагностики
            self._log(f"   ")
            self._log(f"   📄 HTML ответа (первые 800 символов):")
            self._log(f"   {html[:800]}")
            self._log(f"   ")

            # Проверяем, успешен ли логин (ищем признаки)
            if 'logout' in html.lower() or 'выход' in html.lower() or 'exit' in html.lower():
                self._log("   ✅ Найден признак успешного логина (logout/выход)")
            elif 'error' in html.lower() or 'ошибка' in html.lower() or 'неверн' in html.lower():
                self._log("   ⚠️ Возможно ошибка авторизации (найдено слово error/ошибка)")
                self._log(f"   Первые 500 символов ответа:")
                self._log(f"   {html[:500]}")
                return False
            elif params['login_url'] in final_url:
                self._log("   ⚠️ Остались на странице логина — возможно неверные креды")
                return False
            else:
                self._log("   ✅ Предполагаем успешный логин (редирект произошёл)")

            # Шаг 1.3: Заходим на main.php чтобы активировать сессию
            self._log("")
            self._log("📡 Шаг 1.3: GET запрос на main.php (активация сессии)...")
            try:
                main_url = params['base_url'] + '/admin/main.php'
                main_request = urllib.request.Request(
                    main_url,
                    method='GET',
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Referer': login_url
                    }
                )
                main_response = self.opener.open(main_request, timeout=self.config.php_timeout)
                main_status = main_response.getcode()
                main_html = main_response.read().decode('utf-8', errors='ignore')
                self._log(f"   ✅ main.php загружен, статус: {main_status}")
                self._log(f"   Размер: {len(main_html)} символов")

                # Проверяем что мы залогинены
                if 'logout' in main_html.lower() or 'выход' in main_html.lower():
                    self._log("   ✅ Сессия активна (найден logout)")
                    return True
                elif 'locked' in main_html.lower() or 'access' in main_html.lower():
                    self._log("   ❌ Доступ закрыт")
                    return False
                else:
                    self._log("   ✅ Предполагаем что сессия активна")
                    return True

            except Exception as e:
                self._log(f"   ⚠️ Ошибка main.php: {e}")
                # Продолжаем всё равно — может сработает
                return True

        except urllib.error.HTTPError as e:
            self._log(f"   ❌ HTTP ошибка: {e.code} {e.reason}")
            self._log(f"   URL: {e.geturl()}")
            if e.code == 404:
                self._log("   💡 404 = страница не найдена. Проверьте login_url в config.ini")
            elif e.code == 403:
                self._log("   💡 403 = доступ запрещён. Возможно нужна VPN или IP в whitelist")
            elif e.code == 401:
                self._log("   💡 401 = требуется авторизация. Возможно Basic Auth?")
            return False

        except urllib.error.URLError as e:
            self._log(f"   ❌ URL ошибка: {e.reason}")
            self._log("   💡 Проверьте: доступен ли сайт? Правильный ли base_url?")
            return False

        except Exception as e:
            self._log(f"   ❌ Неизвестная ошибка: {type(e).__name__}: {e}")
            return False

    def load_employees(self):
        """Загрузка и парсинг списка сотрудников"""
        if not self._login():
            self._log("")
            self._log("❌ Авторизация не удалась, загрузка сотрудников отменена")
            return {}

        params = self.config.php_params
        employees_url = params['base_url'] + params['employees_url']

        self._log("")
        self._log("=" * 50)
        self._log("📋 ЭТАП 2: Загрузка списка сотрудников")
        self._log("=" * 50)
        self._log(f"   Employees URL: {params['employees_url']}")
        self._log(f"   Полный URL: {employees_url}")

        try:
            request = urllib.request.Request(
                employees_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': params['base_url'] + params['login_url']
                }
            )

            response = self.opener.open(request, timeout=self.config.php_timeout)
            status = response.getcode()
            final_url = response.geturl()
            html = response.read().decode('utf-8', errors='ignore')

            self._log(f"   ✅ GET успешен")
            self._log(f"   Статус: {status}")
            self._log(f"   Итоговый URL: {final_url}")
            self._log(f"   Размер HTML: {len(html)} символов")

            # Проверяем, не редиректнуло ли на логин
            if 'login' in final_url.lower() or 'client_name' in html:
                self._log("   ⚠️ Похоже нас редиректнуло на страницу логина!")
                self._log("   💡 Сессия не сохранилась. Возможные причины:")
                self._log("      - Неверные креды")
                self._log("      - Сайт не принимает cookies")
                self._log("      - Нужен другой механизм авторизации")
                return {}

            # Проверяем наличие таблицы
            if '<table' in html.lower():
                self._log(f"   ✅ Таблица найдена в HTML")
            else:
                self._log(f"   ⚠️ Таблица НЕ найдена в HTML!")
                self._log(f"   Первые 1000 символов:")
                self._log(f"   {html[:1000]}")

            employees = self._parse_html(html)

            self._log("")
            self._log("=" * 50)
            self._log(f"📊 ИТОГ: Загружено {len(employees)} сотрудников")
            self._log("=" * 50)

            if employees:
                # Показываем первых 3 для проверки
                self._log("   Примеры:")
                for i, (emp_id, emp) in enumerate(list(employees.items())[:3]):
                    self._log(f"      {emp_id}: {emp['name']} | {emp['phone']}")

            return employees

        except urllib.error.HTTPError as e:
            self._log(f"   ❌ HTTP ошибка: {e.code} {e.reason}")
            if e.code == 404:
                self._log("   💡 404 = страница не найдена. Проверьте employees_url")
            elif e.code == 403:
                self._log("   💡 403 = доступ запрещён после логина")
            return {}

        except Exception as e:
            self._log(f"   ❌ Ошибка: {type(e).__name__}: {e}")
            return {}

    def _parse_html(self, html):
        """Парсинг HTML-таблицы"""
        employees = {}

        # Диагностика
        self._log("")
        self._log("🔍 ПАРСИНГ HTML:")
        self._log(f"   Размер HTML: {len(html)} символов")

        # Ищем строки таблицы
        row_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
        cell_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL | re.IGNORECASE)

        all_rows = row_pattern.findall(html)
        self._log(f"   Найдено строк <tr>: {len(all_rows)}")

        rows_with_6_cells = 0
        rows_with_id = 0
        rows_with_phone = 0
        skipped_no_phone = 0
        skipped_bad_phone = 0

        for row_html in all_rows:
            cells = cell_pattern.findall(row_html)

            if len(cells) >= 6:
                rows_with_6_cells += 1
                clean_cells = [self._strip_html(cell).strip() for cell in cells]

                try:
                    emp_id = int(clean_cells[0])
                    rows_with_id += 1
                except ValueError:
                    continue

                surname = clean_cells[2] if len(clean_cells) > 2 else ""
                name = clean_cells[3] if len(clean_cells) > 3 else ""
                patronymic = clean_cells[4] if len(clean_cells) > 4 else ""
                phone_raw = clean_cells[5] if len(clean_cells) > 5 else ""

                fio = ' '.join(filter(None, [surname, name, patronymic]))
                phone = self._normalize_phone(phone_raw)

                if not phone_raw:
                    skipped_no_phone += 1
                    continue

                if not phone:
                    skipped_bad_phone += 1
                    # Показываем первые 5 примеров "плохих" телефонов
                    if skipped_bad_phone <= 5:
                        self._log(f"      ⚠️ Пропущен телефон: '{phone_raw}' (ID={emp_id}, {surname})")
                    continue

                if fio and phone:
                    rows_with_phone += 1
                    employees[emp_id] = {"name": fio, "phone": phone}
                elif phone and not fio:
                    skipped_no_fio = skipped_no_fio + 1 if 'skipped_no_fio' in dir() else 1
                    if skipped_no_fio <= 5:
                        self._log(f"      ⚠️ Есть телефон, но нет ФИО:")
                        self._log(f"         ID={emp_id}")
                        self._log(f"         Ячейка[2] (фамилия): '{clean_cells[2] if len(clean_cells) > 2 else 'НЕТ'}'")
                        self._log(f"         Ячейка[3] (имя): '{clean_cells[3] if len(clean_cells) > 3 else 'НЕТ'}'")
                        self._log(f"         Ячейка[4] (отчество): '{clean_cells[4] if len(clean_cells) > 4 else 'НЕТ'}'")
                        self._log(f"         Ячейка[5] (телефон): '{clean_cells[5] if len(clean_cells) > 5 else 'НЕТ'}'")
                        self._log(f"         phone_raw: '{phone_raw}'")
                        self._log(f"         phone после нормализации: '{phone}'")

        # Считаем пропущенных без ФИО
        skipped_no_fio_count = rows_with_id - skipped_no_phone - skipped_bad_phone - rows_with_phone

        self._log(f"   Строк с 6+ ячейками: {rows_with_6_cells}")
        self._log(f"   Строк с числовым ID: {rows_with_id}")
        self._log(f"   Пропущено (нет телефона): {skipped_no_phone}")
        self._log(f"   Пропущено (плохой формат телефона): {skipped_bad_phone}")
        self._log(f"   Пропущено (есть телефон, нет ФИО): {skipped_no_fio_count}")
        self._log(f"   ✅ Сотрудников с телефоном: {rows_with_phone}")

        return employees

    def _strip_html(self, text):
        """Удаление HTML-тегов"""
        return re.sub(r'<[^>]+>', '', text)

    def _normalize_phone(self, phone):
        """Нормализация номера телефона"""
        if not phone:
            return ""

        # Убираем всё кроме цифр и +
        phone = re.sub(r'[^\d+]', '', phone)

        # Пустой после очистки
        if not phone:
            return ""

        # Если только цифры без +
        digits_only = re.sub(r'\D', '', phone)

        # Если 11 цифр и начинается с 8 → меняем на +7
        if len(digits_only) == 11 and digits_only.startswith('8'):
            return '+7' + digits_only[1:]

        # Если 11 цифр и начинается с 7 → добавляем +
        if len(digits_only) == 11 and digits_only.startswith('7'):
            return '+' + digits_only

        # Если 10 цифр (без кода страны) → добавляем +7
        if len(digits_only) == 10:
            return '+7' + digits_only

        # Если уже начинается с + и достаточно цифр → оставляем
        if phone.startswith('+') and len(digits_only) >= 10:
            return phone

        # Если 11+ цифр без + → добавляем +
        if len(digits_only) >= 11:
            return '+' + digits_only

        # Всё остальное — возвращаем как есть, если есть хоть 6 цифр (короткие номера)
        if len(digits_only) >= 6:
            return '+' + digits_only if not phone.startswith('+') else phone

        return ""


class DataLoader:
    """Загрузчик данных с fallback"""

    def __init__(self, config):
        self.config = config
        self.db = DatabaseManager(config)
        self.php = PHPParser(config)
        self.source_used = "none"

    def load_employees(self):
        """Загрузка сотрудников с автоматическим fallback"""
        data_source = self.config.data_source

        if data_source == 'auto':
            # Сначала БД, потом PHP, потом fallback
            employees = self._try_database()
            if employees:
                return employees

            employees = self._try_php()
            if employees:
                return employees

            return self._use_fallback()

        elif data_source == 'db':
            employees = self._try_database()
            return employees if employees else self._use_fallback()

        elif data_source == 'php':
            employees = self._try_php()
            return employees if employees else self._use_fallback()

        else:
            return self._use_fallback()

    def _try_database(self):
        """Попытка загрузки из БД"""
        print("🔄 Попытка загрузки из PostgreSQL...")
        if self.db.connect():
            employees = self.db.load_employees()
            if employees:
                self.source_used = "PostgreSQL"
                return employees
            self.db.disconnect()
        return {}

    def _try_php(self):
        """Попытка загрузки из PHP"""
        print("🔄 Попытка загрузки из PHP...")
        employees = self.php.load_employees()
        if employees:
            self.source_used = "PHP"
            return employees
        return {}

    def _use_fallback(self):
        """Использование тестовых данных"""
        print("⚠️ Используются тестовые данные")
        self.source_used = "Тестовые данные"
        return FALLBACK_EMPLOYEES.copy()

    def disconnect(self):
        """Отключение от источников"""
        self.db.disconnect()


class IVRCallerApp:
    """Основное приложение"""

    def __init__(self, root):
        self.root = root
        self.root.title("📞 IVR Оповещения v4")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        self.root.minsize(650, 550)

        # Конфигурация
        self.config = Config(CONFIG_FILE)

        # Загрузчик данных
        self.data_loader = DataLoader(self.config)

        # Загрузка сотрудников
        self.employees = self.data_loader.load_employees()
        self.data_source = self.data_loader.source_used

        # CONNID
        self.current_connid = self._load_connid()

        # UI переменные
        self.employee_vars = {}
        self.selected_alert_type = tk.StringVar(value="call")

        self.setup_ui()
        self.center_window()

    def _load_connid(self):
        try:
            if os.path.exists(CONNID_FILE):
                with open(CONNID_FILE, "r") as f:
                    return int(f.read().strip())
        except (ValueError, IOError):
            pass
        return 1000000

    def _save_connid(self):
        try:
            with open(CONNID_FILE, "w") as f:
                f.write(str(self.current_connid))
        except IOError:
            pass

    def _log_action(self, action, details):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {action}: {details}\n")
        except IOError:
            pass

    def center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"+{x}+{y}")

    def setup_ui(self):
        # Верхняя панель
        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

        source_icon = "✅" if self.data_source != "Тестовые данные" else "⚠️"
        ttk.Label(
            info_frame,
            text=f"{source_icon} Источник: {self.data_source} | Сотрудников: {len(self.employees)}",
            font=("Segoe UI", 9),
            foreground="gray"
        ).pack(side=tk.LEFT)

        ttk.Button(
            info_frame, text="🔄 Обновить",
            command=self.refresh_employees, width=12
        ).pack(side=tk.RIGHT)

        # Вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.constructor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.constructor_frame, text="📝 Конструктор")
        self.setup_constructor_tab()

        self.scenarios_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scenarios_frame, text="⚡ Быстрые сценарии")
        self.setup_scenarios_tab()

        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📜 История")
        self.setup_history_tab()

        # Статус-бар
        self.status_label = ttk.Label(
            self.root,
            text=f"CONNID: {self.current_connid} | Готов к работе",
            font=("Segoe UI", 9), foreground="gray"
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

    def setup_constructor_tab(self):
        # Инициализация списка номеров
        self.file_phones = []

        # Создаем Canvas с прокруткой для длинного содержимого
        canvas = tk.Canvas(self.constructor_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.constructor_frame, orient="vertical", command=canvas.yview)

        # Внутренний фрейм для содержимого
        frame_inner = ttk.Frame(canvas)

        # Конфигурация прокрутки
        frame_inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=frame_inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Размещение элементов
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Прокрутка колесиком мыши
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Тип оповещения
        alert_frame = ttk.LabelFrame(frame_inner, text="Шаг 1: Тип оповещения", padding="10")
        alert_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        col_idx = 0
        for key, alert in ALERT_TYPES.items():
            ttk.Radiobutton(
                alert_frame, text=alert["name"],
                value=key, variable=self.selected_alert_type
            ).grid(row=0, column=col_idx, padx=10, pady=5, sticky=tk.W)
            col_idx += 1

        # Добавляем trace для отслеживания изменений типа оповещения
        self.selected_alert_type.trace("w", self.toggle_text_fields)

        # Текстовые поля
        text_frame = ttk.LabelFrame(frame_inner, text="Шаг 2: Содержимое сообщений", padding="10")
        text_frame.pack(fill=tk.X, padx=10, pady=5)

        # Поле для озвучивания
        ttk.Label(
            text_frame,
            text="📞 Текст для озвучивания при звонке:",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor=tk.W, pady=(5, 2))

        ttk.Label(
            text_frame,
            text="💡 Этот текст будет произнесён роботом при звонке получателю",
            font=("Segoe UI", 9),
            foreground="gray"
        ).pack(anchor=tk.W, pady=(0, 5))

        self.voice_text = tk.Text(text_frame, height=4, font=("Segoe UI", 10), wrap=tk.WORD)
        self.voice_text.pack(fill=tk.X, pady=(0, 15))

        # Поле для СМС
        ttk.Label(
            text_frame,
            text="📱 Текст для СМС:",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor=tk.W, pady=(5, 2))

        ttk.Label(
            text_frame,
            text="💡 Этот текст будет отправлен в виде SMS-сообщения",
            font=("Segoe UI", 9),
            foreground="gray"
        ).pack(anchor=tk.W, pady=(0, 5))

        self.sms_text = tk.Text(text_frame, height=4, font=("Segoe UI", 10), wrap=tk.WORD)
        self.sms_text.pack(fill=tk.X)

        # Загрузка номеров из файла
        file_load_frame = ttk.LabelFrame(frame_inner, text="Шаг 3: Загрузка номеров телефонов", padding="10")
        file_load_frame.pack(fill=tk.X, padx=10, pady=5)

        # Кнопки загрузки
        btn_frame = ttk.Frame(file_load_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            btn_frame, text="📂 Выбрать TXT файл",
            command=self.load_phones_from_file, width=20
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            btn_frame, text="🗑️ Очистить список",
            command=self.clear_file_phones, width=15
        ).pack(side=tk.LEFT)

        self.file_count_label = ttk.Label(
            btn_frame, text="Загружено: 0 номеров",
            font=("Segoe UI", 10, "bold")
        )
        self.file_count_label.pack(side=tk.RIGHT)

        # Список номеров
        list_frame = ttk.Frame(file_load_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.phones_listbox = tk.Listbox(
            list_frame, font=("Consolas", 10),
            selectmode=tk.EXTENDED, height=6
        )
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.phones_listbox.yview)
        self.phones_listbox.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.phones_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Подсказка
        ttk.Label(
            file_load_frame,
            text="💡 Формат файла: один номер на строку (+79991234567)",
            font=("Segoe UI", 9), foreground="gray"
        ).pack(anchor=tk.W, pady=(5, 0))

        # Шаг 4: Параметры кампании
        params_frame = ttk.LabelFrame(frame_inner, text="Шаг 4: Параметры кампании", padding="10")
        params_frame.pack(fill=tk.X, padx=10, pady=5)

        # Номер отправителя
        sender_frame = ttk.Frame(params_frame)
        sender_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            sender_frame,
            text="Телефонный номер отправителя:",
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.sender_phone = tk.StringVar()
        sender_entry = ttk.Entry(sender_frame, textvariable=self.sender_phone, width=20, font=("Consolas", 10))
        sender_entry.pack(side=tk.LEFT)

        self.sender_validation_label = ttk.Label(sender_frame, text="", font=("Segoe UI", 9), foreground="red")
        self.sender_validation_label.pack(side=tk.LEFT, padx=(10, 0))

        # Валидация номера отправителя
        self.sender_phone.trace("w", self.validate_sender_phone)

        ttk.Label(
            params_frame,
            text="💡 11 цифр, начинается с 7 (например: 79991234567)",
            font=("Segoe UI", 9),
            foreground="gray"
        ).pack(anchor=tk.W, pady=(0, 10))

        # Номер шаблона СМС
        template_frame = ttk.Frame(params_frame)
        template_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            template_frame,
            text="Номер шаблона СМС:",
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.sms_template = tk.StringVar()
        ttk.Entry(template_frame, textvariable=self.sms_template, width=20, font=("Consolas", 10)).pack(side=tk.LEFT)

        # Отложенная отправка
        delayed_frame = ttk.Frame(params_frame)
        delayed_frame.pack(fill=tk.X, pady=(5, 0))

        self.delayed_send = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            delayed_frame,
            text="Отложенная отправка",
            variable=self.delayed_send,
            command=self.toggle_delayed_send
        ).pack(side=tk.LEFT)

        # Поля для даты и времени
        datetime_frame = ttk.Frame(params_frame)
        datetime_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Label(datetime_frame, text="Дата:").pack(side=tk.LEFT, padx=(20, 5))
        self.send_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.date_entry = ttk.Entry(datetime_frame, textvariable=self.send_date, width=12, font=("Consolas", 10))
        self.date_entry.pack(side=tk.LEFT, padx=(0, 15))
        self.date_entry.config(state='disabled')

        ttk.Label(datetime_frame, text="Время:").pack(side=tk.LEFT, padx=(0, 5))
        self.send_time = tk.StringVar(value="12:00")
        self.time_entry = ttk.Entry(datetime_frame, textvariable=self.send_time, width=8, font=("Consolas", 10))
        self.time_entry.pack(side=tk.LEFT)
        self.time_entry.config(state='disabled')

        ttk.Label(
            params_frame,
            text="💡 Формат даты: ГГГГ-ММ-ДД, времени: ЧЧ:ММ",
            font=("Segoe UI", 9),
            foreground="gray"
        ).pack(anchor=tk.W, pady=(5, 0))

        # Нижняя панель - кнопка отправки
        bottom_frame = ttk.Frame(frame_inner)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            bottom_frame, text="🚀 Отправить оповещения",
            command=self.send_constructor_alerts
        ).pack(side=tk.RIGHT, ipady=5, ipadx=20)

        # Инициализируем состояние полей
        self.toggle_text_fields()

    def toggle_text_fields(self, *args):
        """Включение/выключение текстовых полей в зависимости от типа оповещения"""
        alert_type = self.selected_alert_type.get()

        if alert_type == "call":
            # Позвонить - только поле озвучивания
            self.voice_text.config(state='normal', bg='white')
            self.sms_text.config(state='disabled', bg='#f0f0f0')
        elif alert_type == "sms":
            # Отправить СМС - только поле СМС
            self.voice_text.config(state='disabled', bg='#f0f0f0')
            self.sms_text.config(state='normal', bg='white')
        elif alert_type == "call_sms":
            # Позвонить и отправить СМС - оба поля
            self.voice_text.config(state='normal', bg='white')
            self.sms_text.config(state='normal', bg='white')

    def validate_sender_phone(self, *args):
        """Валидация номера отправителя"""
        phone = self.sender_phone.get()

        if not phone:
            self.sender_validation_label.config(text="")
            return

        # Проверка: только цифры
        if not phone.isdigit():
            self.sender_validation_label.config(text="❌ Только цифры", foreground="red")
            return

        # Проверка: 11 цифр
        if len(phone) != 11:
            self.sender_validation_label.config(text=f"❌ {len(phone)}/11 цифр", foreground="orange")
            return

        # Проверка: начинается с 7
        if not phone.startswith('7'):
            self.sender_validation_label.config(text="❌ Должен начинаться с 7", foreground="red")
            return

        # Всё ок
        self.sender_validation_label.config(text="✅ OK", foreground="green")

    def toggle_delayed_send(self):
        """Включение/выключение полей даты и времени"""
        if self.delayed_send.get():
            self.date_entry.config(state='normal')
            self.time_entry.config(state='normal')
        else:
            self.date_entry.config(state='disabled')
            self.time_entry.config(state='disabled')

    def setup_history_tab(self):
        """Вкладка истории кампаний"""
        # Заголовок
        ttk.Label(
            self.history_frame,
            text="История запуска кампаний",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(10, 5))

        # Кнопка обновления
        btn_frame = ttk.Frame(self.history_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(
            btn_frame, text="🔄 Обновить",
            command=self.refresh_history, width=12
        ).pack(side=tk.RIGHT)

        # Таблица (Treeview)
        tree_frame = ttk.Frame(self.history_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview
        columns = ("status", "date", "type", "phones", "success", "fail")
        self.history_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        scrollbar.config(command=self.history_tree.yview)

        # Заголовки колонок
        self.history_tree.heading("status", text="Статус")
        self.history_tree.heading("date", text="Дата и время")
        self.history_tree.heading("type", text="Тип")
        self.history_tree.heading("phones", text="Всего номеров")
        self.history_tree.heading("success", text="Успешно")
        self.history_tree.heading("fail", text="Ошибок")

        # Ширина колонок
        self.history_tree.column("status", width=100, anchor=tk.CENTER)
        self.history_tree.column("date", width=180, anchor=tk.CENTER)
        self.history_tree.column("type", width=200, anchor=tk.W)
        self.history_tree.column("phones", width=120, anchor=tk.CENTER)
        self.history_tree.column("success", width=100, anchor=tk.CENTER)
        self.history_tree.column("fail", width=100, anchor=tk.CENTER)

        self.history_tree.pack(fill=tk.BOTH, expand=True)

        # Загружаем историю
        self.refresh_history()

    def load_history(self):
        """Загрузка истории из файла"""
        if not os.path.exists(HISTORY_FILE):
            return []

        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")
            return []

    def save_history(self, history):
        """Сохранение истории в файл"""
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения истории: {e}")

    def add_campaign_to_history(self, campaign_data):
        """Добавление кампании в историю"""
        history = self.load_history()
        history.append(campaign_data)
        self.save_history(history)
        self.refresh_history()

    def refresh_history(self):
        """Обновление отображения истории"""
        # Очищаем таблицу
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Загружаем историю
        history = self.load_history()

        # Сортируем по дате (новые сверху)
        history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        # Заполняем таблицу
        for campaign in history:
            status_icon = "✅ Запущено" if campaign.get('launched', False) else "❌ Не запущено"
            date_str = campaign.get('date', '')
            alert_type = campaign.get('alert_type', '')
            total = campaign.get('total', 0)
            success = campaign.get('success', 0)
            fail = campaign.get('fail', 0)

            self.history_tree.insert("", "end", values=(
                status_icon,
                date_str,
                alert_type,
                total,
                success,
                fail
            ))

    def setup_scenarios_tab(self):
        ttk.Label(
            self.scenarios_frame,
            text="Нажмите на плитку для быстрой отправки",
            font=("Segoe UI", 11)
        ).pack(pady=(20, 10))

        tiles_frame = ttk.Frame(self.scenarios_frame)
        tiles_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        row, col, max_cols = 0, 0, 2

        for scenario_id, scenario in QUICK_SCENARIOS.items():
            tile = self.create_tile(tiles_frame, scenario_id, scenario)
            tile.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        for i in range(max_cols):
            tiles_frame.columnconfigure(i, weight=1)

    def create_tile(self, parent, scenario_id, scenario):
        emp_names = []
        for emp_id in scenario["employee_ids"]:
            if emp_id in self.employees:
                emp_names.append(self.employees[emp_id]["name"].split()[0])

        tile = tk.Frame(parent, bg=scenario["color"], cursor="hand2", relief=tk.RAISED, bd=2)
        tile.configure(width=280, height=160)
        tile.pack_propagate(False)

        tk.Label(tile, text=scenario["name"], font=("Segoe UI", 14, "bold"), bg=scenario["color"], fg="white").pack(pady=(20, 5))
        tk.Label(tile, text=scenario["description"], font=("Segoe UI", 10), bg=scenario["color"], fg="white").pack()

        count_text = f"→ {len(emp_names)} чел." if emp_names else "→ 0 чел."
        tk.Label(tile, text=count_text, font=("Segoe UI", 11, "bold"), bg=scenario["color"], fg="white").pack(pady=(10, 5))

        preview = ", ".join(emp_names[:3]) + ("..." if len(emp_names) > 3 else "") if emp_names else "—"
        tk.Label(tile, text=preview, font=("Segoe UI", 9), bg=scenario["color"], fg="white", wraplength=250).pack()

        for widget in tile.winfo_children():
            widget.bind("<Button-1>", lambda e, sid=scenario_id: self.run_scenario(sid))
        tile.bind("<Button-1>", lambda e, sid=scenario_id: self.run_scenario(sid))

        return tile

    def load_phones_from_file(self):
        """Загрузка номеров из TXT файла"""
        from tkinter import filedialog

        filepath = filedialog.askopenfilename(
            title="Выберите файл с номерами",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not filepath:
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # Пробуем другую кодировку
            with open(filepath, 'r', encoding='cp1251') as f:
                lines = f.readlines()

        # Парсим номера
        new_phones = []
        for line in lines:
            phone = line.strip()
            if not phone:
                continue

            # Нормализуем номер
            normalized = self._normalize_phone_simple(phone)
            if normalized:
                new_phones.append(normalized)

        # Добавляем к списку (без дубликатов)
        for phone in new_phones:
            if phone not in self.file_phones:
                self.file_phones.append(phone)

        self._update_phones_listbox()

        messagebox.showinfo(
            "Загружено",
            f"Добавлено номеров: {len(new_phones)}\n"
            f"Всего в списке: {len(self.file_phones)}"
        )

    def _normalize_phone_simple(self, phone):
        """Простая нормализация номера"""
        # Убираем всё кроме цифр и +
        phone = re.sub(r'[^\d+]', '', phone)

        if not phone:
            return ""

        digits = re.sub(r'\D', '', phone)

        if len(digits) == 11 and digits.startswith('8'):
            return '+7' + digits[1:]
        elif len(digits) == 11 and digits.startswith('7'):
            return '+' + digits
        elif len(digits) == 10:
            return '+7' + digits
        elif phone.startswith('+') and len(digits) >= 10:
            return phone

        return ""

    def _update_phones_listbox(self):
        """Обновление списка номеров в UI"""
        self.phones_listbox.delete(0, tk.END)
        for i, phone in enumerate(self.file_phones, 1):
            self.phones_listbox.insert(tk.END, f"{i}. {phone}")

        self.file_count_label.config(text=f"Загружено: {len(self.file_phones)} номеров")

    def clear_file_phones(self):
        """Очистка списка номеров"""
        self.file_phones = []
        self._update_phones_listbox()

    def refresh_employees(self):
        # Создаём окно с логом
        log_window = tk.Toplevel(self.root)
        log_window.title("🔄 Загрузка данных...")
        log_window.geometry("700x500")
        log_window.transient(self.root)

        # Текстовое поле для лога
        log_text = tk.Text(log_window, wrap=tk.WORD, font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(log_window, orient=tk.VERTICAL, command=log_text.yview)
        log_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Кнопка закрытия
        ttk.Button(log_window, text="Закрыть", command=log_window.destroy).pack(pady=5)

        log_window.update()

        # Загружаем данные
        self.data_loader = DataLoader(self.config)
        self.employees = self.data_loader.load_employees()
        self.data_source = self.data_loader.source_used

        # Показываем лог PHP если использовался
        if hasattr(self.data_loader.php, 'debug_log'):
            for line in self.data_loader.php.debug_log:
                log_text.insert(tk.END, line + "\n")
                log_text.see(tk.END)
                log_window.update()

        log_text.insert(tk.END, "\n" + "=" * 50 + "\n")
        log_text.insert(tk.END, f"✅ Источник: {self.data_source}\n")
        log_text.insert(tk.END, f"✅ Загружено: {len(self.employees)} сотрудников\n")

        # Обновляем UI
        self.employee_vars.clear()
        self.populate_employees_list()

        for widget in self.scenarios_frame.winfo_children():
            widget.destroy()
        self.setup_scenarios_tab()

    def run_scenario(self, scenario_id):
        scenario = QUICK_SCENARIOS[scenario_id]

        employees_to_call = []
        for emp_id in scenario["employee_ids"]:
            if emp_id in self.employees:
                emp = self.employees[emp_id]
                employees_to_call.append({"id": emp_id, "name": emp["name"], "phone": emp["phone"]})

        if not employees_to_call:
            messagebox.showwarning("Внимание", "Нет сотрудников для этого сценария!")
            return

        emp_list = "\n".join([f"  • {e['name']}" for e in employees_to_call])
        if messagebox.askyesno("Подтверждение", f"Сценарий: {scenario['name']}\n\nБудут оповещены:\n{emp_list}\n\nОтправить?"):
            self.send_alerts(employees_to_call, ALERT_TYPES[scenario["alert_type"]], scenario["name"])

    def send_constructor_alerts(self):
        # Проверка загруженных номеров
        if not self.file_phones:
            messagebox.showwarning("Внимание", "Список номеров пуст!\n\nЗагрузите номера из TXT файла.")
            return

        # Получение текстов
        voice_text = self.voice_text.get("1.0", tk.END).strip()
        sms_text = self.sms_text.get("1.0", tk.END).strip()

        # Проверка что хоть один текст заполнен
        if not voice_text and not sms_text:
            messagebox.showwarning("Внимание", "Заполните хотя бы одно текстовое поле!\n\n(Текст для озвучивания или текст для СМС)")
            return

        alert_type = ALERT_TYPES[self.selected_alert_type.get()]

        # Формируем список для отправки
        employees_to_call = []
        for i, phone in enumerate(self.file_phones):
            employees_to_call.append({
                "id": f"file_{i}",
                "name": f"Номер {phone}",
                "phone": phone
            })

        # Подготовка текста для подтверждения
        confirm_text = f"Тип: {alert_type['name']}\n\n"
        confirm_text += f"Количество номеров: {len(employees_to_call)}\n\n"

        if voice_text:
            confirm_text += f"📞 Текст для озвучивания:\n{voice_text[:100]}{'...' if len(voice_text) > 100 else ''}\n\n"

        if sms_text:
            confirm_text += f"📱 Текст СМС:\n{sms_text[:100]}{'...' if len(sms_text) > 100 else ''}\n\n"

        confirm_text += "Отправить оповещения?"

        # Подтверждение
        if messagebox.askyesno("Подтверждение", confirm_text):
            self.send_alerts(employees_to_call, alert_type, "Конструктор")

    def send_alerts(self, employees, alert_type, source):
        success, fail = 0, 0

        progress = tk.Toplevel(self.root)
        progress.title("Отправка...")
        progress.geometry("350x120")
        progress.transient(self.root)
        progress.grab_set()

        label = ttk.Label(progress, text="Отправка...", font=("Segoe UI", 10))
        label.pack(pady=20)

        bar = ttk.Progressbar(progress, length=300, maximum=len(employees))
        bar.pack(pady=10)

        for i, emp in enumerate(employees):
            label.config(text=f"Отправка: {emp['name']}...")
            bar["value"] = i + 1
            progress.update()

            if self.send_single_request(emp["phone"], alert_type["service"], alert_type["monitor_bank_id"]):
                success += 1
                self._log_action("SUCCESS", f"{source} | {emp['name']} | {emp['phone']} | CONNID: {self.current_connid - 1}")
            else:
                fail += 1
                self._log_action("FAIL", f"{source} | {emp['name']} | {emp['phone']}")

        progress.destroy()
        self.status_label.config(text=f"CONNID: {self.current_connid} | ✅{success} ❌{fail}")

        # Сохраняем в историю
        campaign_data = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "alert_type": alert_type["name"],
            "source": source,
            "total": len(employees),
            "success": success,
            "fail": fail,
            "launched": True
        }
        self.add_campaign_to_history(campaign_data)

        if fail == 0:
            messagebox.showinfo("Успех", f"Отправлено: {success}")
        else:
            messagebox.showwarning("Внимание", f"Успешно: {success}\nОшибок: {fail}")

    def send_single_request(self, phone, service, monitor_bank_id):
        try:
            data = {
                "ANI": phone,
                "CONNID": f"{self.current_connid}7",
                "TZ_DBID": "1",
                "SERVICE": service,
                "DELAY": "1",
                "ADD_PROP": json.dumps({"MONITOR_BANK_ID": monitor_bank_id}),
                "CUSTID": "1000"
            }

            json_data = json.dumps(data).encode("utf-8")

            request = urllib.request.Request(
                self.config.api_url,
                data=json_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            ssl_context = ssl.create_default_context()
            if not self.config.verify_ssl:
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE

            with urllib.request.urlopen(request, context=ssl_context, timeout=self.config.api_timeout):
                pass

            self.current_connid += 1
            self._save_connid()
            return True

        except Exception as e:
            print(f"Ошибка: {phone} - {e}")
            return False

    def on_closing(self):
        self.data_loader.disconnect()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = IVRCallerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
