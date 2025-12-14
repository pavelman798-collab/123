#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Outbound Manager — приложение для управления исходящими звонками и SMS
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

# Попытка импорта paramiko для SSH
try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False
    print("⚠️ paramiko не установлен. Подключение к лог-серверу недоступно.")


# ============== ПУТИ К ФАЙЛАМ ==============
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.ini")
CONNID_FILE = os.path.join(BASE_DIR, "connid.txt")
LOG_FILE = os.path.join(BASE_DIR, "ivr_log.txt")
DEBUG_LOG_FILE = os.path.join(BASE_DIR, "debug.log")
HISTORY_FILE = os.path.join(BASE_DIR, "campaigns_history.json")
THEME_FILE = os.path.join(BASE_DIR, "theme.txt")
# ===========================================


# ============== ДИЗАЙН-СИСТЕМА МТС ==============
class MTSTheme:
    """Управление темами оформления в стиле МТС"""

    # Светлая тема (по умолчанию)
    LIGHT = {
        'bg': '#FFFFFF',
        'fg': '#333333',
        'primary': '#E30611',  # Красный МТС
        'primary_hover': '#C5050C',
        'secondary': '#F5F5F5',
        'border': '#E0E0E0',
        'card_bg': '#FFFFFF',
        'card_shadow': '#00000015',
        'success': '#28A745',
        'warning': '#FFC107',
        'error': '#DC3545',
        'text_muted': '#6C757D',
        'input_bg': '#FFFFFF',
        'header_bg': '#E30611',
        'header_fg': '#FFFFFF'
    }

    # Темная тема
    DARK = {
        'bg': '#1E1E1E',
        'fg': '#E0E0E0',
        'primary': '#FF0019',  # Яркий красный для темной темы
        'primary_hover': '#FF3340',
        'secondary': '#2D2D2D',
        'border': '#404040',
        'card_bg': '#252525',
        'card_shadow': '#00000040',
        'success': '#2ECC71',
        'warning': '#F39C12',
        'error': '#E74C3C',
        'text_muted': '#95A5A6',
        'input_bg': '#2D2D2D',
        'header_bg': '#252525',
        'header_fg': '#FFFFFF'
    }

    @staticmethod
    def load_theme():
        """Загрузить текущую тему из файла"""
        try:
            if os.path.exists(THEME_FILE):
                with open(THEME_FILE, 'r') as f:
                    theme = f.read().strip()
                    return theme if theme in ['light', 'dark'] else 'light'
        except:
            pass
        return 'light'

    @staticmethod
    def save_theme(theme):
        """Сохранить текущую тему в файл"""
        try:
            with open(THEME_FILE, 'w') as f:
                f.write(theme)
        except:
            pass

    @staticmethod
    def get_colors(theme='light'):
        """Получить цвета для указанной темы"""
        return MTSTheme.DARK if theme == 'dark' else MTSTheme.LIGHT

# ===========================================


# ============== ТИПЫ ОПОВЕЩЕНИЙ ==============
ALERT_TYPES = {
    "call": {
        "name": "☎ Позвонить",
        "icon": "☎",
        "service": "MONITOR_BANK",
        "monitor_bank_id": "1"
    },
    "call_sms": {
        "name": "⚡ Позвонить и отправить СМС",
        "icon": "⚡",
        "service": "MONITOR_BANK",
        "monitor_bank_id": "1"
    },
    "sms": {
        "name": "✉ Отправить СМС",
        "icon": "✉",
        "service": "MONITOR_BANK",
        "monitor_bank_id": "1"
    },
}
# =============================================


# ============== БЫСТРЫЕ СЦЕНАРИИ ==============
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


class DebugLogger:
    """Детальное логирование для отладки"""

    def __init__(self, log_file=DEBUG_LOG_FILE):
        self.log_file = log_file

    def _write_log(self, level, message, data=None):
        """Запись в лог файл"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            log_entry = f"[{timestamp}] [{level}] {message}"

            if data:
                log_entry += f"\nДанные: {json.dumps(data, ensure_ascii=False, indent=2)}"

            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n" + "-" * 80 + "\n")
        except Exception as e:
            print(f"Ошибка записи в debug.log: {e}")

    def debug(self, message, data=None):
        """DEBUG уровень - детальная отладочная информация"""
        self._write_log("DEBUG", message, data)

    def info(self, message, data=None):
        """INFO уровень - общая информация"""
        self._write_log("INFO", message, data)

    def warning(self, message, data=None):
        """WARNING уровень - предупреждения"""
        self._write_log("WARNING", message, data)

    def error(self, message, data=None):
        """ERROR уровень - ошибки"""
        self._write_log("ERROR", message, data)


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
        self.config['api'] = {'url': 'http://172.16.152.67:80/fm2/UDB/IVR_ADD_CALL_EXP'}
        self.config['settings'] = {
            'api_timeout': '3',
            'verify_ssl': 'false'
        }
        self.config['log_server'] = {
            'host': '',  # Адрес сервера (укажите сами)
            'port': '22',
            'username': '',  # Имя пользователя (укажите сами)
            'password': '',  # Пароль (укажите сами)
            'log_dir': '/opt/log/fm2/',
            'log_file': 'fm2.log'
        }
        with open(self.config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)
        print(f"✅ Создан конфиг: {self.config_path}")

    @property
    def api_url(self):
        return self.config.get('api', 'url')

    @property
    def api_timeout(self):
        return self.config.getint('settings', 'api_timeout', fallback=3)

    @property
    def verify_ssl(self):
        return self.config.getboolean('settings', 'verify_ssl', fallback=False)

    def get(self, key, default=''):
        """Получить значение из секции auth"""
        if not self.config.has_section('auth'):
            return default
        return self.config.get('auth', key, fallback=default)

    def set(self, key, value):
        """Установить значение в секцию auth"""
        if not self.config.has_section('auth'):
            self.config.add_section('auth')
        self.config.set('auth', key, value)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)


class LogServerConnector:
    """Подключение к лог-серверу по SSH и парсинг логов"""

    def __init__(self, config):
        self.config = config
        self.client = None
        self.connected = False

    def get_connection_params(self):
        """Получить параметры подключения из конфига"""
        if not self.config.config.has_section('log_server'):
            # Создаем секцию с параметрами по умолчанию
            self.config.config['log_server'] = {
                'host': '',  # Адрес сервера (укажите сами)
                'port': '22',
                'username': '',  # Имя пользователя (укажите сами)
                'password': '',  # Пароль (укажите сами)
                'log_dir': '/opt/log/fm2/',
                'log_file': 'fm2.log'
            }
            with open(self.config.config_path, 'w', encoding='utf-8') as f:
                self.config.config.write(f)
            print("⚠️ Добавлена секция [log_server] в config.ini. Укажите параметры подключения.")

        return {
            'host': self.config.config.get('log_server', 'host'),
            'port': self.config.config.getint('log_server', 'port', fallback=22),
            'username': self.config.config.get('log_server', 'username'),
            'password': self.config.config.get('log_server', 'password'),
            'log_dir': self.config.config.get('log_server', 'log_dir', fallback='/opt/log/fm2/'),
            'log_file': self.config.config.get('log_server', 'log_file', fallback='fm2.log')
        }

    def connect(self):
        """Подключение к серверу по SSH"""
        if not HAS_PARAMIKO:
            print("⚠️ paramiko не установлен. Установите: pip install paramiko")
            return False

        params = self.get_connection_params()

        if not params['host'] or not params['username'] or not params['password']:
            print("⚠️ Не указаны параметры подключения к лог-серверу в config.ini")
            return False

        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=params['host'],
                port=params['port'],
                username=params['username'],
                password=params['password'],
                timeout=10
            )
            self.connected = True
            print(f"✅ Подключено к лог-серверу: {params['host']}")
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения к лог-серверу: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """Отключение от сервера"""
        if self.client:
            self.client.close()
            self.connected = False
            print("🔌 Отключено от лог-сервера")

    def search_phone_in_logs(self, phone_number):
        """Поиск телефонного номера в логах

        Args:
            phone_number: номер телефона для поиска

        Returns:
            dict: {'success': bool, 'entries': list, 'count': int}
        """
        if not self.connected:
            if not self.connect():
                return {'success': False, 'entries': [], 'count': 0, 'error': 'Нет подключения'}

        params = self.get_connection_params()
        log_path = os.path.join(params['log_dir'], params['log_file'])

        # Очищаем номер от спецсимволов для поиска
        clean_phone = phone_number.replace('+', '').replace('-', '').replace(' ', '')

        # Формируем команду grep
        command = f"grep '{clean_phone}' {log_path}"

        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            if error and 'No such file' in error:
                return {'success': False, 'entries': [], 'count': 0, 'error': 'Файл лога не найден'}

            # Парсим результаты
            entries = []
            if output:
                lines = output.strip().split('\n')
                for line in lines:
                    if line.strip():
                        entries.append(line)

            return {
                'success': True,
                'entries': entries,
                'count': len(entries)
            }

        except Exception as e:
            return {'success': False, 'entries': [], 'count': 0, 'error': str(e)}

    def check_campaign_delivery(self, phone_numbers):
        """Проверка доставки для списка номеров

        Args:
            phone_numbers: list of phone numbers

        Returns:
            dict: {'total': int, 'delivered': int, 'failed': int, 'details': dict}
        """
        results = {
            'total': len(phone_numbers),
            'delivered': 0,
            'failed': 0,
            'details': {}
        }

        for phone in phone_numbers:
            search_result = self.search_phone_in_logs(phone)

            if search_result['success'] and search_result['count'] > 0:
                results['delivered'] += 1
                results['details'][phone] = {
                    'status': 'delivered',
                    'log_entries': search_result['count']
                }
            else:
                results['failed'] += 1
                results['details'][phone] = {
                    'status': 'not_found',
                    'log_entries': 0
                }

        return results


class LoginWindow:
    """Окно авторизации"""

    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Авторизация - Outbound Manager")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Центрируем окно
        self.root.eval('tk::PlaceWindow . center')

        # Результат авторизации
        self.authenticated = False
        self.username = None
        self.password = None

        # Создаем UI
        self.create_widgets()

        # Загружаем сохраненные учетные данные
        self.load_credentials()

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # Заголовок
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=(30, 20))

        ttk.Label(
            title_frame,
            text="🔐 Вход в систему",
            font=("Segoe UI", 16, "bold")
        ).pack()

        ttk.Label(
            title_frame,
            text="Outbound Manager v5",
            font=("Segoe UI", 10),
            foreground="gray"
        ).pack(pady=(5, 0))

        # Поля ввода
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20, padx=40, fill=tk.X)

        # Логин
        ttk.Label(form_frame, text="Логин:", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(form_frame, textvariable=self.username_var, font=("Segoe UI", 10))
        self.username_entry.pack(fill=tk.X, pady=(0, 15))

        # Пароль
        ttk.Label(form_frame, text="Пароль:", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(form_frame, textvariable=self.password_var, font=("Segoe UI", 10), show="●")
        self.password_entry.pack(fill=tk.X, pady=(0, 10))

        # Чекбокс "Запомнить"
        self.remember_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            form_frame,
            text="Запомнить учетные данные",
            variable=self.remember_var
        ).pack(anchor=tk.W, pady=(5, 0))

        # Кнопка входа
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)

        ttk.Button(
            btn_frame,
            text="Войти",
            command=self.login,
            width=20
        ).pack()

        # Статус
        self.status_label = ttk.Label(self.root, text="", font=("Segoe UI", 9), foreground="red")
        self.status_label.pack()

        # Привязываем Enter к кнопке входа
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())

        # Фокус на поле логина
        self.username_entry.focus()

    def load_credentials(self):
        """Загрузка сохраненных учетных данных"""
        config = Config(CONFIG_FILE)
        username = config.get('username', '')
        password = config.get('password', '')

        if username:
            self.username_var.set(username)
        if password:
            self.password_var.set(password)
            self.password_entry.focus()

    def save_credentials(self):
        """Сохранение учетных данных"""
        if self.remember_var.get():
            config = Config(CONFIG_FILE)
            config.set('username', self.username)
            config.set('password', self.password)
        else:
            # Очищаем сохраненные данные
            config = Config(CONFIG_FILE)
            config.set('username', '')
            config.set('password', '')

    def login(self):
        """Обработка входа"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            self.status_label.config(text="Заполните все поля!")
            return

        # Здесь можно добавить реальную проверку учетных данных
        # Пока что принимаем любые непустые значения
        if len(username) >= 3 and len(password) >= 3:
            self.authenticated = True
            self.username = username
            self.password = password
            self.save_credentials()
            self.root.destroy()
        else:
            self.status_label.config(text="Логин и пароль должны быть минимум 3 символа!")


class IVRCallerApp:
    """Основное приложение"""

    def __init__(self, root, username=None):
        self.root = root
        self.root.title("МТС Outbound Manager")
        self.root.geometry("850x700")
        self.root.resizable(True, True)
        self.root.minsize(750, 600)

        # Загрузка темы
        self.current_theme = MTSTheme.load_theme()
        self.colors = MTSTheme.get_colors(self.current_theme)

        # Применение цветов к окну
        self.root.configure(bg=self.colors['bg'])

        # Конфигурация
        self.config = Config(CONFIG_FILE)

        # Debug logger
        self.debug_logger = DebugLogger()
        self.debug_logger.info("Приложение запущено", {"version": "v5", "user": username, "theme": self.current_theme})

        # Подключение к лог-серверу
        self.log_server = LogServerConnector(self.config)
        # Создаем секцию log_server в конфиге, если её нет
        self.log_server.get_connection_params()

        # CONNID
        self.current_connid = self._load_connid()

        # UI переменные
        self.selected_alert_type = tk.StringVar(value="call")

        self.setup_ui()
        self.center_window()

        # Запускаем проверку отложенных кампаний
        self.root.after(5000, self.check_scheduled_campaigns)

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

    def create_card(self, parent, title=None, padx=20, pady=10):
        """Создает карточку с рамкой и отступами в стиле МТС"""
        # Внешний контейнер для отступов
        card_container = tk.Frame(parent, bg=self.colors['bg'])
        card_container.pack(fill=tk.BOTH, expand=True, padx=padx, pady=pady)

        # Карточка с границей
        card = tk.Frame(
            card_container,
            bg=self.colors['card_bg'],
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        card.pack(fill=tk.BOTH, expand=True)

        # Заголовок карточки (опционально)
        if title:
            title_frame = tk.Frame(card, bg=self.colors['card_bg'])
            title_frame.pack(fill=tk.X, padx=15, pady=(12, 8))

            tk.Label(
                title_frame,
                text=title,
                font=("Roboto", 12, "bold"),
                bg=self.colors['card_bg'],
                fg=self.colors['fg']
            ).pack(side=tk.LEFT)

            # Разделитель
            separator = tk.Frame(card, bg=self.colors['border'], height=1)
            separator.pack(fill=tk.X, padx=15)

        # Контент карточки
        content = tk.Frame(card, bg=self.colors['card_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        return content

    def setup_ui(self):
        # Header МТС с логотипом и переключателем темы
        header_frame = tk.Frame(self.root, bg=self.colors['header_bg'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Логотип МТС - красный квадрат с белым текстом
        logo_container = tk.Frame(header_frame, bg=self.colors['header_bg'])
        logo_container.pack(side=tk.LEFT, padx=20, pady=10)

        # Красный квадрат с логотипом МТС
        logo_label = tk.Label(
            logo_container,
            text="МТС",
            font=("Arial", 24, "bold"),
            bg="#E30611",
            fg="#FFFFFF",
            padx=12,
            pady=8
        )
        logo_label.pack(side=tk.LEFT)

        # Название приложения
        tk.Label(
            logo_container,
            text="Outbound Manager",
            font=("Roboto", 13),
            bg=self.colors['header_bg'],
            fg=self.colors['header_fg']
        ).pack(side=tk.LEFT, padx=(12, 0))

        # Переключатель темы
        theme_frame = tk.Frame(header_frame, bg=self.colors['header_bg'])
        theme_frame.pack(side=tk.RIGHT, padx=20)

        theme_btn = tk.Button(
            theme_frame,
            text="◐ Сменить тему",
            font=("Roboto", 10),
            bg=self.colors['header_bg'],
            fg=self.colors['header_fg'],
            activebackground=self.colors['primary_hover'],
            activeforeground=self.colors['header_fg'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.toggle_theme
        )
        theme_btn.pack()

        # Вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 15))

        self.constructor_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.constructor_frame, text="⚙ Конструктор")
        self.setup_constructor_tab()

        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="⏱ История")
        self.setup_history_tab()

        # Статус-бар с границей
        status_border = tk.Frame(self.root, bg=self.colors['border'], height=1)
        status_border.pack(side=tk.BOTTOM, fill=tk.X)

        status_frame = tk.Frame(self.root, bg='#EEEEEE', height=40)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text=f"CONNID: {self.current_connid}  •  Готов к работе",
            font=("Roboto", 10, "bold"),
            bg='#EEEEEE',
            fg='#333333',
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, padx=20, pady=10)

    def setup_constructor_tab(self):
        # Инициализация списка номеров
        self.file_phones = []

        # Создаем Canvas с прокруткой
        canvas = tk.Canvas(self.constructor_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.constructor_frame, orient="vertical", command=canvas.yview)

        # Внутренний фрейм для содержимого
        frame_inner = tk.Frame(canvas, bg=self.colors['bg'])

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

        # === КАРТОЧКА 1: Тип оповещения ===
        alert_card = self.create_card(frame_inner, title="☎ Тип оповещения", pady=15)

        alert_buttons_frame = tk.Frame(alert_card, bg=self.colors['card_bg'])
        alert_buttons_frame.pack(fill=tk.X, pady=10)

        col_idx = 0
        for key, alert in ALERT_TYPES.items():
            rb_frame = tk.Frame(alert_buttons_frame, bg=self.colors['card_bg'])
            rb_frame.grid(row=0, column=col_idx, padx=15, pady=10, sticky=tk.W)

            tk.Radiobutton(
                rb_frame,
                text=alert["name"],
                value=key,
                variable=self.selected_alert_type,
                font=("Roboto", 11),
                bg=self.colors['card_bg'],
                fg=self.colors['fg'],
                selectcolor=self.colors['card_bg'],
                activebackground=self.colors['card_bg'],
                activeforeground=self.colors['primary'],
                cursor="hand2"
            ).pack()
            col_idx += 1

        # Добавляем trace для отслеживания изменений типа оповещения
        self.selected_alert_type.trace("w", self.toggle_text_fields)

        # === КАРТОЧКА 2: Содержимое сообщений ===
        text_card = self.create_card(frame_inner, title="✉ Содержимое сообщений", pady=15)

        # Поле для озвучивания
        tk.Label(
            text_card,
            text="📞 Текст для озвучивания при звонке",
            font=("Roboto", 12, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['fg']
        ).pack(anchor=tk.W, pady=(5, 8))

        self.voice_text = tk.Text(
            text_card,
            height=4,
            font=("Roboto", 11),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1,
            padx=10,
            pady=8
        )
        self.voice_text.pack(fill=tk.X, pady=(0, 20))

        # Поле для СМС
        tk.Label(
            text_card,
            text="📱 Текст для СМС",
            font=("Roboto", 12, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['fg']
        ).pack(anchor=tk.W, pady=(5, 8))

        self.sms_text = tk.Text(
            text_card,
            height=4,
            font=("Roboto", 11),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1,
            padx=10,
            pady=8
        )
        self.sms_text.pack(fill=tk.X)

        # === КАРТОЧКА 3: Загрузка номеров ===
        file_card = self.create_card(frame_inner, title="📂 Загрузка номеров телефонов", pady=15)

        # Кнопки загрузки
        btn_frame = tk.Frame(file_card, bg=self.colors['card_bg'])
        btn_frame.pack(fill=tk.X, pady=(5, 15))

        tk.Button(
            btn_frame,
            text="📂 Выбрать файл",
            font=("Roboto", 11, "bold"),
            bg=self.colors['primary'],
            fg="white",
            activebackground=self.colors['primary_hover'],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.load_phones_from_file
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_frame,
            text="📥 Пример",
            font=("Roboto", 11, "bold"),
            bg='#E0E0E0',
            fg='#333333',
            activebackground='#D0D0D0',
            activeforeground='#333333',
            relief=tk.SOLID,
            borderwidth=1,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.export_example_file
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_frame,
            text="🗑️ Очистить",
            font=("Roboto", 11, "bold"),
            bg='#E0E0E0',
            fg='#333333',
            activebackground='#D0D0D0',
            activeforeground='#333333',
            relief=tk.SOLID,
            borderwidth=1,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.clear_file_phones
        ).pack(side=tk.LEFT)

        self.file_count_label = tk.Label(
            btn_frame,
            text="Загружено: 0 номеров",
            font=("Roboto", 11, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['primary']
        )
        self.file_count_label.pack(side=tk.RIGHT)

        # Список номеров
        list_frame = tk.Frame(file_card, bg=self.colors['card_bg'])
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.phones_listbox = tk.Listbox(
            list_frame,
            font=("Consolas", 10),
            selectmode=tk.EXTENDED,
            height=6,
            relief=tk.SOLID,
            borderwidth=1
        )
        scrollbar_list = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.phones_listbox.yview)
        self.phones_listbox.configure(yscrollcommand=scrollbar_list.set)

        scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)
        self.phones_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Подсказка
        tk.Label(
            file_card,
            text="💡 Формат файла: один номер на строку (+79991234567;+3)",
            font=("Roboto", 10),
            bg=self.colors['card_bg'],
            fg=self.colors['text_muted']
        ).pack(anchor=tk.W)

        # === КАРТОЧКА 4: Параметры кампании ===
        params_card = self.create_card(frame_inner, title="⚙ Параметры кампании", pady=15)

        # Номер отправителя
        tk.Label(
            params_card,
            text="Номер с которого совершать вызов *",
            font=("Roboto", 12, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['fg']
        ).pack(anchor=tk.W, pady=(5, 8))

        sender_frame = tk.Frame(params_card, bg=self.colors['card_bg'])
        sender_frame.pack(fill=tk.X, pady=(0, 5))

        self.sender_phone = tk.StringVar()
        self.sender_entry = tk.Entry(
            sender_frame,
            textvariable=self.sender_phone,
            font=("Consolas", 12),
            relief=tk.SOLID,
            borderwidth=1,
            width=25
        )
        self.sender_entry.pack(side=tk.LEFT, ipady=5)

        self.sender_validation_label = tk.Label(
            sender_frame,
            text="",
            font=("Roboto", 10),
            bg=self.colors['card_bg']
        )
        self.sender_validation_label.pack(side=tk.LEFT, padx=(10, 0))

        # Валидация номера отправителя
        self.sender_phone.trace("w", self.validate_sender_phone)

        tk.Label(
            params_card,
            text="💡 11 цифр, начинается с 7 (например: 79991234567)",
            font=("Roboto", 10),
            bg=self.colors['card_bg'],
            fg=self.colors['text_muted']
        ).pack(anchor=tk.W, pady=(0, 15))

        # Номер шаблона СМС
        self.template_label = tk.Label(
            params_card,
            text="Номер шаблона СМС",
            font=("Roboto", 12, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['fg']
        )
        self.template_label.pack(anchor=tk.W, pady=(5, 8))

        template_frame = tk.Frame(params_card, bg=self.colors['card_bg'])
        template_frame.pack(fill=tk.X, pady=(0, 5))

        self.sms_template = tk.StringVar()
        self.sms_template_entry = tk.Entry(
            template_frame,
            textvariable=self.sms_template,
            font=("Consolas", 12),
            relief=tk.SOLID,
            borderwidth=1,
            width=25
        )
        self.sms_template_entry.pack(side=tk.LEFT, ipady=5)

        # Подсказка для шаблона СМС
        self.template_hint = tk.Label(
            params_card,
            text="",
            font=("Roboto", 10),
            bg=self.colors['card_bg'],
            fg=self.colors['text_muted']
        )
        self.template_hint.pack(anchor=tk.W, pady=(0, 15))

        # Отложенная отправка
        delayed_frame = tk.Frame(params_card, bg=self.colors['card_bg'])
        delayed_frame.pack(fill=tk.X, pady=(10, 10))

        self.delayed_send = tk.BooleanVar(value=False)
        tk.Checkbutton(
            delayed_frame,
            text="Отложенная отправка",
            variable=self.delayed_send,
            font=("Roboto", 11),
            bg=self.colors['card_bg'],
            fg=self.colors['fg'],
            selectcolor=self.colors['card_bg'],
            activebackground=self.colors['card_bg'],
            activeforeground=self.colors['primary'],
            cursor="hand2",
            command=self.toggle_delayed_send
        ).pack(side=tk.LEFT)

        # Поля для даты и времени
        datetime_frame = tk.Frame(params_card, bg=self.colors['card_bg'])
        datetime_frame.pack(fill=tk.X, pady=(5, 5))

        tk.Label(
            datetime_frame,
            text="Дата:",
            font=("Roboto", 11),
            bg=self.colors['card_bg'],
            fg=self.colors['fg']
        ).pack(side=tk.LEFT, padx=(20, 8))

        self.send_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.date_entry = tk.Entry(
            datetime_frame,
            textvariable=self.send_date,
            font=("Consolas", 11),
            relief=tk.SOLID,
            borderwidth=1,
            width=12
        )
        self.date_entry.pack(side=tk.LEFT, ipady=3, padx=(0, 20))
        self.date_entry.config(state='disabled')

        tk.Label(
            datetime_frame,
            text="Время:",
            font=("Roboto", 11),
            bg=self.colors['card_bg'],
            fg=self.colors['fg']
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.send_time = tk.StringVar(value="12:00")
        self.time_entry = tk.Entry(
            datetime_frame,
            textvariable=self.send_time,
            font=("Consolas", 11),
            relief=tk.SOLID,
            borderwidth=1,
            width=8
        )
        self.time_entry.pack(side=tk.LEFT, ipady=3)
        self.time_entry.config(state='disabled')

        tk.Label(
            params_card,
            text="💡 Формат даты: ГГГГ-ММ-ДД, времени: ЧЧ:ММ",
            font=("Roboto", 10),
            bg=self.colors['card_bg'],
            fg=self.colors['text_muted']
        ).pack(anchor=tk.W, pady=(5, 0))

        # === КНОПКА ОТПРАВКИ ===
        bottom_container = tk.Frame(frame_inner, bg=self.colors['bg'])
        bottom_container.pack(fill=tk.X, padx=20, pady=20)

        send_btn = tk.Button(
            bottom_container,
            text="Отправить оповещения",
            font=("Roboto", 14, "bold"),
            bg=self.colors['primary'],
            fg="white",
            activebackground=self.colors['primary_hover'],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=40,
            pady=15,
            command=self.send_constructor_alerts
        )
        send_btn.pack(side=tk.RIGHT)

        # Инициализируем состояние полей
        self.toggle_text_fields()

    def toggle_text_fields(self, *args):
        """Включение/выключение текстовых полей в зависимости от типа оповещения"""
        alert_type = self.selected_alert_type.get()

        if alert_type == "call":
            # Позвонить - только поле озвучивания
            self.voice_text.config(state='normal', bg='white')
            self.sms_text.config(state='disabled', bg='#f0f0f0')
            # Номер отправителя нужен
            self.sender_entry.config(state='normal')
            # Номер шаблона СМС не требуется
            self.sms_template_entry.config(state='disabled')
            self.template_label.config(text="Номер шаблона СМС:")
            self.template_hint.config(text="💡 Поле недоступно для типа 'Позвонить' (не требуется)", foreground="gray")

        elif alert_type == "sms":
            # Отправить СМС - только поле СМС
            self.voice_text.config(state='disabled', bg='#f0f0f0')
            self.sms_text.config(state='normal', bg='white')
            # Номер отправителя не нужен для СМС
            self.sender_entry.config(state='disabled')
            # Номер шаблона СМС обязателен
            self.sms_template_entry.config(state='normal')
            self.template_label.config(text="Номер шаблона СМС: *", font=("Segoe UI", 10, "bold"))
            self.template_hint.config(text="💡 Обязательное поле для типа 'Отправить СМС'", foreground="green")

        elif alert_type == "call_sms":
            # Позвонить и отправить СМС - оба поля
            self.voice_text.config(state='normal', bg='white')
            self.sms_text.config(state='normal', bg='white')
            # Номер отправителя нужен
            self.sender_entry.config(state='normal')
            # Номер шаблона СМС обязателен
            self.sms_template_entry.config(state='normal')
            self.template_label.config(text="Номер шаблона СМС: *", font=("Segoe UI", 10, "bold"))
            self.template_hint.config(text="💡 Обязательное поле для типа 'Позвонить и отправить СМС'", foreground="green")

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
        # Создаем подвкладки для истории
        self.history_notebook = ttk.Notebook(self.history_frame)
        self.history_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Подвкладка "В очереди"
        self.queued_frame = ttk.Frame(self.history_notebook)
        self.history_notebook.add(self.queued_frame, text="⏳ В очереди")
        self.setup_queued_tab()

        # Подвкладка "Завершенные"
        self.completed_frame = ttk.Frame(self.history_notebook)
        self.history_notebook.add(self.completed_frame, text="✅ Завершенные")
        self.setup_completed_tab()

    def setup_queued_tab(self):
        """Подвкладка с кампаниями в очереди"""
        # Поиск
        search_frame = ttk.Frame(self.queued_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(search_frame, text="🔍 Поиск по номеру телефона:").pack(side=tk.LEFT, padx=(0, 10))
        self.queued_search_var = tk.StringVar()
        self.queued_search_var.trace("w", lambda *args: self.refresh_queued_history())
        ttk.Entry(search_frame, textvariable=self.queued_search_var, width=20).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            search_frame,
            text="🔄 Обновить",
            font=("Roboto", 10, "bold"),
            bg=self.colors['primary'],
            fg="white",
            activebackground=self.colors['primary_hover'],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            command=self.refresh_queued_history
        ).pack(side=tk.RIGHT)

        # Таблица
        tree_frame = ttk.Frame(self.queued_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("scheduled_time", "type", "phones", "sender", "actions")
        self.queued_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=12
        )
        scrollbar.config(command=self.queued_tree.yview)

        self.queued_tree.heading("scheduled_time", text="📅 Запланировано")
        self.queued_tree.heading("type", text="Тип")
        self.queued_tree.heading("phones", text="Всего номеров")
        self.queued_tree.heading("sender", text="Отправитель")
        self.queued_tree.heading("actions", text="Действия")

        self.queued_tree.column("scheduled_time", width=180, anchor=tk.CENTER)
        self.queued_tree.column("type", width=200, anchor=tk.W)
        self.queued_tree.column("phones", width=120, anchor=tk.CENTER)
        self.queued_tree.column("sender", width=120, anchor=tk.CENTER)
        self.queued_tree.column("actions", width=150, anchor=tk.CENTER)

        self.queued_tree.pack(fill=tk.BOTH, expand=True)

        # Двойной клик для просмотра детальной информации
        self.queued_tree.bind("<Double-Button-1>", lambda e: self.view_campaign_details("queued"))

        # Кнопки действий
        btn_frame = ttk.Frame(self.queued_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(
            btn_frame,
            text="👁️ Просмотреть",
            font=("Roboto", 10, "bold"),
            bg=self.colors['primary'],
            fg="white",
            activebackground=self.colors['primary_hover'],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=lambda: self.view_campaign_details("queued")
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_frame,
            text="Экспорт запросов",
            font=("Roboto", 10, "bold"),
            bg=self.colors['primary'],
            fg="white",
            activebackground=self.colors['primary_hover'],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=lambda: self.export_campaign_requests("queued")
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_frame,
            text="Удалить из очереди",
            font=("Roboto", 10, "bold"),
            bg=self.colors['primary'],
            fg="white",
            activebackground=self.colors['primary_hover'],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.delete_queued_campaign
        ).pack(side=tk.LEFT)

        self.refresh_queued_history()

    def setup_completed_tab(self):
        """Подвкладка с завершенными кампаниями"""
        # Поиск
        search_frame = ttk.Frame(self.completed_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(search_frame, text="🔍 Поиск по номеру телефона:").pack(side=tk.LEFT, padx=(0, 10))
        self.completed_search_var = tk.StringVar()
        self.completed_search_var.trace("w", lambda *args: self.refresh_completed_history())
        ttk.Entry(search_frame, textvariable=self.completed_search_var, width=20).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            search_frame,
            text="🔄 Обновить",
            font=("Roboto", 10, "bold"),
            bg=self.colors['primary'],
            fg="white",
            activebackground=self.colors['primary_hover'],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=6,
            command=self.refresh_completed_history
        ).pack(side=tk.RIGHT)

        # Таблица
        tree_frame = ttk.Frame(self.completed_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("status", "date", "type", "phones", "success", "fail")
        self.completed_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=12
        )
        scrollbar.config(command=self.completed_tree.yview)

        self.completed_tree.heading("status", text="Статус")
        self.completed_tree.heading("date", text="Дата и время")
        self.completed_tree.heading("type", text="Тип")
        self.completed_tree.heading("phones", text="Всего номеров")
        self.completed_tree.heading("success", text="Успешно")
        self.completed_tree.heading("fail", text="Ошибок")

        self.completed_tree.column("status", width=100, anchor=tk.CENTER)
        self.completed_tree.column("date", width=180, anchor=tk.CENTER)
        self.completed_tree.column("type", width=200, anchor=tk.W)
        self.completed_tree.column("phones", width=120, anchor=tk.CENTER)
        self.completed_tree.column("success", width=100, anchor=tk.CENTER)
        self.completed_tree.column("fail", width=100, anchor=tk.CENTER)

        self.completed_tree.pack(fill=tk.BOTH, expand=True)

        # Двойной клик для просмотра детальной информации
        self.completed_tree.bind("<Double-Button-1>", lambda e: self.view_campaign_details("completed"))

        # Кнопки действий
        btn_frame = ttk.Frame(self.completed_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(
            btn_frame,
            text="👁️ Просмотреть",
            font=("Roboto", 10, "bold"),
            bg=self.colors['primary'],
            fg="white",
            activebackground=self.colors['primary_hover'],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=lambda: self.view_campaign_details("completed")
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btn_frame,
            text="Экспорт запросов",
            font=("Roboto", 10, "bold"),
            bg=self.colors['primary'],
            fg="white",
            activebackground=self.colors['primary_hover'],
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=lambda: self.export_campaign_requests("completed")
        ).pack(side=tk.LEFT)

        self.refresh_completed_history()

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
        import uuid
        # Добавляем уникальный ID если его нет
        if 'id' not in campaign_data:
            campaign_data['id'] = str(uuid.uuid4())

        history = self.load_history()
        history.append(campaign_data)
        self.save_history(history)

        # Обновляем обе вкладки
        try:
            self.refresh_queued_history()
            self.refresh_completed_history()
        except:
            pass  # Если вкладки еще не созданы

    def delete_queued_campaign(self):
        """Удаление кампании из очереди"""
        selection = self.queued_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите кампанию для удаления")
            return

        if not messagebox.askyesno("Подтверждение", "Удалить выбранную кампанию из очереди?"):
            return

        # Получаем ID кампании из tags
        item = selection[0]
        campaign_id = self.queued_tree.item(item)['tags'][0]

        # Загружаем историю и удаляем кампанию
        history = self.load_history()
        history = [c for c in history if c.get('id') != campaign_id]
        self.save_history(history)

        self.refresh_queued_history()
        messagebox.showinfo("Успех", "Кампания удалена из очереди")

    def export_campaign_requests(self, tab_type):
        """Экспорт запросов кампании в txt файл"""
        # Определяем какое дерево использовать
        tree = self.queued_tree if tab_type == "queued" else self.completed_tree

        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите кампанию для экспорта")
            return

        # Получаем ID кампании
        item = selection[0]
        campaign_id = tree.item(item)['tags'][0]

        # Находим кампанию в истории
        history = self.load_history()
        campaign = None
        for c in history:
            if c.get('id') == campaign_id:
                campaign = c
                break

        if not campaign:
            messagebox.showerror("Ошибка", "Кампания не найдена")
            return

        # Формируем содержимое файла
        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"campaign_export_{campaign.get('date', 'unknown').replace(':', '-')}.txt"
        )

        if not filename:
            return

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write(f"ЭКСПОРТ КАМПАНИИ\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Тип: {campaign.get('alert_type', 'Не указан')}\n")
                f.write(f"Дата создания: {campaign.get('date', 'Не указана')}\n")
                f.write(f"Статус: {campaign.get('status', 'unknown')}\n")
                f.write(f"Всего номеров: {campaign.get('total', 0)}\n")

                if campaign.get('status') == 'completed':
                    f.write(f"Успешно: {campaign.get('success', 0)}\n")
                    f.write(f"Ошибок: {campaign.get('fail', 0)}\n")
                elif campaign.get('status') == 'queued':
                    f.write(f"Запланировано на: {campaign.get('scheduled_time', 'Не указано')}\n")

                f.write(f"\nОтправитель: {campaign.get('sender_phone', 'Не указан')}\n")
                f.write(f"Шаблон СМС: {campaign.get('sms_template', 'Не указан')}\n")

                f.write("\n" + "=" * 80 + "\n")
                f.write("ТЕКСТЫ СООБЩЕНИЙ\n")
                f.write("=" * 80 + "\n\n")

                voice_text = campaign.get('voice_text', '')
                if voice_text:
                    f.write(f"📞 Текст для озвучивания:\n{voice_text}\n\n")

                sms_text = campaign.get('sms_text', '')
                if sms_text:
                    f.write(f"📱 Текст СМС:\n{sms_text}\n\n")

                f.write("=" * 80 + "\n")
                f.write("СПИСОК НОМЕРОВ И ЗАПРОСОВ\n")
                f.write("=" * 80 + "\n\n")

                phones_data = campaign.get('phones_data', [])
                for i, phone_info in enumerate(phones_data, 1):
                    f.write(f"\n{'-' * 80}\n")
                    f.write(f"ЗАПРОС #{i}\n")
                    f.write(f"{'-' * 80}\n\n")

                    f.write(f"Номер: {phone_info.get('number', 'Не указан')}\n")
                    f.write(f"Часовой пояс: UTC{phone_info.get('timezone', '+0')}\n\n")

                    # Выводим полный JSON запроса
                    request_info = phone_info.get('request_info', {})
                    if request_info:
                        f.write(f"URL: {request_info.get('url', 'Не указан')}\n")
                        f.write(f"Статус: {request_info.get('status', 'Не указан')}\n\n")

                        # Полный JSON запроса в читаемом формате
                        request_json = request_info.get('request_json', {})
                        if request_json:
                            f.write("JSON ЗАПРОСА:\n")
                            f.write(json.dumps(request_json, ensure_ascii=False, indent=4))
                            f.write("\n")

                    f.write("\n")

            messagebox.showinfo("Успех", f"Экспорт завершен!\n\nФайл сохранен:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте:\n{e}")

    def view_campaign_details(self, tab_type):
        """Просмотр детальной информации по кампании в отдельном окне"""
        # Определяем какое дерево использовать
        tree = self.queued_tree if tab_type == "queued" else self.completed_tree

        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите кампанию для просмотра")
            return

        # Получаем ID кампании
        item = selection[0]
        campaign_id = tree.item(item)['tags'][0]

        # Находим кампанию в истории
        history = self.load_history()
        campaign = None
        for c in history:
            if c.get('id') == campaign_id:
                campaign = c
                break

        if not campaign:
            messagebox.showerror("Ошибка", "Кампания не найдена")
            return

        # Создаем окно для просмотра
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Детальная информация по кампании")
        detail_window.geometry("900x700")
        detail_window.transient(self.root)

        # Рамка для текста
        text_frame = ttk.Frame(detail_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Скроллбар
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Текстовое поле с моноширинным шрифтом
        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            padx=10,
            pady=10
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        # Формируем содержимое (такое же как при экспорте)
        content = ""
        content += "=" * 80 + "\n"
        content += "ЭКСПОРТ КАМПАНИИ\n"
        content += "=" * 80 + "\n\n"
        content += f"Тип: {campaign.get('alert_type', 'Не указан')}\n"
        content += f"Дата создания: {campaign.get('date', 'Не указана')}\n"
        content += f"Статус: {campaign.get('status', 'unknown')}\n"
        content += f"Всего номеров: {campaign.get('total', 0)}\n"

        if campaign.get('status') == 'completed':
            content += f"Успешно: {campaign.get('success', 0)}\n"
            content += f"Ошибок: {campaign.get('fail', 0)}\n"
        elif campaign.get('status') == 'queued':
            content += f"Запланировано на: {campaign.get('scheduled_time', 'Не указано')}\n"

        content += f"\nОтправитель: {campaign.get('sender_phone', 'Не указан')}\n"
        content += f"Шаблон СМС: {campaign.get('sms_template', 'Не указан')}\n"

        content += "\n" + "=" * 80 + "\n"
        content += "ТЕКСТЫ СООБЩЕНИЙ\n"
        content += "=" * 80 + "\n\n"

        voice_text = campaign.get('voice_text', '')
        if voice_text:
            content += f"📞 Текст для озвучивания:\n{voice_text}\n\n"

        sms_text = campaign.get('sms_text', '')
        if sms_text:
            content += f"📱 Текст СМС:\n{sms_text}\n\n"

        content += "=" * 80 + "\n"
        content += "СПИСОК НОМЕРОВ И ЗАПРОСОВ\n"
        content += "=" * 80 + "\n\n"

        phones_data = campaign.get('phones_data', [])
        for i, phone_info in enumerate(phones_data, 1):
            content += f"\n{'-' * 80}\n"
            content += f"ЗАПРОС #{i}\n"
            content += f"{'-' * 80}\n\n"

            content += f"Номер: {phone_info.get('number', 'Не указан')}\n"
            content += f"Часовой пояс: UTC{phone_info.get('timezone', '+0')}\n\n"

            # Выводим полный JSON запроса
            request_info = phone_info.get('request_info', {})
            if request_info:
                content += f"URL: {request_info.get('url', 'Не указан')}\n"
                content += f"Статус: {request_info.get('status', 'Не указан')}\n\n"

                # Полный JSON запроса в читаемом формате
                request_json = request_info.get('request_json', {})
                if request_json:
                    content += "JSON ЗАПРОСА:\n"
                    content += json.dumps(request_json, ensure_ascii=False, indent=4)
                    content += "\n"

            content += "\n"

        # Вставляем содержимое
        text_widget.insert("1.0", content)
        text_widget.config(state='disabled')  # Делаем только для чтения

        # Рамка для кнопок
        btn_frame = ttk.Frame(detail_window)
        btn_frame.pack(pady=(0, 10))

        # Кнопка проверки доставки
        check_delivery_btn = tk.Button(
            btn_frame,
            text="Проверить доставку",
            font=("Roboto", 11, "bold"),
            bg=self.colors['primary'],
            fg='white',
            activebackground='#B8050E',
            activeforeground='white',
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: self.check_campaign_delivery_ui(campaign)
        )
        check_delivery_btn.pack(side=tk.LEFT, padx=5)

        # Кнопка закрытия
        close_btn = tk.Button(
            btn_frame,
            text="Закрыть",
            font=("Roboto", 11),
            bg='#E0E0E0',
            fg='#333333',
            activebackground='#D0D0D0',
            activeforeground='#333333',
            relief=tk.SOLID,
            borderwidth=1,
            cursor="hand2",
            padx=20,
            pady=10,
            command=detail_window.destroy
        )
        close_btn.pack(side=tk.LEFT, padx=5)

    def check_campaign_delivery_ui(self, campaign):
        """Проверка доставки кампании через лог-сервер"""
        if not HAS_PARAMIKO:
            messagebox.showerror(
                "Ошибка",
                "Библиотека paramiko не установлена.\n\n"
                "Установите её командой:\n"
                "pip install paramiko"
            )
            return

        # Извлекаем номера телефонов
        phones_data = campaign.get('phones_data', [])
        if not phones_data:
            messagebox.showwarning("Внимание", "В кампании нет номеров телефонов")
            return

        phone_numbers = [phone.get('number', '') for phone in phones_data if phone.get('number')]

        if not phone_numbers:
            messagebox.showwarning("Внимание", "Не удалось извлечь номера телефонов")
            return

        # Показываем окно ожидания
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Проверка доставки")
        progress_window.geometry("400x150")
        progress_window.transient(self.root)
        progress_window.grab_set()

        tk.Label(
            progress_window,
            text="Подключение к лог-серверу...",
            font=("Roboto", 12),
            pady=20
        ).pack()

        tk.Label(
            progress_window,
            text=f"Проверка {len(phone_numbers)} номеров",
            font=("Roboto", 10),
            fg='gray'
        ).pack()

        progress_window.update()

        try:
            # Проверяем доставку
            result = self.log_server.check_campaign_delivery(phone_numbers)

            progress_window.destroy()

            if not result['success']:
                messagebox.showerror("Ошибка", f"Ошибка при проверке доставки:\n{result.get('error', 'Неизвестная ошибка')}")
                return

            # Показываем результаты
            self.show_delivery_results(result, campaign)

        except Exception as e:
            progress_window.destroy()
            messagebox.showerror("Ошибка", f"Ошибка при проверке доставки:\n{str(e)}")

    def show_delivery_results(self, result, campaign):
        """Отображение результатов проверки доставки"""
        # Создаем окно результатов
        results_window = tk.Toplevel(self.root)
        results_window.title("Результаты проверки доставки")
        results_window.geometry("800x600")
        results_window.transient(self.root)

        # Заголовок
        header_frame = tk.Frame(results_window, bg=self.colors['primary'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text=f"Статистика доставки: {campaign.get('alert_type', 'кампания')}",
            font=("Roboto", 14, "bold"),
            bg=self.colors['primary'],
            fg='white'
        ).pack(pady=15)

        # Рамка для статистики
        stats_frame = tk.Frame(results_window, bg='white')
        stats_frame.pack(fill=tk.X, padx=20, pady=20)

        # Общая статистика
        total = result.get('total', 0)
        delivered = result.get('delivered', 0)
        failed = result.get('failed', 0)
        delivery_rate = (delivered / total * 100) if total > 0 else 0

        stats_text = f"""
┌─────────────────────────────────────────┐
│          ОБЩАЯ СТАТИСТИКА              │
├─────────────────────────────────────────┤
│  Всего номеров:     {total:>4}              │
│  Доставлено:        {delivered:>4}  ({delivery_rate:.1f}%)      │
│  Не доставлено:     {failed:>4}              │
└─────────────────────────────────────────┘
        """

        tk.Label(
            stats_frame,
            text=stats_text,
            font=("Consolas", 11),
            bg='white',
            fg='#333333',
            justify=tk.LEFT
        ).pack(pady=10)

        # Детальная информация
        details_label = tk.Label(
            results_window,
            text="Детальная информация по номерам:",
            font=("Roboto", 12, "bold"),
            bg='white'
        )
        details_label.pack(anchor=tk.W, padx=20, pady=(10, 5))

        # Рамка для деталей с прокруткой
        details_frame = tk.Frame(results_window)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        scrollbar = ttk.Scrollbar(details_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        details_text = tk.Text(
            details_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            padx=10,
            pady=10
        )
        details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=details_text.yview)

        # Формируем детальную информацию
        details_content = ""
        details = result.get('details', {})

        for i, (phone, info) in enumerate(details.items(), 1):
            status = "✓ ДОСТАВЛЕНО" if info['delivered'] else "✗ НЕ ДОСТАВЛЕНО"
            status_color = "green" if info['delivered'] else "red"

            details_content += f"\n{'-' * 70}\n"
            details_content += f"{i}. {phone} - {status}\n"
            details_content += f"{'-' * 70}\n"

            if info['count'] > 0:
                details_content += f"Записей в логах: {info['count']}\n"
                if info['entries']:
                    details_content += "\nПримеры записей из лога:\n"
                    for entry in info['entries'][:3]:  # Показываем до 3 записей
                        details_content += f"  • {entry}\n"
            else:
                details_content += "Записи в логах не найдены\n"

            details_content += "\n"

        details_text.insert("1.0", details_content)
        details_text.config(state='disabled')

        # Кнопка закрытия
        close_btn = tk.Button(
            results_window,
            text="Закрыть",
            font=("Roboto", 11),
            bg='#E0E0E0',
            fg='#333333',
            activebackground='#D0D0D0',
            activeforeground='#333333',
            relief=tk.SOLID,
            borderwidth=1,
            cursor="hand2",
            padx=30,
            pady=10,
            command=results_window.destroy
        )
        close_btn.pack(pady=(0, 20))

    def refresh_queued_history(self):
        """Обновление отображения кампаний в очереди"""
        # Очищаем таблицу
        for item in self.queued_tree.get_children():
            self.queued_tree.delete(item)

        # Загружаем историю
        history = self.load_history()

        # Фильтруем только кампании в очереди
        search_query = self.queued_search_var.get().strip()
        queued_campaigns = []

        for campaign in history:
            if campaign.get('status') == 'queued':
                # Поиск по номеру телефона
                if search_query:
                    phones = campaign.get('phones_data', [])
                    found = any(search_query in phone.get('number', '') for phone in phones)
                    if not found:
                        continue
                queued_campaigns.append(campaign)

        # Сортируем по дате (ближайшие сверху)
        queued_campaigns.sort(key=lambda x: x.get('scheduled_time', ''))

        # Заполняем таблицу
        for campaign in queued_campaigns:
            scheduled_time = campaign.get('scheduled_time', 'Не указано')
            alert_type = campaign.get('alert_type', '')
            total = campaign.get('total', 0)
            sender = campaign.get('sender_phone', 'Не указан')

            self.queued_tree.insert("", "end", values=(
                scheduled_time,
                alert_type,
                total,
                sender,
                "📄 Экспорт"
            ), tags=(campaign.get('id', ''),))

    def refresh_completed_history(self):
        """Обновление отображения завершенных кампаний"""
        # Очищаем таблицу
        for item in self.completed_tree.get_children():
            self.completed_tree.delete(item)

        # Загружаем историю
        history = self.load_history()

        # Фильтруем только завершенные кампании
        search_query = self.completed_search_var.get().strip()
        completed_campaigns = []

        for campaign in history:
            if campaign.get('status') == 'completed':
                # Поиск по номеру телефона
                if search_query:
                    phones = campaign.get('phones_data', [])
                    found = any(search_query in phone.get('number', '') for phone in phones)
                    if not found:
                        continue
                completed_campaigns.append(campaign)

        # Сортируем по дате (новые сверху)
        completed_campaigns.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        # Заполняем таблицу
        for campaign in completed_campaigns:
            status_icon = "✅ Успешно" if campaign.get('success', 0) > 0 else "❌ Ошибка"
            date_str = campaign.get('date', '')
            alert_type = campaign.get('alert_type', '')
            total = campaign.get('total', 0)
            success = campaign.get('success', 0)
            fail = campaign.get('fail', 0)

            self.completed_tree.insert("", "end", values=(
                status_icon,
                date_str,
                alert_type,
                total,
                success,
                fail
            ), tags=(campaign.get('id', ''),))


    def load_phones_from_file(self):
        """Загрузка номеров из TXT файла (поддержка 2 колонок: номер + часовой пояс)"""
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

        # Парсим номера (поддержка формата: номер или номер;часовой_пояс)
        new_phones = []
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):  # Пропускаем пустые строки и комментарии
                continue

            # Разделяем по табуляции или точке с запятой
            parts = re.split(r'[\t;,]', line)

            phone = parts[0].strip()
            timezone = parts[1].strip() if len(parts) > 1 else "+0"

            # Нормализуем номер
            normalized = self._normalize_phone_simple(phone)
            if normalized:
                # Проверяем что часовой пояс валидный
                if not re.match(r'^[+-]?\d{1,2}$', timezone):
                    timezone = "+0"

                phone_data = {
                    "number": normalized,
                    "timezone": timezone
                }
                new_phones.append(phone_data)

        # Добавляем к списку
        existing_numbers = [p.get('number') if isinstance(p, dict) else p for p in self.file_phones]

        # Проверяем есть ли дубликаты
        duplicates_count = sum(1 for phone_data in new_phones if phone_data['number'] in existing_numbers)

        if duplicates_count > 0:
            # Спрашиваем что делать с дублями
            remove_duplicates = messagebox.askyesno(
                "Обнаружены дубликаты",
                f"Найдено дубликатов: {duplicates_count}\n\n"
                f"Удалить дубликаты?\n\n"
                f"ДА - добавить только уникальные номера\n"
                f"НЕТ - добавить все номера (включая дубли)"
            )
        else:
            remove_duplicates = True  # Если дублей нет, не имеет значения

        added_count = 0
        for phone_data in new_phones:
            if remove_duplicates:
                # Добавляем только если нет в списке
                if phone_data['number'] not in existing_numbers:
                    self.file_phones.append(phone_data)
                    added_count += 1
            else:
                # Добавляем все
                self.file_phones.append(phone_data)
                added_count += 1

        self._update_phones_listbox()

        messagebox.showinfo(
            "Загружено",
            f"Добавлено номеров: {added_count}\n"
            f"Всего в списке: {len(self.file_phones)}\n\n"
            f"💡 Формат файла:\n"
            f"номер;часовой_пояс\n"
            f"Например: +79991234567;+3"
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
        for i, phone_info in enumerate(self.file_phones, 1):
            if isinstance(phone_info, dict):
                display = f"{i}. {phone_info['number']} (UTC{phone_info['timezone']})"
            else:
                display = f"{i}. {phone_info}"
            self.phones_listbox.insert(tk.END, display)

        self.file_count_label.config(text=f"Загружено: {len(self.file_phones)} номеров")

    def clear_file_phones(self):
        """Очистка списка номеров"""
        self.file_phones = []
        self._update_phones_listbox()

    def export_example_file(self):
        """Экспорт примера файла с тестовыми данными"""
        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="example_phones.txt"
        )

        if not filename:
            return

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# Пример файла со списком номеров телефонов и часовыми поясами\n")
                f.write("# Формат: номер_телефона;часовой_пояс_UTC\n")
                f.write("# Часовой пояс указывается с + или - (например: +3, -5, +0)\n")
                f.write("# Строки, начинающиеся с #, игнорируются\n")
                f.write("#\n")
                f.write("# Примеры:\n\n")
                f.write("+79991234567;+3\n")
                f.write("+79992345678;+5\n")
                f.write("+79993456789;+0\n")
                f.write("+79994567890;-2\n")
                f.write("+79995678901;+7\n")
                f.write("\n# Можно также использовать табуляцию или запятую как разделитель:\n")
                f.write("# +79996789012\t+3\n")
                f.write("# +79997890123,+5\n")
                f.write("\n# Если часовой пояс не указан, используется UTC+0:\n")
                f.write("# +79998901234\n")

            messagebox.showinfo(
                "Успех",
                f"Пример файла создан!\n\n"
                f"Файл сохранен:\n{filename}\n\n"
                f"Откройте его в текстовом редакторе,\n"
                f"замените тестовые данные на реальные\n"
                f"и загрузите через кнопку '📂 Выбрать TXT файл'"
            )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании файла:\n{e}")

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

        # Валидация номера отправителя (обязательное поле)
        sender_phone = self.sender_phone.get().strip()
        if not sender_phone or len(sender_phone) != 11 or not sender_phone.startswith('7'):
            messagebox.showwarning("Внимание", "Заполните обязательное поле!\n\n'Номер с которого совершать вызов'\nДолжен быть 11 цифр, начинается с 7")
            return

        alert_type_key = self.selected_alert_type.get()
        alert_type = ALERT_TYPES[alert_type_key]

        # Валидация номера шаблона СМС для типов "sms" и "call_sms"
        sms_template = self.sms_template.get().strip()
        if alert_type_key in ["sms", "call_sms"]:
            if not sms_template:
                messagebox.showwarning("Внимание", "Заполните обязательное поле!\n\n'Номер шаблона СМС' обязателен для этого типа оповещения")
                return

        # Формируем phones_data с часовыми поясами
        phones_data = []
        for phone_info in self.file_phones:
            if isinstance(phone_info, dict):
                phones_data.append(phone_info)
            else:
                # Старый формат - только номер
                phones_data.append({"number": phone_info, "timezone": "+0"})

        # Формируем список для отправки
        employees_to_call = []
        for i, phone_info in enumerate(phones_data):
            phone = phone_info.get("number") if isinstance(phone_info, dict) else phone_info
            employees_to_call.append({
                "id": f"file_{i}",
                "name": f"Номер {phone}",
                "phone": phone
            })

        # Подготовка расширенных данных кампании
        campaign_extra = {
            "voice_text": voice_text,
            "sms_text": sms_text,
            "sender_phone": sender_phone,
            "sms_template": self.sms_template.get().strip(),
            "phones_data": phones_data
        }

        # Проверяем отложенную отправку
        if self.delayed_send.get():
            # Валидация даты и времени
            send_date = self.send_date.get().strip()
            send_time = self.send_time.get().strip()

            try:
                scheduled_datetime = datetime.strptime(f"{send_date} {send_time}", "%Y-%m-%d %H:%M")
                if scheduled_datetime <= datetime.now():
                    messagebox.showwarning("Внимание", "Дата и время должны быть в будущем!")
                    return
            except ValueError:
                messagebox.showwarning("Внимание", "Некорректный формат даты или времени!\n\nФормат: ГГГГ-ММ-ДД ЧЧ:ММ")
                return

            campaign_extra["scheduled_time"] = f"{send_date} {send_time}"

            # Сохраняем кампанию в очередь
            confirm_text = f"Тип: {alert_type['name']}\n\n"
            confirm_text += f"Количество номеров: {len(employees_to_call)}\n\n"
            confirm_text += f"⏰ Запланировано на: {send_date} {send_time}\n\n"

            if voice_text:
                confirm_text += f"📞 Текст для озвучивания:\n{voice_text[:100]}{'...' if len(voice_text) > 100 else ''}\n\n"

            if sms_text:
                confirm_text += f"📱 Текст СМС:\n{sms_text[:100]}{'...' if len(sms_text) > 100 else ''}\n\n"

            confirm_text += "Добавить в очередь?"

            if messagebox.askyesno("Подтверждение", confirm_text):
                import uuid
                # Создаем кампанию в очереди
                campaign_data = {
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "alert_type": alert_type["name"],
                    "source": "Конструктор",
                    "total": len(employees_to_call),
                    "status": "queued",
                    **campaign_extra
                }
                self.add_campaign_to_history(campaign_data)
                messagebox.showinfo("Успех", f"Кампания добавлена в очередь!\n\nЗапуск: {send_date} {send_time}")
        else:
            # Немедленная отправка
            confirm_text = f"Тип: {alert_type['name']}\n\n"
            confirm_text += f"Количество номеров: {len(employees_to_call)}\n\n"

            if voice_text:
                confirm_text += f"📞 Текст для озвучивания:\n{voice_text[:100]}{'...' if len(voice_text) > 100 else ''}\n\n"

            if sms_text:
                confirm_text += f"📱 Текст СМС:\n{sms_text[:100]}{'...' if len(sms_text) > 100 else ''}\n\n"

            confirm_text += "Отправить оповещения?"

            # Подтверждение
            if messagebox.askyesno("Подтверждение", confirm_text):
                self.send_alerts(employees_to_call, alert_type, "Конструктор", campaign_extra)

    def send_alerts(self, employees, alert_type, source, campaign_extra=None, show_ui=True):
        # DEBUG: Логируем запуск кампании
        self.debug_logger.info(f"🚀 Запуск кампании", {
            "source": source,
            "alert_type": alert_type.get("name"),
            "total_employees": len(employees),
            "show_ui": show_ui
        })

        success, fail = 0, 0
        requests_log = []

        # Создаем прогресс-окно только если show_ui=True
        if show_ui:
            progress = tk.Toplevel(self.root)
            progress.title("Отправка...")
            progress.geometry("400x160")
            progress.transient(self.root)
            progress.grab_set()

            label = ttk.Label(progress, text="Отправка...", font=("Segoe UI", 10))
            label.pack(pady=(20, 5))

            # Процентный индикатор
            percent_label = ttk.Label(progress, text="0%", font=("Segoe UI", 12, "bold"), foreground="#0066CC")
            percent_label.pack(pady=(0, 10))
        else:
            progress = None
            label = None
            percent_label = None

        if show_ui:
            bar = ttk.Progressbar(progress, length=350, maximum=len(employees), mode='determinate')
            bar.pack(pady=10)
        else:
            bar = None

        for i, emp in enumerate(employees):
            if show_ui:
                current_percent = int(((i + 1) / len(employees)) * 100)
                label.config(text=f"Отправка: {emp['name']}...")
                percent_label.config(text=f"{current_percent}%")
                bar["value"] = i + 1
                progress.update()

            # Получаем данные для запроса
            phone_info = campaign_extra.get('phones_data', [])[i] if campaign_extra else {}
            timezone = phone_info.get('timezone', '+0') if isinstance(phone_info, dict) else '+0'
            voice_text = campaign_extra.get('voice_text', '') if campaign_extra else ''
            sms_text = campaign_extra.get('sms_text', '') if campaign_extra else ''
            sender_phone = campaign_extra.get('sender_phone', '') if campaign_extra else ''
            sms_template = campaign_extra.get('sms_template', '') if campaign_extra else ''

            # Получаем ключ типа оповещения из ALERT_TYPES
            alert_type_key = None
            for key, alert in ALERT_TYPES.items():
                if alert['name'] == alert_type['name']:
                    alert_type_key = key
                    break

            request_result, request_data = self.send_single_request(
                phone=emp["phone"],
                timezone=timezone,
                voice_text=voice_text,
                sms_text=sms_text,
                sender_phone=sender_phone,
                sms_template=sms_template,
                alert_type_key=alert_type_key or 'call'
            )

            # Логируем информацию о запросе с полным JSON
            request_info = {
                "url": self.config.api_url,
                "status": "success" if request_result else "failed",
                "request_json": request_data  # Полный JSON запроса
            }

            # Обновляем phone_data с информацией о запросе
            if campaign_extra and 'phones_data' in campaign_extra and i < len(campaign_extra['phones_data']):
                campaign_extra['phones_data'][i]['request_info'] = request_info

            if request_result:
                success += 1
                self._log_action("SUCCESS", f"{source} | {emp['name']} | {emp['phone']} | CONNID: {self.current_connid - 1}")
            else:
                fail += 1
                self._log_action("FAIL", f"{source} | {emp['name']} | {emp['phone']}")

        if show_ui:
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
            "status": "completed",
            "launched": True
        }

        # Добавляем расширенные данные если есть
        if campaign_extra:
            campaign_data.update(campaign_extra)

        self.add_campaign_to_history(campaign_data)

        if show_ui:
            if fail == 0:
                messagebox.showinfo("Успех", f"Отправлено: {success}")
            else:
                messagebox.showwarning("Внимание", f"Успешно: {success}\nОшибок: {fail}")

    def check_scheduled_campaigns(self):
        """Проверяет и запускает отложенные кампании"""
        try:
            if not os.path.exists(HISTORY_FILE):
                return

            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                campaigns = json.load(f)

            current_time = datetime.now()
            campaigns_to_update = []

            for campaign in campaigns:
                # Проверяем только кампании в очереди
                if campaign.get("status") != "queued":
                    continue

                scheduled_time_str = campaign.get("scheduled_time")
                if not scheduled_time_str:
                    continue

                # Парсим запланированное время
                try:
                    scheduled_time = datetime.strptime(scheduled_time_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    continue

                # Если время наступило, запускаем кампанию
                if current_time >= scheduled_time:
                    # Получаем данные для запуска
                    phones_data = campaign.get("phones_data", [])
                    alert_type_name = campaign.get("alert_type", "Позвонить")

                    # Находим соответствующий тип оповещения
                    alert_type = None
                    for key, alert in ALERT_TYPES.items():
                        if alert['name'] == alert_type_name:
                            alert_type = alert
                            break

                    if not alert_type or not phones_data:
                        continue

                    # Формируем список для отправки
                    employees_to_call = []
                    for phone_info in phones_data:
                        employees_to_call.append({
                            "name": phone_info.get("number", ""),
                            "phone": phone_info.get("number", "")
                        })

                    # Подготавливаем campaign_extra
                    campaign_extra = {
                        "voice_text": campaign.get("voice_text", ""),
                        "sms_text": campaign.get("sms_text", ""),
                        "sender_phone": campaign.get("sender_phone", ""),
                        "sms_template": campaign.get("sms_template", ""),
                        "phones_data": phones_data
                    }

                    # Запускаем отправку (без UI подтверждения)
                    try:
                        self.send_alerts(employees_to_call, alert_type, "Автозапуск (Отложенная отправка)", campaign_extra, show_ui=False)
                        # Отмечаем кампанию как запущенную
                        campaign["status"] = "completed"
                        campaign["launched"] = True
                        campaigns_to_update.append(campaign)
                    except Exception as e:
                        print(f"Ошибка запуска отложенной кампании: {e}")
                        campaign["status"] = "failed"
                        campaign["error"] = str(e)
                        campaigns_to_update.append(campaign)

            # Обновляем статусы кампаний в файле
            if campaigns_to_update:
                for updated_campaign in campaigns_to_update:
                    for i, campaign in enumerate(campaigns):
                        if campaign.get("id") == updated_campaign.get("id"):
                            campaigns[i] = updated_campaign
                            break

                with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                    json.dump(campaigns, f, ensure_ascii=False, indent=4)

                # Обновляем отображение истории
                self.refresh_queued_history()
                self.refresh_completed_history()

        except Exception as e:
            print(f"Ошибка проверки отложенных кампаний: {e}")

        # Запланировать следующую проверку через 60 секунд
        self.root.after(60000, self.check_scheduled_campaigns)

    def send_single_request(self, phone, timezone, voice_text, sms_text, sender_phone, sms_template, alert_type_key):
        """
        Отправка запроса на API

        Args:
            phone: Номер телефона (ANI)
            timezone: Часовой пояс (TZ_DBID) из файла, например "+3"
            voice_text: Текст для озвучивания
            sms_text: Текст СМС
            sender_phone: Номер отправителя (CPN)
            sms_template: Номер шаблона СМС
            alert_type_key: Тип оповещения ("call", "call_sms", "sms")

        Returns:
            tuple: (success: bool, request_data: dict) - результат и данные запроса
        """
        try:
            import uuid as uuid_module

            # Генерируем уникальный CONNID
            connid = str(uuid_module.uuid4()).upper()

            # Конвертируем часовой пояс в формат TZ_DBID
            # Например: "+3" -> "3", "-5" -> "-5", "+0" -> "0"
            tz_dbid = timezone.replace('+', '') if timezone else "0"

            # Формируем ADD_PROP в зависимости от типа
            add_prop = {}
            service = "MONITOR_BANK"  # По умолчанию

            if alert_type_key == "call":
                # Только звонок
                add_prop = {
                    "text_voice": voice_text,
                    "CPN": sender_phone
                }
                service = "MONITOR_BANK"

            elif alert_type_key == "call_sms":
                # Звонок + СМС
                add_prop = {
                    "text_voice": voice_text,
                    "CPN": sender_phone,
                    "sms_text": sms_text,
                    "template": sms_template
                }
                service = "IVR_Quality_Control"

            elif alert_type_key == "sms":
                # Только СМС
                add_prop = {
                    "text_voice": voice_text,
                    "CPN": sender_phone,
                    "sms_text": sms_text,
                    "template": sms_template
                }
                service = "IVR_Quality_Control_SMS"

            # Формируем данные запроса
            data = {
                "ANI": phone,
                "CONNID": connid,
                "TZ_DBID": tz_dbid,
                "CUSTID": "499287966839",
                "SERVICE": service,
                "DELAY": "1",
                "ADD_PROP": json.dumps(add_prop, ensure_ascii=False)
            }

            json_data = json.dumps(data, ensure_ascii=False).encode("utf-8")

            # DEBUG: Логируем запрос перед отправкой
            self.debug_logger.debug(f"Отправка запроса на номер {phone}", {
                "phone": phone,
                "alert_type": alert_type_key,
                "service": service,
                "url": self.config.api_url,
                "request_data": data
            })

            request = urllib.request.Request(
                self.config.api_url,
                data=json_data,
                headers={"Content-Type": "application/json; charset=utf-8"},
                method="POST"
            )

            ssl_context = ssl.create_default_context()
            if not self.config.verify_ssl:
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE

            with urllib.request.urlopen(request, context=ssl_context, timeout=self.config.api_timeout):
                pass

            # DEBUG: Успешная отправка
            self.debug_logger.info(f"✅ Успешная отправка на {phone}", {"connid": connid})

            self.current_connid += 1
            self._save_connid()
            return (True, data)

        except Exception as e:
            # DEBUG: Ошибка отправки
            error_data = {
                "phone": phone,
                "error": str(e),
                "error_type": type(e).__name__
            }
            if 'data' in locals():
                error_data["request_data"] = data

            self.debug_logger.error(f"❌ Ошибка отправки на {phone}", error_data)
            print(f"Ошибка: {phone} - {e}")
            # Возвращаем данные запроса даже при ошибке
            return (False, data if 'data' in locals() else {})

    def toggle_theme(self):
        """Переключение между светлой и темной темой"""
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        MTSTheme.save_theme(new_theme)

        # Показываем сообщение о перезапуске
        messagebox.showinfo(
            "Смена темы",
            f"Тема изменена на {'темную' if new_theme == 'dark' else 'светлую'}!\n\n"
            f"Перезапустите приложение для применения изменений."
        )

    def get_dashboard_metrics(self):
        """Получение метрик для Dashboard"""
        queued_count = 0
        completed_count = 0
        total_sent = 0

        try:
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)

                    for campaign in history:
                        status = campaign.get("status", "")
                        if status == "queued":
                            queued_count += 1
                        elif status == "completed":
                            completed_count += 1

                        # Подсчет отправленных сообщений
                        phones = campaign.get("phones", [])
                        if isinstance(phones, list):
                            total_sent += len(phones)
        except (IOError, json.JSONDecodeError):
            pass

        return queued_count, completed_count, total_sent

    def on_closing(self):
        self.data_loader.disconnect()
        self.root.destroy()


def main():
    # Показываем окно авторизации
    login_root = tk.Tk()
    login_window = LoginWindow(login_root)
    login_root.mainloop()

    # Проверяем результат авторизации
    if not login_window.authenticated:
        print("Авторизация отменена")
        return

    # Запускаем основное приложение
    root = tk.Tk()
    app = IVRCallerApp(root, username=login_window.username)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
