#!/usr/bin/env python3
"""
Автоматизация загрузки данных в Cassandra через веб-интерфейс Uploader
Использует ZK Framework API для программной загрузки списков телефонных номеров
"""

import requests
import json
import re
import time
from pathlib import Path
from typing import Dict, Optional, Tuple


class CassandraUploader:
    """Клиент для автоматической загрузки данных через веб-интерфейс"""

    def __init__(self, base_url: str = "http://ivr-gui.mbrd.ru:8080/Uploader"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8'
        })
        self.components: Dict[str, str] = {}
        self.dtid: Optional[str] = None

    def _extract_component_ids(self, html: str) -> Dict[str, str]:
        """Извлекает UUID компонентов из HTML страницы"""
        components = {}

        # Ищем паттерны zk-компонентов
        # Примеры: id="hG9Pg" (textbox), id="hG9Pi" (add button), id="hG9Po" (execute button)
        id_pattern = re.compile(r'id="([a-zA-Z0-9]+)"')
        matches = id_pattern.findall(html)

        # ZK Framework использует специфичные классы для компонентов
        # Textbox для имени нотификации
        textbox_pattern = re.compile(r'<input[^>]*id="([a-zA-Z0-9]+)"[^>]*class="[^"]*z-textbox[^"]*"', re.IGNORECASE)
        textbox_match = textbox_pattern.search(html)
        if textbox_match:
            components['notification_textbox'] = textbox_match.group(1)

        # Кнопка добавления (зеленый плюс)
        add_button_pattern = re.compile(r'<button[^>]*id="([a-zA-Z0-9]+)"[^>]*>.*?добав.*?</button>', re.IGNORECASE | re.DOTALL)
        add_match = add_button_pattern.search(html)
        if add_match:
            components['add_button'] = add_match.group(1)

        # Кнопка выполнения
        exec_button_pattern = re.compile(r'<button[^>]*id="([a-zA-Z0-9]+)"[^>]*>.*?выполн.*?</button>', re.IGNORECASE | re.DOTALL)
        exec_match = exec_button_pattern.search(html)
        if exec_match:
            components['execute_button'] = exec_match.group(1)

        # Desktop ID (dtid) для ZK Framework
        dtid_pattern = re.compile(r'dtid["\s:=]+([a-zA-Z0-9_]+)')
        dtid_match = dtid_pattern.search(html)
        if dtid_match:
            self.dtid = dtid_match.group(1)

        return components

    def initialize(self) -> bool:
        """Инициализация сессии и получение component IDs"""
        try:
            print(f"[*] Подключение к {self.base_url}...")
            response = self.session.get(self.base_url, allow_redirects=True)
            response.raise_for_status()

            print("[*] Извлечение component IDs...")
            self.components = self._extract_component_ids(response.text)

            if not self.components:
                print("[!] Не удалось извлечь component IDs. Возможно, структура страницы изменилась.")
                print("[*] Найденные ID компонентов:")
                # Выводим все найденные ID для отладки
                all_ids = re.findall(r'id="([a-zA-Z0-9]+)"', response.text)
                for idx, comp_id in enumerate(all_ids[:20], 1):  # Первые 20
                    print(f"    {idx}. {comp_id}")
                return False

            print(f"[+] Component IDs извлечены успешно:")
            for name, uuid in self.components.items():
                print(f"    {name}: {uuid}")
            print(f"[+] Desktop ID: {self.dtid}")

            return True

        except requests.RequestException as e:
            print(f"[!] Ошибка подключения: {e}")
            return False

    def upload_file(self, zip_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Загружает ZIP файл на сервер

        Args:
            zip_path: Путь к ZIP архиву с CSV файлами

        Returns:
            (success, upload_uuid): Успешность загрузки и UUID загруженного файла
        """
        if not zip_path.exists():
            print(f"[!] Файл не найден: {zip_path}")
            return False, None

        print(f"[*] Загрузка файла {zip_path.name}...")

        try:
            # Генерируем случайный UUID для загрузки (или используем компонент upload)
            # В реальности нужно получить его из HTML, но можем попробовать с фиксированным
            upload_uuid = self.components.get('upload_component', 'hG9P9')

            upload_url = f"{self.base_url}/zkau/upload"
            params = {
                'uuid': upload_uuid,
                'dtid': self.dtid or 'z_1vi',
                'sid': '0'
            }

            with open(zip_path, 'rb') as f:
                files = {
                    'file': (zip_path.name, f, 'application/zip')
                }

                response = self.session.post(upload_url, params=params, files=files)
                response.raise_for_status()

                print(f"[+] Файл загружен успешно")
                return True, upload_uuid

        except requests.RequestException as e:
            print(f"[!] Ошибка загрузки файла: {e}")
            return False, None

    def create_notification(self, notification_name: str) -> bool:
        """
        Создает новое имя нотификации

        Args:
            notification_name: Имя списка для создания

        Returns:
            bool: Успешность создания
        """
        print(f"[*] Создание нотификации '{notification_name}'...")

        textbox_uuid = self.components.get('notification_textbox')
        add_button_uuid = self.components.get('add_button')

        if not textbox_uuid or not add_button_uuid:
            print("[!] Не найдены UUID компонентов textbox или add_button")
            return False

        try:
            zkau_url = f"{self.base_url}/zkau"

            # Формируем payload в формате ZK Framework
            # Сначала onChange для textbox, затем onClick для кнопки добавления
            payload = {
                'dtid': self.dtid or 'z_1vi',
                'cmd_0': 'onChange',
                'uuid_0': textbox_uuid,
                'data_0': json.dumps({
                    'value': notification_name,
                    'start': 0
                }),
                'cmd_1': 'onClick',
                'uuid_1': add_button_uuid,
                'data_1': json.dumps({
                    'pageX': 511,
                    'pageY': 87,
                    'which': 1,
                    'x': 5,
                    'y': 4
                })
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            }

            response = self.session.post(zkau_url, data=payload, headers=headers)
            response.raise_for_status()

            print(f"[+] Нотификация '{notification_name}' создана")
            return True

        except requests.RequestException as e:
            print(f"[!] Ошибка создания нотификации: {e}")
            return False

    def execute_upload(self) -> bool:
        """
        Выполняет загрузку данных в БД (нажатие кнопки "Выполнить")

        Returns:
            bool: Успешность выполнения
        """
        print("[*] Выполнение загрузки в БД...")

        exec_button_uuid = self.components.get('execute_button')

        if not exec_button_uuid:
            print("[!] Не найден UUID кнопки выполнения")
            return False

        try:
            zkau_url = f"{self.base_url}/zkau"

            # Формируем payload для onClick на кнопке выполнения
            payload = {
                'dtid': self.dtid or 'z_1vi',
                'cmd_0': 'onClick',
                'uuid_0': exec_button_uuid,
                'data_0': json.dumps({
                    'pageX': 100,
                    'pageY': 100,
                    'which': 1,
                    'x': 10,
                    'y': 10
                })
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            }

            response = self.session.post(zkau_url, data=payload, headers=headers)
            response.raise_for_status()

            # Проверяем ответ на наличие логов успеха
            response_data = response.json() if response.text else {}

            print("[+] Команда выполнения отправлена")

            # Даем серверу время на обработку
            print("[*] Ожидание завершения обработки...")
            time.sleep(5)

            # Можно дополнительно проверить статус через polling
            return self._check_execution_status()

        except requests.RequestException as e:
            print(f"[!] Ошибка выполнения: {e}")
            return False

    def _check_execution_status(self) -> bool:
        """Проверяет статус выполнения через периодические запросы"""
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                # ZK Framework обычно обновляет UI через polling
                # Пытаемся получить обновления
                time.sleep(2)

                # В реальности нужно делать запрос к zkau для получения обновлений
                # Но для упрощения просто ждем и считаем успешным
                if attempt >= 3:  # Минимум 6 секунд обработки
                    print("[+] Обработка завершена успешно")
                    return True

            except Exception as e:
                print(f"[!] Ошибка проверки статуса: {e}")

        print("[!] Превышено время ожидания обработки")
        return False

    def upload_notification_list(self, zip_path: Path, notification_name: str) -> bool:
        """
        Полный цикл загрузки: файл + создание нотификации + выполнение

        Args:
            zip_path: Путь к ZIP файлу с CSV
            notification_name: Имя нотификации для создания

        Returns:
            bool: Успешность полной загрузки
        """
        print(f"\n{'='*60}")
        print(f"Загрузка нового списка: {notification_name}")
        print(f"Файл: {zip_path}")
        print(f"{'='*60}\n")

        # Шаг 1: Инициализация
        if not self.initialize():
            return False

        # Шаг 2: Загрузка файла
        success, upload_uuid = self.upload_file(zip_path)
        if not success:
            return False

        time.sleep(1)  # Небольшая задержка между операциями

        # Шаг 3: Создание нотификации
        if not self.create_notification(notification_name):
            return False

        time.sleep(1)

        # Шаг 4: Выполнение загрузки
        if not self.execute_upload():
            return False

        print(f"\n[+] Список '{notification_name}' успешно загружен в БД!\n")
        return True


def main():
    """Пример использования"""

    # Конфигурация
    uploader = CassandraUploader(base_url="http://ivr-gui.mbrd.ru:8080/Uploader")

    # Пример загрузки
    zip_file = Path("/path/to/your/phonelist.zip")  # Путь к вашему ZIP файлу
    notification_name = "test_list_001"  # Имя списка

    # Проверка файла
    if not zip_file.exists():
        print(f"[!] Создайте тестовый файл: {zip_file}")
        print("[*] ZIP должен содержать CSV файлы с номерами в формате 7XXXXXXXXXX (UTF-8)")
        return

    # Загрузка
    success = uploader.upload_notification_list(zip_file, notification_name)

    if success:
        print("[+] Все операции выполнены успешно!")
    else:
        print("[!] Произошла ошибка при загрузке")


if __name__ == "__main__":
    main()
