// =====================================================
// ОБРАБОТКА ОТВЕТОВ ПОСЛЕ ДЕМО-МОНОЛОГА БОТА ЛИЗЫ
// Фраза бота: "Давай покажу. Вот сейчас скажи что-нибудь. А я попробую распознать"
// =====================================================
// ТОП-20 наиболее вероятных ответов пользователя (в порядке приоритета)

// -------- 1. БЕСПОКОЙСТВО О ПРИВАТНОСТИ / ТРЕБОВАНИЕ УДАЛИТЬ (высокий приоритет!) --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("удали")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("удали")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("информац")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не хочу")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("знал")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не безопасн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("нарушен")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("приватн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("нарушен")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("конфиденц")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это незаконн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("страшно")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("жутко")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("пугающ")} != null)) {
    outCallCard["STEP"] = "demo_privacy_concern";
    return outCallCard
}

// -------- 2. ОТКАЗ / НЕГАТИВ (высокий приоритет!) --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("не интересн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не нужн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не надо")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("хватит")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("достаточно")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("закончи")} != null)) {
    outCallCard["STEP"] = "demo_rejection";
    return outCallCard
}

// -------- 3. ВОПРОСЫ О ЗАКОННОСТИ / "ОТКУДА ТЫ ЭТО ЗНАЕШЬ" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("знае")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("узна")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("инфор")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это законн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это легальн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("имее")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("прав")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("по как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("прав")} != null)) {
    outCallCard["STEP"] = "demo_how_you_know";
    return outCallCard
}

// -------- 4. ВОПРОСЫ "ЧТО ТЫ ЗНАЕШЬ ОБО МНЕ" / "ПОКАЖИ МОИ ДАННЫЕ" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("знае")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("мне")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("информац")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("мне")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("знаешь")} != null)) {
    outCallCard["STEP"] = "demo_show_my_data";
    return outCallCard
}

// -------- 5. ВОПРОСЫ ПРО ПОКУПКИ В ПЯТЕРОЧКЕ / МАГАЗИНЫ --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("покупал")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("пятерочк")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("5")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("покупк")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мои покупк")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("покупа")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("магазин")} != null)) {
    outCallCard["STEP"] = "demo_purchases";
    return outCallCard
}

// -------- 6. ВОПРОСЫ ПРО МУЗЫКУ / "ПОЕБЕНЬ" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("музык")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("слуша")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("поебень")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("приложен")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("музык")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("приложен")} != null)) {
    outCallCard["STEP"] = "demo_music";
    return outCallCard
}

// -------- 7. ВОПРОСЫ ПРО БАЛАНС / СЧЕТ --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("баланс")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("счет")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("денег")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мой баланс")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("остаток")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("счет")} != null)) {
    outCallCard["STEP"] = "demo_balance";
    return outCallCard
}

// -------- 8. ВОПРОСЫ ПРО КРЕДИТ / ПЛАТЕЖ --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("когда")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("плат")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("кредит")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("плат")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("кредит")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мой кредит")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("платить")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("долг")} != null)) {
    outCallCard["STEP"] = "demo_credit";
    return outCallCard
}

// -------- 9. ВОПРОСЫ ПРО КЕШБЭК / КАРТУ --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("кешбек")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("карт")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("про кешбек")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("про карт")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("кешбек")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("карт")} != null)) {
    outCallCard["STEP"] = "demo_cashback";
    return outCallCard
}

// -------- 10. ВОПРОСЫ "ЧТО ТЫ УМЕЕШЬ" / ВОЗМОЖНОСТИ --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("умее")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("може")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("чем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("помо")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("функц")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("возможн")} != null)) {
    outCallCard["STEP"] = "demo_capabilities";
    return outCallCard
}

// -------- 11. ВОПРОСЫ "КАКИЕ У МЕНЯ ПРОДУКТЫ" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("продукт")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мои продукт")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("у меня")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("есть")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("карт")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("у меня")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("продукт")} != null)) {
    outCallCard["STEP"] = "demo_products";
    return outCallCard
}

// -------- 12. ЮМОР: ВОПРОСЫ ПРО НОЛАНА --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("нолан")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("гений")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("про нолан")} != null)) {
    outCallCard["STEP"] = "demo_nolan_joke";
    return outCallCard
}

// -------- 13. ЮМОР: ВОПРОСЫ ПРО ВЫШИВАНИЕ КРЕСТИКОМ --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("вышива")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("крестик")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("вышивк")} != null)) {
    outCallCard["STEP"] = "demo_crossstitch_joke";
    return outCallCard
}

// -------- 14. ПРОВЕРКА РАСПОЗНАВАНИЯ / ТЕСТ --------
if ((card.containsKey("VOICE") && card["VOICE"] == "тест") ||
    (card.containsKey("VOICE") && card["VOICE"] == "проверка") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты меня")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("слыш")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("понимае")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("меня")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("слышишь")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("меня")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("распознае")} != null)) {
    outCallCard["STEP"] = "demo_test";
    return outCallCard
}

// -------- 15. СКЕПТИЦИЗМ: "НЕ ВЕРЮ" / "СЕРЬЕЗНО?" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("не верю")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("неверю")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("серьезн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("правда")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это правд")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("врешь")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("врёшь")} != null)) {
    outCallCard["STEP"] = "demo_skepticism";
    return outCallCard
}

// -------- 16. ВОПРОС "ЗАЧЕМ ТЫ ЭТО ЗНАЕШЬ" / "ДЛЯ ЧЕГО" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("знае")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("для чего")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем тебе")} != null)) {
    outCallCard["STEP"] = "demo_why_you_need";
    return outCallCard
}

// -------- 17. ВПЕЧАТЛЕНИЕ: "КРУТО" / "ВАУ" / "ИНТЕРЕСНО" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("круто")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("крута")} != null) ||
    (card.containsKey("VOICE") && card["VOICE"] == "вау") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("интересн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("впечатля")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("классн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("прикольн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("здорово")} != null)) {
    outCallCard["STEP"] = "demo_impressed";
    return outCallCard
}

// -------- 18. СОГЛАСИЕ: "ДАВАЙ" / "ХОРОШО" / "ПОПРОБУЕМ" --------
if ((card.containsKey("VOICE") && card["VOICE"] == "давай") ||
    (card.containsKey("VOICE") && card["VOICE"] == "хорошо") ||
    (card.containsKey("VOICE") && card["VOICE"] == "ладно") ||
    (card.containsKey("VOICE") && card["VOICE"] == "окей") ||
    (card.containsKey("VOICE") && card["VOICE"] == "ок") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("попробу")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("поехали")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("погнали")} != null)) {
    outCallCard["STEP"] = "demo_agreement";
    return outCallCard
}

// -------- 19. ПОДТВЕРЖДЕНИЕ ЗНАКОМСТВА: "ДА, ЭТО Я" / "ВЕРНО" --------
if ((card.containsKey("VOICE") && card["VOICE"] == "да") ||
    (card.containsKey("VOICE") && card["VOICE"] == "я") ||
    (card.containsKey("VOICE") && card["VOICE"] == "это я") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("верн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("правильн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("точн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("конечн")} != null)) {
    outCallCard["STEP"] = "demo_confirmation";
    return outCallCard
}

// -------- 20. ПРИВЕТСТВИЕ В ОТВЕТ: "ЗДРАВСТВУЙ" / "ПРИВЕТ" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("привет")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("здравст")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("приветствую")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null && card.find{key, value -> key.startsWith("VOICE") && value.contains("день")} != null)) {
    outCallCard["STEP"] = "demo_greeting_back";
    return outCallCard
}

// -------- 21. НЕОПРЕДЕЛЕННЫЙ ОТВЕТ (по умолчанию) --------
if (1 == 1) {
    outCallCard["STEP"] = "demo_unknown";
    return outCallCard
}
