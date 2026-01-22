/**
 * Регулярные выражения для обработки ответов на приветствие голосового ассистента
 * Фраза: "Привет. Меня зовут Лиза - я голосовой помощник"
 *
 * Формат: проверка через card.find{key, value -> key.startsWith("VOICE") && value.contains("корень")}
 * Используются корни слов для покрытия всех словоформ
 */

// =====================================================
// 1. ПРИВЕТСТВИЯ
// =====================================================
// Распознает: привет, приветик, здравствуй, здравствуйте, добрый день, хай, алло и т.д.
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("привет")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("приветствую")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("здравст")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("здорово")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("здрасьте")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("здрасти")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("день")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("утро")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("вечер")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("день")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("утро")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("вечер")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("хай")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("хэй")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("хелло")} != null) ||
    (card.containsKey("VOICE") && card["VOICE"] == "йо") ||
    (card.containsKey("VOICE") && card["VOICE"] == "алло")) {
    outCallCard["STEP"] = "greeting";
    return outCallCard
}

// =====================================================
// 2. ВЕЖЛИВЫЕ ОТВЕТЫ / БЛАГОДАРНОСТЬ
// =====================================================
// Распознает: спасибо, благодарю, рад слышать, приятно познакомиться, отлично и т.д.
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("спасиб")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("благодар")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("признател")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("приятн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("рад")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("слышать")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("рада")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("слышать")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("рад")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("познаком")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("рада")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("познаком")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("рады")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("хорошо")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("отлично")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("отличн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("замечательно")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("прекрасно")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("супер")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("взаимн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мне тоже")} != null)) {
    outCallCard["STEP"] = "polite";
    return outCallCard
}

// =====================================================
// 3. СОГЛАСИЕ / ПОДТВЕРЖДЕНИЕ
// =====================================================
// Распознает: да, слушаю, понял, давай, ок, ясно и т.д.
if ((card.containsKey("VOICE") && card["VOICE"] == "да") ||
    (card.containsKey("VOICE") && card["VOICE"] == "ага") ||
    (card.containsKey("VOICE") && card["VOICE"] == "угу") ||
    (card.containsKey("VOICE") && card["VOICE"] == "ок") ||
    (card.containsKey("VOICE") && card["VOICE"] == "окей") ||
    (card.containsKey("VOICE") && card["VOICE"] == "ладно") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ну да")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("слуша")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("слышу")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("понял")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("поняла")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("поняли")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("понятн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ясно")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("давай")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("вперед")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("продолжай")} != null) ||
    (card.containsKey("VOICE") && card["VOICE"] == "го") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("погнали")} != null)) {
    outCallCard["STEP"] = "confirmation";
    return outCallCard
}

// =====================================================
// 4. ВОПРОСЫ О ВОЗМОЖНОСТЯХ / ПОМОЩИ
// =====================================================
// Распознает: что ты умеешь, чем можешь помочь, какие функции и т.д.
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("умее")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("може")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("делае")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("чем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("помо")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("в чем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("помо")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("предлага")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("будет")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("дальше")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("для чего")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("нужн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("функц")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("возможн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("услуг")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("опци")} != null)) {
    outCallCard["STEP"] = "capability_question";
    return outCallCard
}

// =====================================================
// 5. ВОПРОСЫ ПРО ДЕЛА / САМОЧУВСТВИЕ
// =====================================================
// Распознает: как дела, как ты, что нового, все хорошо и т.д.
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("дела")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как ты")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как вы")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как у тебя")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как у вас")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("настроен")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("поживае")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("нов")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("жизнь")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("все")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("хорош")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("всё")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("хорош")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("все")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("нормальн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("всё")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("нормальн")} != null)) {
    outCallCard["STEP"] = "small_talk";
    return outCallCard
}

// =====================================================
// 6. ВОПРОСЫ ИДЕНТИФИКАЦИИ
// =====================================================
// Распознает: кто ты, представься, как тебя зовут, кто говорит и т.д.
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("вы")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("говор")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("звон")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты кто")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("вы кто")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("представ")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("назов")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("себя")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("назов")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("имя")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("зовут")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как тебя")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как вас")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("твое имя")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ваше имя")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("звон")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("кто так")} != null)) {
    outCallCard["STEP"] = "identity_question";
    return outCallCard
}

// =====================================================
// 7. ВОПРОСЫ О ПРИЧИНЕ ЗВОНКА
// =====================================================
// Распознает: зачем звонишь, что нужно, по какому вопросу и т.д.
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("звон")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("почему")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("звон")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("по как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("причин")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("нужн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("чего")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("нужн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("надо")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("хоти")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("треб")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("по как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("вопрос")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("по как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("повод")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("по как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("делу")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("в чем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("дело")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("случил")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("происход")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("цель")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("смысл")} != null)) {
    outCallCard["STEP"] = "purpose_question";
    return outCallCard
}

// =====================================================
// 8. ОТКАЗЫ / НЕГАТИВНЫЕ РЕАКЦИИ
// =====================================================
// Распознает: не нужно, отстань, пока, не интересно и т.д.
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("отстань")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("отвали")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("уйди")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("отъебись")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("свали")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("отвян")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не нужн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не надо")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не хочу")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не интересн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не требуется")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("повесь")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("трубк")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("положи")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("трубк")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("брось")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("трубк")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("кинь")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("трубк")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("до свидан")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("всего добр")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("прощай")} != null) ||
    (card.containsKey("VOICE") && card["VOICE"] == "пока") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не звони")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не беспокой")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не трево")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не дёргай")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мне")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("не интересн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мне")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("не нужн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("убер")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("баз")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("удал")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("номер")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("удал")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("баз")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("исключ")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("баз")} != null)) {
    outCallCard["STEP"] = "rejection";
    return outCallCard
}

// =====================================================
// 9. ПЕРЕСПРОС / НЕПОНИМАНИЕ
// =====================================================
// Распознает: что, а, не расслышал, повтори, плохо слышно и т.д.
if ((card.containsKey("VOICE") && card["VOICE"] == "что") ||
    (card.containsKey("VOICE") && card["VOICE"] == "чего") ||
    (card.containsKey("VOICE") && card["VOICE"] == "а") ||
    (card.containsKey("VOICE") && card["VOICE"] == "ась") ||
    (card.containsKey("VOICE") && card["VOICE"] == "га") ||
    (card.containsKey("VOICE") && card["VOICE"] == "чё") ||
    (card.containsKey("VOICE") && card["VOICE"] == "чево") ||
    (card.containsKey("VOICE") && card["VOICE"] == "что?") ||
    (card.containsKey("VOICE") && card["VOICE"] == "а?") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не расслыша")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не слыш")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не понял")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("плох")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("слышн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("плох")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("понятн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("плох")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("слыш")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("повтор")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("еще раз")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ещё раз")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("можно еще")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("можно ещё")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что сказал")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("извин")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("прости")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("пардон")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("громче")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("тише")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("громкость")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("погромче")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("потише")} != null)) {
    outCallCard["STEP"] = "clarification";
    return outCallCard
}

// =====================================================
// 10. ОЖИДАНИЕ / ПРОСЬБА ПОДОЖДАТЬ
// =====================================================
// Распознает: секунду, минутку, сейчас, подожди и т.д.
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("секунд")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("минут")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("момент")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мгновени")} != null) ||
    (card.containsKey("VOICE") && card["VOICE"] == "сейчас") ||
    (card.containsKey("VOICE") && card["VOICE"] == "щас") ||
    (card.containsKey("VOICE") && card["VOICE"] == "счас") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("погод")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("подожд")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("од")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("секунд")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("од")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("минут")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("од")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("момент")} != null)) {
    outCallCard["STEP"] = "wait";
    return outCallCard
}

// =====================================================
// 11. ЗАНЯТ / НЕЛЬЗЯ ГОВОРИТЬ
// =====================================================
// Распознает: я занят, не могу говорить, перезвоните, я за рулем и т.д.
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("я")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("занят")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("сейчас")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("занят")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("занята")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("занято")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не могу")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("говор")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не могу")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("разговар")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не могу")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("общ")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("нельзя")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("говор")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("некогда")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("говор")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("перезвон")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("позже")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("перезвон")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("потом")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("позвон")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("позже")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("позвон")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("потом")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("звони")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("позже")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("звони")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("потом")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("я за рулем")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("я еду")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("я ед")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("я на работ")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("я на совещ")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("я на встреч")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("сейчас на работ")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("сейчас на совещ")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не врем")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("неудобн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не подходящ")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("момент")} != null)) {
    outCallCard["STEP"] = "busy";
    return outCallCard
}

// =====================================================
// 12. ВОПРОСЫ О БОТЕ / РОБОТЕ
// =====================================================
// Распознает: ты робот, ты бот, это автоответчик, живой человек и т.д.
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("робот")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("вы")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("робот")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("бот")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("вы")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("бот")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("машин")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("компьютер")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("автомат")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("автоответч")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("запись")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("автомат")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("робот")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("живой")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("человек")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("настоящ")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("человек")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("реальн")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("человек")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("с кем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("говор")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("с кем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("общ")} != null)) {
    outCallCard["STEP"] = "bot_question";
    return outCallCard
}

// =====================================================
// НЕОПРЕДЕЛЕННЫЙ ОТВЕТ (по умолчанию)
// =====================================================
if (1 == 1) {
    outCallCard["STEP"] = "unknown_response";
    return outCallCard
}
