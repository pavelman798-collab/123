#!/usr/bin/env python3
"""
Примеры использования Cassandra Uploader
"""

from cassandra_uploader import CassandraUploader
from pathlib import Path
import sys


def example_single_upload():
    """Пример 1: Загрузка одного списка"""

    print("\n" + "="*60)
    print("Пример 1: Загрузка одного списка")
    print("="*60 + "\n")

    uploader = CassandraUploader()

    # Путь к вашему ZIP файлу
    zip_file = Path("phonelist.zip")

    # Имя нотификации (списка)
    notification_name = "test_list_001"

    # Проверка существования файла
    if not zip_file.exists():
        print(f"[!] Файл не найден: {zip_file}")
        print("[*] Создайте файл phonelist.zip с CSV файлами телефонных номеров")
        return False

    # Загрузка
    success = uploader.upload_notification_list(zip_file, notification_name)

    if success:
        print("\n[+] Загрузка завершена успешно!")
        return True
    else:
        print("\n[!] Произошла ошибка при загрузке")
        return False


def example_batch_upload():
    """Пример 2: Пакетная загрузка нескольких списков"""

    print("\n" + "="*60)
    print("Пример 2: Пакетная загрузка")
    print("="*60 + "\n")

    # Список файлов для загрузки
    uploads = [
        ("region_moscow.zip", "moscow_calling_list"),
        ("region_spb.zip", "spb_calling_list"),
        ("region_kazan.zip", "kazan_calling_list"),
    ]

    results = []

    for zip_filename, notification_name in uploads:
        zip_path = Path(zip_filename)

        if not zip_path.exists():
            print(f"[!] Пропуск {zip_filename} - файл не найден")
            results.append(False)
            continue

        print(f"\n--- Загрузка {notification_name} ---")

        uploader = CassandraUploader()
        success = uploader.upload_notification_list(zip_path, notification_name)

        results.append(success)

        if success:
            print(f"[+] {notification_name} загружен успешно")
        else:
            print(f"[!] Ошибка загрузки {notification_name}")

        # Небольшая задержка между загрузками
        import time
        time.sleep(3)

    # Итоговая статистика
    print("\n" + "="*60)
    print("Итоги пакетной загрузки:")
    print(f"  Успешно: {sum(results)} из {len(results)}")
    print(f"  Ошибок: {len(results) - sum(results)}")
    print("="*60 + "\n")

    return all(results)


def example_with_validation():
    """Пример 3: Загрузка с предварительной валидацией"""

    print("\n" + "="*60)
    print("Пример 3: Загрузка с валидацией")
    print("="*60 + "\n")

    zip_file = Path("phonelist.zip")
    notification_name = "validated_list"

    # Валидация файла
    print("[*] Валидация файла...")

    if not zip_file.exists():
        print(f"[!] Файл не существует: {zip_file}")
        return False

    file_size = zip_file.stat().st_size
    file_size_mb = file_size / (1024 * 1024)

    print(f"[*] Размер файла: {file_size_mb:.2f} MB")

    if file_size_mb > 100:
        print("[!] Файл слишком большой (максимум 100 MB)")
        return False

    if file_size < 100:
        print("[!] Файл подозрительно маленький")
        return False

    # Валидация имени нотификации
    print("[*] Валидация имени нотификации...")

    if not notification_name:
        print("[!] Имя нотификации не может быть пустым")
        return False

    if len(notification_name) < 3:
        print("[!] Имя нотификации слишком короткое (минимум 3 символа)")
        return False

    # Проверка на спецсимволы
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+$', notification_name):
        print("[!] Имя нотификации может содержать только буквы, цифры, _ и -")
        return False

    print("[+] Валидация пройдена")

    # Загрузка
    print("\n[*] Начало загрузки...")
    uploader = CassandraUploader()
    success = uploader.upload_notification_list(zip_file, notification_name)

    return success


def example_custom_config():
    """Пример 4: Использование с пользовательской конфигурацией"""

    print("\n" + "="*60)
    print("Пример 4: Пользовательская конфигурация")
    print("="*60 + "\n")

    # Можно указать другой URL если есть несколько серверов
    custom_url = "http://ivr-gui.mbrd.ru:8080/Uploader"

    uploader = CassandraUploader(base_url=custom_url)

    # Дополнительные headers если требуется аутентификация
    uploader.session.headers.update({
        'X-Custom-Header': 'value',
        # 'Authorization': 'Bearer token',  # Если требуется
    })

    zip_file = Path("phonelist.zip")
    notification_name = "custom_config_list"

    if not zip_file.exists():
        print(f"[!] Файл не найден: {zip_file}")
        return False

    success = uploader.upload_notification_list(zip_file, notification_name)

    return success


def interactive_mode():
    """Интерактивный режим с запросом параметров"""

    print("\n" + "="*60)
    print("Интерактивный режим загрузки")
    print("="*60 + "\n")

    try:
        # Запрос пути к файлу
        zip_path_str = input("Введите путь к ZIP файлу: ").strip()
        zip_file = Path(zip_path_str)

        if not zip_file.exists():
            print(f"[!] Файл не найден: {zip_file}")
            return False

        # Запрос имени нотификации
        notification_name = input("Введите имя нотификации (списка): ").strip()

        if not notification_name:
            print("[!] Имя не может быть пустым")
            return False

        # Подтверждение
        print(f"\n[*] Файл: {zip_file}")
        print(f"[*] Имя: {notification_name}")
        confirm = input("\nПродолжить? (y/n): ").strip().lower()

        if confirm != 'y':
            print("[*] Отменено пользователем")
            return False

        # Загрузка
        uploader = CassandraUploader()
        success = uploader.upload_notification_list(zip_file, notification_name)

        return success

    except KeyboardInterrupt:
        print("\n[*] Прервано пользователем")
        return False


def main():
    """Главное меню"""

    examples = {
        '1': ('Загрузка одного списка', example_single_upload),
        '2': ('Пакетная загрузка', example_batch_upload),
        '3': ('Загрузка с валидацией', example_with_validation),
        '4': ('Пользовательская конфигурация', example_custom_config),
        '5': ('Интерактивный режим', interactive_mode),
    }

    print("\n" + "="*60)
    print("Cassandra Uploader - Примеры использования")
    print("="*60)
    print("\nВыберите пример:")

    for key, (description, _) in examples.items():
        print(f"  {key}. {description}")

    print("  0. Выход")
    print()

    try:
        choice = input("Ваш выбор: ").strip()

        if choice == '0':
            print("Выход")
            return

        if choice in examples:
            _, example_func = examples[choice]
            success = example_func()

            if success:
                print("\n[+] Пример выполнен успешно!")
            else:
                print("\n[!] Пример завершился с ошибкой")
                sys.exit(1)
        else:
            print(f"[!] Неверный выбор: {choice}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n[*] Прервано пользователем")
        sys.exit(0)


if __name__ == "__main__":
    main()
