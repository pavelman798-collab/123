/**
 * ПРИМЕР ИНТЕГРАЦИИ: Обработка ответов на приветствие голосового ассистента
 *
 * Этот файл показывает, как интегрировать паттерны распознавания приветствий
 * в существующий скрипт checkConditions
 */

import groovy.time.TimeCategory
import java.text.SimpleDateFormat
import java.time.ZoneId
import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter

def inParams = [:] as HashMap

// =====================================================
// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (существующие)
// =====================================================

def getDateTime(format, datetime) {
    try {
        return new Date().parse(format, datetime)
    } catch (Exception e) {
        e.printStackTrace()
    }
    return null
}

def getTime(format, datetime) {
    try {
        def time = new SimpleDateFormat("HH:mm:ss").format(new Date().parse(format, datetime))
        def date = new SimpleDateFormat("dd/MM/yy").format(new Date())
        def d = new Date().parse("dd/MM/yy HH:mm:ss", "$date $time")
        return d
    } catch (Exception e) {
        e.printStackTrace()
    }
    return null
}

def getCurrDateTime() {
    try {
        return new Date()
    } catch (Exception e) {
        e.printStackTrace()
    }
    return null
}

def checkDateWithNow(dateStr, operator) {
    try {
        ZonedDateTime now = ZonedDateTime.now(ZoneId.of("UTC"))
        ZonedDateTime str_date = ZonedDateTime.parse(dateStr, DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ssXXX"))
        str_date = ZonedDateTime.ofInstant(str_date.toInstant(), ZoneId.of("UTC"))
        switch (operator) {
            case "before":
                return str_date.isBefore(now).toString()
            case "after":
                return str_date.isAfter(now).toString()
            case "equal":
                return str_date.isEqual(now).toString()
            default:
                return "Invalid Operator"
        }
    } catch(Exception ex) {
        return "Invalid Date Format"
    }
}

// =====================================================
// ОСНОВНАЯ ФУНКЦИЯ С ИНТЕГРИРОВАННЫМИ ПАТТЕРНАМИ
// =====================================================

def checkConditions(card) {
    def outCallCard = card
    use (TimeCategory) {
        try {

            // ================================================================
            // БЛОК 1: КРИТИЧЕСКИЕ СЛУЧАИ (ВСЕГДА ПЕРВЫМИ!)
            // ================================================================

            // Пропуск на следующий шаг (если нужно)
            if (card.containsKey("skip_greeting_check") && card["skip_greeting_check"] == "true") {
                outCallCard["STEP"] = "ba410ced-6a73-4ce6-b852-03083c04fe45"
                return outCallCard
            }

            // Мат и ругательства
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("бля")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("заебал")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("хуй")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("пидор")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("муда")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("долба")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("сука")} != null)) {
                outCallCard["STEP"] = "ce11c549-9ddb-466c-9712-375e636017d5"
                return outCallCard
            }

            // Смерть/похороны
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("умер")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("погиб")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("мертв")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("похорон")} != null)) {
                outCallCard["STEP"] = "340ed047-0524-4ba1-ae28-96ef213cef87"
                return outCallCard
            }

            // Тюрьма/мобилизация/СВО
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("тюрьм")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("мобил")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("сво")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("войн")} != null)) {
                outCallCard["STEP"] = "7fcc08f9-cce7-4559-9970-ee440604e04b"
                return outCallCard
            }

            // ================================================================
            // БЛОК 2: ОТВЕТЫ НА ПРИВЕТСТВИЕ "Привет. Меня зовут Лиза - я голосовой помощник"
            // ================================================================

            // -------- 2.1. ОТКАЗЫ (высокий приоритет!) --------
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("отстань")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("отвали")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("уйди")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не нужн")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не надо")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не хочу")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не интересн")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("до свидан")} != null) ||
                (card.containsKey("VOICE") && card["VOICE"] == "пока") ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не звони")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("удал")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("номер")} != null)) {
                outCallCard["STEP"] = "greeting_rejection"
                outCallCard["rejection_type"] = "explicit"
                return outCallCard
            }

            // -------- 2.2. ЗАНЯТ / НЕ МОЖЕТ ГОВОРИТЬ --------
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("я")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("занят")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("сейчас")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("занят")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("занята")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не могу")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("говор")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("перезвон")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("позже")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("я за рулем")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("я на работ")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("неудобн")} != null)) {
                outCallCard["STEP"] = "greeting_busy"
                return outCallCard
            }

            // -------- 2.3. ПЕРЕСПРОС / НЕПОНИМАНИЕ --------
            if ((card.containsKey("VOICE") && card["VOICE"] == "что") ||
                (card.containsKey("VOICE") && card["VOICE"] == "а") ||
                (card.containsKey("VOICE") && card["VOICE"] == "чего") ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не расслыша")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не слыш")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("плох")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("слышн")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("повтор")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("еще раз")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("ещё раз")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("громче")} != null)) {
                outCallCard["STEP"] = "greeting_repeat"
                // Увеличиваем счетчик переспросов
                outCallCard["repeat_count"] = (card.containsKey("repeat_count") ? card["repeat_count"].toInteger() + 1 : 1).toString()
                return outCallCard
            }

            // -------- 2.4. ПРИВЕТСТВИЯ (позитивный ответ) --------
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("привет")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("приветствую")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("здравст")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("здорово")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("день")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("утро")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("вечер")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("хай")} != null) ||
                (card.containsKey("VOICE") && card["VOICE"] == "алло")) {
                outCallCard["STEP"] = "greeting_positive"
                outCallCard["greeting_type"] = "reciprocal"
                return outCallCard
            }

            // -------- 2.5. ВЕЖЛИВЫЕ ОТВЕТЫ --------
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("спасиб")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("благодар")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("приятн")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("рад")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("слышать")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("рада")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("отлично")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("замечательно")} != null)) {
                outCallCard["STEP"] = "greeting_polite"
                return outCallCard
            }

            // -------- 2.6. ПОДТВЕРЖДЕНИЕ / СОГЛАСИЕ --------
            if ((card.containsKey("VOICE") && card["VOICE"] == "да") ||
                (card.containsKey("VOICE") && card["VOICE"] == "ага") ||
                (card.containsKey("VOICE") && card["VOICE"] == "угу") ||
                (card.containsKey("VOICE") && card["VOICE"] == "ок") ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("слуша")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("слышу")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("понял")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("поняла")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("давай")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("вперед")} != null)) {
                outCallCard["STEP"] = "greeting_confirmation"
                return outCallCard
            }

            // -------- 2.7. ВОПРОСЫ О ВОЗМОЖНОСТЯХ --------
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("умее")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("може")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("чем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("помо")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("предлага")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("функц")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("возможн")} != null)) {
                outCallCard["STEP"] = "greeting_capabilities"
                return outCallCard
            }

            // -------- 2.8. СВЕТСКАЯ БЕСЕДА (как дела, что нового) --------
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("дела")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("как ты")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("нов")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("все")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("хорош")} != null)) {
                outCallCard["STEP"] = "greeting_smalltalk"
                return outCallCard
            }

            // -------- 2.9. ВОПРОСЫ ИДЕНТИФИКАЦИИ --------
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("говор")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("звон")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("представ")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("зовут")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("звон")} != null)) {
                outCallCard["STEP"] = "greeting_identity"
                return outCallCard
            }

            // -------- 2.10. ВОПРОСЫ О ЦЕЛИ ЗВОНКА --------
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("звон")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("нужн")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("по как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("вопрос")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("в чем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("дело")} != null)) {
                outCallCard["STEP"] = "greeting_purpose"
                return outCallCard
            }

            // -------- 2.11. ПРОСЬБА ПОДОЖДАТЬ --------
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("секунд")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("минут")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("момент")} != null) ||
                (card.containsKey("VOICE") && card["VOICE"] == "сейчас") ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("подожд")} != null)) {
                outCallCard["STEP"] = "greeting_wait"
                return outCallCard
            }

            // -------- 2.12. ВОПРОСЫ О РОБОТЕ --------
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("робот")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("бот")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("автоответч")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("живой")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("человек")} != null)) {
                outCallCard["STEP"] = "greeting_bot_question"
                return outCallCard
            }

            // ================================================================
            // БЛОК 3: СУЩЕСТВУЮЩИЕ ПРОВЕРКИ (ваш старый код)
            // ================================================================

            // Проверка "допустим" / "говорите" / "возможно"
            if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("допустим")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("говори")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("что вас интерес")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("возмож")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("банк")} != null)) &&
                (card.containsKey("dopustim") && card["dopustim"] < "1") &&
                (card.containsKey("I_IVR") && card["I_IVR"] == "0")) {
                outCallCard["STEP"] = "af7da7dc-a050-4b87-a1ae-41e524427fcd"
                return outCallCard
            }

            // Вопросы "кто"/"что" при первом IVR
            if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("робот")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("как зовут")} != null)) &&
                (card.containsKey("I_IVR") && card["I_IVR"] < "1") &&
                (card.containsKey("dopustim") && card["dopustim"] == "0")) {
                outCallCard["STEP"] = "bdef4ae1-291a-45b3-89a2-b92a14f88492"
                return outCallCard
            }

            // Непонятный ответ (счетчик)
            if (card.containsKey("neponytno") && card["neponytno"] < "2" &&
                card.containsKey("dopustim") && card["dopustim"] == "0" &&
                card.containsKey("I_IVR") && card["I_IVR"] == "0") {
                outCallCard["STEP"] = "9f28521f-5273-417b-9378-e15965916cd5"
                return outCallCard
            }

            // Подтверждение ответа "да" (старая логика)
            if (((card.containsKey("VOICE") && card["VOICE"] == "я") ||
                 (card.find{key, value -> key.startsWith("VOICE") && value.contains("да")} != null) ||
                 (card.find{key, value -> key.startsWith("VOICE") && value.contains("верно")} != null) ||
                 (card.find{key, value -> key.startsWith("VOICE") && value.contains("именно")} != null) ||
                 (card.find{key, value -> key.startsWith("VOICE") && value.contains("ну да")} != null) ||
                 (card.find{key, value -> key.startsWith("VOICE") && value.contains("ага")} != null) ||
                 (card.find{key, value -> key.startsWith("VOICE") && value.contains("угу")} != null) ||
                 (card.find{key, value -> key.startsWith("VOICE") && value.contains("конечно")} != null) ||
                 (card.find{key, value -> key.startsWith("VOICE") && value.contains("естественно")} != null) ||
                 (card.find{key, value -> key.startsWith("VOICE") && value.contains("точно")} != null)) &&
                ((card.find{key, value -> key.startsWith("VOICE") && !value.contains(" не ")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains(" нет ")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("нет ")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains(" нет")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("не ")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("нехочу")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("неверно")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("неправильно")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("тюрьм")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("мобилиз")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("войн")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("сво")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("операц")} != null) &&
                 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("неточно")} != null))) {
                outCallCard["STEP"] = "f0651306-a656-4c0d-b1a4-e15af706c5d3"
                return outCallCard
            }

            // Ошибка или не знаю
            if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ошиб")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не знаю")} != null) ||
                ((card.find{key, value -> key.startsWith("VOICE") && value.contains("друг")} != null) &&
                 ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ном")} != null) ||
                  (card.find{key, value -> key.startsWith("VOICE") && value.contains("телеф")} != null)))) {
                outCallCard["STEP"] = "ccf34905-5002-4db7-b0c4-db0b29a72fb7"
                return outCallCard
            }

            // Отрицание "нет"
            if ((card.containsKey("VOICE") && card["VOICE"] == "нет") ||
                (card.containsKey("VOICE") && card["VOICE"] == "не я") ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains(" не ")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не ")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("не подтвержд")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("неточно")} != null) ||
                (card.find{key, value -> key.startsWith("VOICE") && value.contains("неверно")} != null)) {
                outCallCard["STEP"] = "192b48ad-b252-4ede-a52d-83ff8217ef3c"
                return outCallCard
            }

            // ================================================================
            // FALLBACK (по умолчанию)
            // ================================================================

            if (1 == 1) {
                outCallCard["STEP"] = "aebc4ea3-bc64-4567-994c-ac689456642e"
                return outCallCard
            }

        } catch (Exception e) {
            e.getStackTrace()
        }
    }
    outCallCard["GROOVY_UUID"] = UUID.randomUUID()
    return outCallCard
}

// =====================================================
// ЗАПУСК
// =====================================================

outParams = checkConditions(inParams)
return outParams
