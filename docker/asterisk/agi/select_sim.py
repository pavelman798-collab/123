#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AGI скрипт для умного выбора SIM-карты
Определяет оператора абонента и выбирает SIM того же оператора
"""

import sys
import psycopg2
import random
from datetime import datetime, timedelta

# Конфигурация БД
DB_CONFIG = {
    'host': 'postgres',
    'database': 'phone_campaigns',
    'user': 'phone_user',
    'password': 'phone_pass_2024'
}

class AGI:
    """Простой AGI интерфейс"""
    def __init__(self):
        self.env = {}
        self._read_environment()

    def _read_environment(self):
        """Читаем переменные окружения AGI"""
        while True:
            line = sys.stdin.readline().strip()
            if not line:
                break
            key, value = line.split(':', 1)
            self.env[key.strip()] = value.strip()

    def set_variable(self, name, value):
        """Устанавливаем переменную в Asterisk"""
        sys.stdout.write(f'SET VARIABLE {name} "{value}"\n')
        sys.stdout.flush()
        sys.stdin.readline()

    def verbose(self, message, level=1):
        """Логирование"""
        sys.stdout.write(f'VERBOSE "{message}" {level}\n')
        sys.stdout.flush()
        sys.stdin.readline()


def detect_operator(phone_number):
    """
    Определяет оператора по номеру телефона
    Возвращает: (operator_name, sim_number) или (None, None)
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Извлекаем префикс (первые 3 цифры после 7)
        prefix = phone_number[1:4] if phone_number.startswith('7') else phone_number[:3]

        # Ищем оператора
        cur.execute("""
            SELECT operator FROM operator_ranges
            WHERE prefix = %s LIMIT 1
        """, (prefix,))

        result = cur.fetchone()
        operator = result[0] if result else None

        if not operator:
            cur.close()
            conn.close()
            return None, None

        # Ищем доступную SIM этого оператора
        cur.execute("""
            SELECT sim_number, calls_today, calls_this_hour, last_call_time
            FROM sim_cards
            WHERE operator = %s AND status = 'active'
            ORDER BY calls_today ASC, calls_this_hour ASC, RANDOM()
            LIMIT 1
        """, (operator,))

        sim_data = cur.fetchone()

        if not sim_data:
            # Нет активных SIM этого оператора - берем любую доступную
            cur.execute("""
                SELECT sim_number, operator, calls_today, calls_this_hour
                FROM sim_cards
                WHERE status = 'active'
                ORDER BY calls_today ASC, calls_this_hour ASC, RANDOM()
                LIMIT 1
            """)
            fallback = cur.fetchone()
            if fallback:
                sim_number, operator = fallback[0], fallback[1]
            else:
                cur.close()
                conn.close()
                return None, None
        else:
            sim_number = sim_data[0]
            calls_today = sim_data[1]
            calls_this_hour = sim_data[2]
            last_call = sim_data[3]

            # Проверка лимитов
            cur.execute("""
                SELECT daily_call_limit, hourly_call_limit
                FROM sim_cards WHERE sim_number = %s
            """, (sim_number,))

            limits = cur.fetchone()
            daily_limit, hourly_limit = limits

            # Проверяем превышение лимитов
            if calls_today >= daily_limit or calls_this_hour >= hourly_limit:
                # Превышен лимит - берем другую SIM
                cur.execute("""
                    SELECT sim_number, operator
                    FROM sim_cards
                    WHERE status = 'active'
                        AND calls_today < daily_call_limit
                        AND calls_this_hour < hourly_call_limit
                    ORDER BY calls_today ASC, RANDOM()
                    LIMIT 1
                """)
                fallback = cur.fetchone()
                if fallback:
                    sim_number, operator = fallback[0], fallback[1]
                else:
                    cur.close()
                    conn.close()
                    return None, None

        # Обновляем счетчики
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)

        cur.execute("""
            UPDATE sim_cards
            SET calls_today = calls_today + 1,
                calls_this_hour = CASE
                    WHEN last_call_time > %s THEN calls_this_hour + 1
                    ELSE 1
                END,
                last_call_time = %s
            WHERE sim_number = %s
        """, (hour_ago, now, sim_number))

        conn.commit()
        cur.close()
        conn.close()

        return operator, sim_number

    except Exception as e:
        sys.stderr.write(f"ERROR in detect_operator: {e}\n")
        return None, None


def main():
    """Главная функция AGI скрипта"""
    agi = AGI()

    # Получаем номер телефона из аргументов
    phone_number = sys.argv[1] if len(sys.argv) > 1 else None

    if not phone_number:
        agi.verbose("ERROR: Номер телефона не указан")
        agi.set_variable("SIM_ID", "")
        agi.set_variable("OPERATOR", "")
        sys.exit(1)

    agi.verbose(f"Определяем оператора для номера: {phone_number}")

    # Определяем оператора и выбираем SIM
    operator, sim_id = detect_operator(phone_number)

    if sim_id:
        agi.verbose(f"Выбрана SIM#{sim_id} ({operator})")
        agi.set_variable("SIM_ID", str(sim_id))
        agi.set_variable("OPERATOR", operator or "Unknown")
    else:
        agi.verbose("Нет доступных SIM-карт")
        agi.set_variable("SIM_ID", "")
        agi.set_variable("OPERATOR", "")

    sys.exit(0)


if __name__ == "__main__":
    main()
