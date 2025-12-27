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
    audio_file VARCHAR(255),         -- Путь к аудиофайлу
    status VARCHAR(20) DEFAULT 'draft',  -- draft, running, paused, completed
    total_numbers INTEGER DEFAULT 0,
    processed_numbers INTEGER DEFAULT 0,
    successful_calls INTEGER DEFAULT 0,
    failed_calls INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Таблица номеров для обзвона
CREATE TABLE IF NOT EXISTS campaign_numbers (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    phone_number VARCHAR(20) NOT NULL,
    operator VARCHAR(50),            -- Определенный оператор
    status VARCHAR(20) DEFAULT 'pending',  -- pending, calling, answered, busy, failed, no_answer
    sim_used INTEGER,                -- Какая SIM использовалась
    call_attempts INTEGER DEFAULT 0,
    last_attempt_time TIMESTAMP,
    answer_time TIMESTAMP,
    duration INTEGER,                -- Длительность в секундах
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_campaign_status (campaign_id, status),
    INDEX idx_phone (phone_number)
);

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
    error_message TEXT,
    INDEX idx_call_time (call_time),
    INDEX idx_campaign (campaign_id)
);

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
