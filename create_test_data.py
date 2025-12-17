#!/usr/bin/env python3
"""
Скрипт для создания тестовых данных для загрузки в Cassandra Uploader
Генерирует ZIP архив с CSV файлами телефонных номеров
"""

import csv
import zipfile
import random
from pathlib import Path


def generate_phone_numbers(count: int, region_code: str = "999") -> list:
    """
    Генерирует список телефонных номеров в формате 7XXXXXXXXXX

    Args:
        count: Количество номеров для генерации
        region_code: Код региона (3 цифры после 7)

    Returns:
        list: Список телефонных номеров
    """
    phone_numbers = []

    for _ in range(count):
        # Формат: 7 + region_code(3) + 7 цифр = 11 цифр
        subscriber = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        phone = f"7{region_code}{subscriber}"
        phone_numbers.append(phone)

    return phone_numbers


def create_csv_file(filename: Path, phone_numbers: list):
    """
    Создает CSV файл с номерами телефонов

    Args:
        filename: Путь к CSV файлу
        phone_numbers: Список номеров
    """
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for phone in phone_numbers:
            writer.writerow([phone])

    print(f"[+] Создан CSV файл: {filename} ({len(phone_numbers)} номеров)")


def create_zip_archive(zip_filename: Path, csv_files: list):
    """
    Создает ZIP архив с CSV файлами

    Args:
        zip_filename: Имя ZIP файла
        csv_files: Список путей к CSV файлам
    """
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for csv_file in csv_files:
            if csv_file.exists():
                zipf.write(csv_file, csv_file.name)
                print(f"[+] Добавлен в архив: {csv_file.name}")

    print(f"[+] Создан ZIP архив: {zip_filename}")

    # Удаление временных CSV файлов
    for csv_file in csv_files:
        if csv_file.exists():
            csv_file.unlink()


def create_test_data_simple(output_dir: Path = Path(".")):
    """
    Создает простой тестовый архив с одним CSV файлом

    Args:
        output_dir: Директория для сохранения
    """
    print("\n" + "="*60)
    print("Создание простого тестового архива")
    print("="*60 + "\n")

    # Генерация 100 номеров
    phone_numbers = generate_phone_numbers(100, region_code="999")

    # Создание CSV
    csv_file = output_dir / "phonelist_test.csv"
    create_csv_file(csv_file, phone_numbers)

    # Создание ZIP
    zip_file = output_dir / "phonelist_test_simple.zip"
    create_zip_archive(zip_file, [csv_file])

    print(f"\n[+] Готово! Используйте файл: {zip_file}")


def create_test_data_multiple(output_dir: Path = Path(".")):
    """
    Создает архив с несколькими CSV файлами (разные регионы)

    Args:
        output_dir: Директория для сохранения
    """
    print("\n" + "="*60)
    print("Создание архива с несколькими CSV файлами")
    print("="*60 + "\n")

    regions = [
        ("495", "moscow", 200),      # Москва
        ("812", "spb", 150),          # Санкт-Петербург
        ("843", "kazan", 100),        # Казань
    ]

    csv_files = []

    for region_code, region_name, count in regions:
        phone_numbers = generate_phone_numbers(count, region_code=region_code)
        csv_file = output_dir / f"phonelist_{region_name}.csv"
        create_csv_file(csv_file, phone_numbers)
        csv_files.append(csv_file)

    # Создание ZIP
    zip_file = output_dir / "phonelist_test_multiple.zip"
    create_zip_archive(zip_file, csv_files)

    print(f"\n[+] Готово! Используйте файл: {zip_file}")
    print(f"[*] Всего номеров: {sum(c for _, _, c in regions)}")


def create_test_data_large(output_dir: Path = Path(".")):
    """
    Создает большой архив для нагрузочного тестирования

    Args:
        output_dir: Директория для сохранения
    """
    print("\n" + "="*60)
    print("Создание большого архива (нагрузочное тестирование)")
    print("="*60 + "\n")

    # Генерация 10000 номеров
    count = 10000
    phone_numbers = generate_phone_numbers(count, region_code="999")

    # Создание CSV
    csv_file = output_dir / "phonelist_large.csv"
    create_csv_file(csv_file, phone_numbers)

    # Создание ZIP
    zip_file = output_dir / "phonelist_test_large.zip"
    create_zip_archive(zip_file, [csv_file])

    file_size = zip_file.stat().st_size
    file_size_kb = file_size / 1024

    print(f"\n[+] Готово! Используйте файл: {zip_file}")
    print(f"[*] Размер файла: {file_size_kb:.2f} KB")
    print(f"[*] Количество номеров: {count}")


def create_test_data_custom():
    """
    Интерактивное создание пользовательского архива
    """
    print("\n" + "="*60)
    print("Создание пользовательского архива")
    print("="*60 + "\n")

    try:
        # Запрос параметров
        count = int(input("Количество номеров (например, 100): ").strip() or "100")
        region_code = input("Код региона (3 цифры, например 999): ").strip() or "999"
        output_name = input("Имя выходного ZIP файла (без .zip): ").strip() or "phonelist_custom"

        if len(region_code) != 3 or not region_code.isdigit():
            print("[!] Код региона должен состоять из 3 цифр")
            return

        print(f"\n[*] Параметры:")
        print(f"    Количество: {count}")
        print(f"    Регион: {region_code}")
        print(f"    Файл: {output_name}.zip")

        confirm = input("\nПродолжить? (y/n): ").strip().lower()
        if confirm != 'y':
            print("[*] Отменено")
            return

        # Генерация
        phone_numbers = generate_phone_numbers(count, region_code=region_code)

        # Создание CSV
        csv_file = Path(f"phonelist_{output_name}.csv")
        create_csv_file(csv_file, phone_numbers)

        # Создание ZIP
        zip_file = Path(f"{output_name}.zip")
        create_zip_archive(zip_file, [csv_file])

        print(f"\n[+] Готово! Используйте файл: {zip_file}")

    except ValueError as e:
        print(f"[!] Ошибка ввода: {e}")
    except KeyboardInterrupt:
        print("\n[*] Прервано пользователем")


def main():
    """Главное меню"""

    print("\n" + "="*60)
    print("Генератор тестовых данных для Cassandra Uploader")
    print("="*60)
    print("\nВыберите тип тестовых данных:")
    print("  1. Простой архив (100 номеров, 1 CSV)")
    print("  2. Множественный архив (450 номеров, 3 CSV - разные регионы)")
    print("  3. Большой архив (10000 номеров, нагрузочное тестирование)")
    print("  4. Пользовательский архив (свои параметры)")
    print("  0. Выход")
    print()

    try:
        choice = input("Ваш выбор: ").strip()

        output_dir = Path(".")

        if choice == '1':
            create_test_data_simple(output_dir)
        elif choice == '2':
            create_test_data_multiple(output_dir)
        elif choice == '3':
            create_test_data_large(output_dir)
        elif choice == '4':
            create_test_data_custom()
        elif choice == '0':
            print("Выход")
        else:
            print(f"[!] Неверный выбор: {choice}")

    except KeyboardInterrupt:
        print("\n[*] Прервано пользователем")
    except Exception as e:
        print(f"[!] Ошибка: {e}")


if __name__ == "__main__":
    main()
