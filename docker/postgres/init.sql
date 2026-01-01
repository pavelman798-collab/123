-- =================================================================
-- База данных для телефонных кампаний
-- =================================================================

-- Таблица операторов и диапазонов номеров
CREATE TABLE IF NOT EXISTS operator_ranges (
    id SERIAL PRIMARY KEY,
    operator VARCHAR(50) NOT NULL,  -- МТС, Билайн, Мегафон, Теле2
    prefix VARCHAR(10) NOT NULL,     -- Префикс номера (910, 920 и т.д.)
    region VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(operator, prefix)
);

-- Таблица SIM-карт
CREATE TABLE IF NOT EXISTS sim_cards (
    id SERIAL PRIMARY KEY,
    sim_number INTEGER NOT NULL,     -- Номер слота (1-4)
    operator VARCHAR(50) NOT NULL,   -- Оператор (МТС, Билайн и т.д.)
    phone_number VARCHAR(20),        -- Номер SIM-карты
    status VARCHAR(20) DEFAULT 'active',  -- active, blocked, disabled
    daily_call_limit INTEGER DEFAULT 80,
    hourly_call_limit INTEGER DEFAULT 15,
    calls_today INTEGER DEFAULT 0,
    calls_this_hour INTEGER DEFAULT 0,
    last_call_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sim_number)
);

-- Таблица кампаний
CREATE TABLE IF NOT EXISTS campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    campaign_type VARCHAR(20) DEFAULT 'call',  -- call, sms, call_and_sms
    audio_file VARCHAR(255),         -- Путь к аудиофайлу
    sms_on_no_answer TEXT,           -- Текст СМС при недозвоне
    sms_on_success TEXT,             -- Текст СМС при успешном дозвоне
    send_sms_on_no_answer BOOLEAN DEFAULT FALSE,  -- Отправлять ли СМС при недозвоне
    send_sms_on_success BOOLEAN DEFAULT FALSE,    -- Отправлять ли СМС при успешном дозвоне
    status VARCHAR(20) DEFAULT 'draft',  -- draft, running, paused, completed, scheduled
    scheduled_start_time TIMESTAMP,  -- Запланированное время старта (UTC)
    use_timezones BOOLEAN DEFAULT FALSE,  -- Использовать ли часовые пояса
    timezone_mode VARCHAR(20) DEFAULT 'none',  -- none, manual, auto
    total_numbers INTEGER DEFAULT 0,
    processed_numbers INTEGER DEFAULT 0,
    successful_calls INTEGER DEFAULT 0,
    failed_calls INTEGER DEFAULT 0,
    sms_sent INTEGER DEFAULT 0,      -- Количество отправленных СМС
    sms_failed INTEGER DEFAULT 0,    -- Количество неудачных СМС
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    cancelled_at TIMESTAMP           -- Время отмены запланированного запуска
);

-- Таблица номеров для обзвона
CREATE TABLE IF NOT EXISTS campaign_numbers (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    phone_number VARCHAR(20) NOT NULL,
    operator VARCHAR(50),            -- Определенный оператор
    timezone VARCHAR(50),            -- Часовой пояс контакта (Europe/Moscow, Asia/Yekaterinburg и т.д.)
    status VARCHAR(20) DEFAULT 'pending',  -- pending, calling, answered, busy, failed, no_answer
    sim_used INTEGER,                -- Какая SIM использовалась
    call_attempts INTEGER DEFAULT 0,
    last_attempt_time TIMESTAMP,
    answer_time TIMESTAMP,
    duration INTEGER,                -- Длительность в секундах
    sms_status VARCHAR(20),          -- pending, sent, failed (статус отправки СМС)
    sms_sent_at TIMESTAMP,           -- Время отправки СМС
    sms_text TEXT,                   -- Текст отправленной СМС
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для campaign_numbers
CREATE INDEX IF NOT EXISTS idx_campaign_status ON campaign_numbers(campaign_id, status);
CREATE INDEX IF NOT EXISTS idx_phone ON campaign_numbers(phone_number);

-- Таблица логов звонков
CREATE TABLE IF NOT EXISTS call_logs (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id),
    phone_number VARCHAR(20) NOT NULL,
    sim_number INTEGER,
    operator VARCHAR(50),
    status VARCHAR(50),              -- ANSWER, BUSY, NOANSWER, FAILED
    duration INTEGER,
    call_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT
);

-- Индексы для call_logs
CREATE INDEX IF NOT EXISTS idx_call_time ON call_logs(call_time);
CREATE INDEX IF NOT EXISTS idx_campaign ON call_logs(campaign_id);

-- Таблица SMS (для будущего функционала)
CREATE TABLE IF NOT EXISTS sms_log (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id),
    phone_number VARCHAR(20) NOT NULL,
    sim_number INTEGER,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- pending, sent, failed
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица шаблонов СМС
CREATE TABLE IF NOT EXISTS sms_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,      -- Название шаблона
    text TEXT NOT NULL,              -- Текст шаблона
    category VARCHAR(50),            -- Категория (no_answer, success, general)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица информации о префиксах (оператор + часовой пояс + регион)
CREATE TABLE IF NOT EXISTS phone_prefix_info (
    id SERIAL PRIMARY KEY,
    prefix VARCHAR(10) NOT NULL,     -- Префикс номера (910, 920 и т.д.)
    operator VARCHAR(50) NOT NULL,   -- Оператор (МТС, Билайн, Мегафон, Теле2)
    timezone VARCHAR(50),            -- Часовой пояс (Europe/Moscow, Asia/Yekaterinburg и т.д.)
    region VARCHAR(100),             -- Регион
    utc_offset INTEGER,              -- Смещение от UTC в часах
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(prefix)
);

-- =================================================================
-- Начальные данные: диапазоны операторов
-- =================================================================

INSERT INTO operator_ranges (operator, prefix) VALUES
-- МТС
('МТС', '910'), ('МТС', '911'), ('МТС', '912'), ('МТС', '913'), ('МТС', '914'),
('МТС', '915'), ('МТС', '916'), ('МТС', '917'), ('МТС', '918'), ('МТС', '919'),
('МТС', '980'), ('МТС', '981'), ('МТС', '982'), ('МТС', '983'), ('МТС', '984'),
('МТС', '985'), ('МТС', '986'), ('МТС', '987'), ('МТС', '988'), ('МТС', '989'),

-- Билайн
('Билайн', '903'), ('Билайн', '905'), ('Билайн', '906'), ('Билайн', '909'),
('Билайн', '951'), ('Билайн', '953'), ('Билайн', '960'), ('Билайн', '961'),
('Билайн', '962'), ('Билайн', '963'), ('Билайн', '964'), ('Билайн', '965'),
('Билайн', '966'), ('Билайн', '967'), ('Билайн', '968'),

-- Мегафон
('Мегафон', '920'), ('Мегафон', '921'), ('Мегафон', '922'), ('Мегафон', '923'),
('Мегафон', '924'), ('Мегафон', '925'), ('Мегафон', '926'), ('Мегафон', '927'),
('Мегафон', '928'), ('Мегафон', '929'), ('Мегафон', '930'), ('Мегафон', '931'),
('Мегафон', '932'), ('Мегафон', '933'), ('Мегафон', '934'), ('Мегафон', '936'),
('Мегафон', '937'), ('Мегафон', '938'), ('Мегафон', '939'),

-- Теле2
('Теле2', '900'), ('Теле2', '901'), ('Теле2', '902'), ('Теле2', '904'),
('Теле2', '908'), ('Теле2', '950'), ('Теле2', '951'), ('Теле2', '952'),
('Теле2', '953'), ('Теле2', '954'), ('Теле2', '955'), ('Теле2', '958'),
('Теле2', '977'), ('Теле2', '991'), ('Теле2', '992'), ('Теле2', '993'),
('Теле2', '994'), ('Теле2', '995')
ON CONFLICT DO NOTHING;

-- Начальная конфигурация SIM-карт (после покупки GoIP обнови)
INSERT INTO sim_cards (sim_number, operator, phone_number, status) VALUES
(1, 'МТС', NULL, 'disabled'),
(2, 'Билайн', NULL, 'disabled'),
(3, 'Мегафон', NULL, 'disabled'),
(4, 'Теле2', NULL, 'disabled')
ON CONFLICT DO NOTHING;

-- Справочник префиксов с часовыми поясами (для автоопределения)
--
-- ВАЖНО: Мобильные префиксы операторов работают по всей России!
-- Этот справочник использует статистический подход - большинство абонентов
-- находятся в центральной России (Europe/Moscow, UTC+3).
--
-- Для точного определения часового пояса используйте режим "manual" с указанием
-- timezone во втором столбце CSV файла.
--
-- Итого уникальных префиксов: 70 (МТС: 20, Билайн: 15, Мегафон: 19, Теле2: 16)
--
INSERT INTO phone_prefix_info (prefix, operator, timezone, region, utc_offset) VALUES
-- МТС (20 префиксов)
('910', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('911', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('912', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('913', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('914', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('915', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('916', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('917', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('918', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('919', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('980', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('981', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('982', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('983', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('984', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('985', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('986', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('987', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('988', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),
('989', 'МТС', 'Europe/Moscow', 'Москва и ЦФО', 3),

-- Билайн (15 префиксов, включая 951 и 953)
('903', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('905', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('906', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('909', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('951', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('953', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('960', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('961', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('962', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('963', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('964', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('965', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('966', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('967', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),
('968', 'Билайн', 'Europe/Moscow', 'Москва и ЦФО', 3),

-- Мегафон (19 префиксов)
('920', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('921', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('922', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('923', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('924', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('925', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('926', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('927', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('928', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('929', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('930', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('931', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('932', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('933', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('934', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('936', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('937', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('938', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),
('939', 'Мегафон', 'Europe/Moscow', 'Москва и ЦФО', 3),

-- Теле2 (16 префиксов, БЕЗ 951 и 953 из-за UNIQUE constraint)
('900', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('901', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('902', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('904', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('908', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('950', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('952', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('954', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('955', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('958', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('977', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('991', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('992', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('993', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('994', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3),
('995', 'Теле2', 'Europe/Moscow', 'Москва и ЦФО', 3)
ON CONFLICT DO NOTHING;

-- =================================================================
-- Функции и триггеры
-- =================================================================

-- Функция для определения оператора по номеру
CREATE OR REPLACE FUNCTION detect_operator(phone VARCHAR(20))
RETURNS VARCHAR(50) AS $$
DECLARE
    phone_prefix VARCHAR(10);
    operator_name VARCHAR(50);
BEGIN
    -- Извлекаем первые 3 цифры после +7
    phone_prefix := SUBSTRING(phone FROM 2 FOR 3);

    -- Ищем оператора
    SELECT operator INTO operator_name
    FROM operator_ranges
    WHERE prefix = phone_prefix
    LIMIT 1;

    RETURN COALESCE(operator_name, 'Неизвестно');
END;
$$ LANGUAGE plpgsql;

-- Триггер для автоопределения оператора при добавлении номера
CREATE OR REPLACE FUNCTION set_operator_on_insert()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.operator IS NULL THEN
        NEW.operator := detect_operator(NEW.phone_number);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER campaign_numbers_set_operator
BEFORE INSERT ON campaign_numbers
FOR EACH ROW
EXECUTE FUNCTION set_operator_on_insert();

COMMENT ON DATABASE phone_campaigns IS 'База данных для управления телефонными кампаниями через GoIP-4';
