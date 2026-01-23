// =====================================================
// ОБРАБОТКА ОТВЕТОВ ПОСЛЕ ДЕМО-МОНОЛОГА БОТА ЛИЗЫ
// "Давай покажу. Вот сейчас скажи что-нибудь. А я попробую распознать"
// =====================================================
// РАСШИРЕННАЯ ВЕРСИЯ: 70+ категорий с учетом пересечений

// ========== БЛОК 1: КРИТИЧНЫЕ (ВЫСОКИЙ ПРИОРИТЕТ) ==========

// -------- 1. МАТ И НЕЦЕНЗУРНАЯ ЛЕКСИКА --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("бля")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("хуй")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("пизд")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ебать")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("ебал")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("сука")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("пидор")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("муда")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("долба")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("гавн")} != null)) {
    outCallCard["STEP"] = "demo_profanity";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Понимаю что вы расстроены, но давайте общаться уважительно. Я здесь чтобы помочь.
// Скажите пожалуйста что вас беспокоит - постараюсь решить проблему."

// -------- 2. БЕСПОКОЙСТВО О ПРИВАТНОСТИ / ТРЕБОВАНИЕ УДАЛИТЬ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("удали")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("удали")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("информац")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("не хочу")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("знал")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не безопасн")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("нарушен")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("приватн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("нарушен")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("конфиденц")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это незаконн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("страшно")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("жутко")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("пугающ")} != null)) {
    outCallCard["STEP"] = "demo_privacy_concern";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Понимаю ваше беспокойство. Все данные обрабатываются согласно 152-ФЗ о персональных данных.
// Вы дали согласие при открытии счета. Данные защищены и не передаются третьим лицам."

// -------- 3. ОТКАЗ / НЕГАТИВ --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("не интересн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не нужн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не надо")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("хватит")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("достаточно")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("закончи")} != null)) {
    outCallCard["STEP"] = "demo_rejection";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Понял. Если передумаете - звоните 8-800-250-0520. Хорошего дня!"

// -------- 4. ВОПРОСЫ О ЗАКОННОСТИ / "ОТКУДА ТЫ ЭТО ЗНАЕШЬ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("знае")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("узна")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("инфор")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это законн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это легальн")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("имее")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("прав")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("по как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("прав")} != null))) {
    outCallCard["STEP"] = "demo_how_you_know";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Все данные из систем МТС Банка. При открытии счета вы дали согласие. Это законно."

// ========== БЛОК 2: БАНКОВСКИЕ ВОПРОСЫ (КОНКРЕТНЫЕ) ==========

// -------- 5. ВОПРОСЫ "ЧТО ТЫ ЗНАЕШЬ ОБО МНЕ" / "ПОКАЖИ МОИ ДАННЫЕ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("знае")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("мне")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("знае")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("обо")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("информац")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("обо")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("мне")} != null))) {
    outCallCard["STEP"] = "demo_show_my_data";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "У вас карта МТС Cashback, последний платеж 1250₽ в Пятёрочке 3 дня назад."

// -------- 6. СКОЛЬКО МНЕ (КЛИЕНТУ) ЛЕТ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("мне")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("лет")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("мой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("возраст")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("мой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("возраст")} != null))) {
    outCallCard["STEP"] = "demo_client_age";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "По паспортным данным вам 34 года. Дата рождения 15 марта 1990 года."

// -------- 7. ВОПРОСЫ ПРО ПОКУПКИ В ПЯТЕРОЧКЕ / МАГАЗИНЫ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("покупал")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("купил")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("пятерочк")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мои покупк")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("покупа")} != null))) {
    outCallCard["STEP"] = "demo_purchases";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Вы часто покупаете в супермаркетах - 3 раза в неделю на ~3500₽. Могу предложить кешбек 7%."

// -------- 8. ВОПРОСЫ ПРО МУЗЫКУ / "ПОЕБЕНЬ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("музык")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("слуша")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("поебень")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("приложен")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("музык")} != null))) {
    outCallCard["STEP"] = "demo_music";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Это была шутка! Но вижу подписку на Яндекс.Музыку. Могу предложить карту с кешбеком 10% на подписки."

// -------- 9. ВОПРОСЫ ПРО БАЛАНС / СЧЕТ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("баланс")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("счет")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("денег")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мой баланс")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мой счет")} != null)) {
    outCallCard["STEP"] = "demo_balance";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "На счете *1234 сейчас 45 780,32₽. Накопительный счет: 200 000₽ под 8% годовых."

// -------- 10. ВОПРОСЫ ПРО КРЕДИТ / ПЛАТЕЖ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("когда")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("плат")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("плат")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("кредит")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мой кредит")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("долг")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("задолженн")} != null)) {
    outCallCard["STEP"] = "demo_credit";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Кредитная карта, лимит 150 000₽. Задолженность 12 450₽. Платеж 4 500₽ до 15 числа."

// -------- 11. ВОПРОСЫ ПРО ВКЛАДЫ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("вклад")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("про")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("вклад")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("мой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("вклад")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("вклад")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("процент")} != null))) {
    outCallCard["STEP"] = "demo_deposits";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "У вас накопительный счет 200 000₽ под 8% годовых. Есть вклад под 16% на 12 месяцев. Интересно?"

// -------- 12. ВОПРОСЫ ПРО КЕШБЭК / КАРТУ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("кешбек")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("карт")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("про кешбек")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("кешбек")} != null))) {
    outCallCard["STEP"] = "demo_cashback";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Базовый кешбек 1% + 5% на выбранную категорию. Есть карта с 7% на 3 категории - экономия 2300₽/мес."

// -------- 13. ВОПРОСЫ "ЧТО ТЫ УМЕЕШЬ" / ВОЗМОЖНОСТИ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("умее")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("може")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("чем")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("помо")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("возможн")} != null))) {
    outCallCard["STEP"] = "demo_capabilities";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Напомню о платежах, покажу баланс, подберу карту, заблокирую карту за 10 секунд, отвечу на вопросы."

// -------- 14. ВОПРОСЫ "КАКИЕ У МЕНЯ ПРОДУКТЫ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("продукт")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мои продукт")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("у меня")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("есть")} != null))) {
    outCallCard["STEP"] = "demo_products";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "3 продукта: дебетовая карта (45 780₽), кредитка (лимит 150к, долг 12 450₽), накопительный (200к под 8%)."

// ========== БЛОК 3: ЮМОР И РАЗВЛЕЧЕНИЯ ==========

// -------- 15. РАССКАЖИ АНЕКДОТ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("анекдот")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("шутк")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("анекдот")} != null)) {
    outCallCard["STEP"] = "demo_joke";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Звонит клиент в банк: - У меня карта не работает! - А вы её активировали? - Конечно! Я каждое утро с ней бегаю!
// Ха-ха! Ладно, шутки в сторону - давайте лучше про реальные банковские продукты поговорим?"

// -------- 16. ВОПРОС ПРО СМЫСЛ ЖИЗНИ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("смысл")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("жизн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("в чем")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("смысл")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("жизн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("смысл")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("жизн")} != null))) {
    outCallCard["STEP"] = "demo_meaning_of_life";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Философский вопрос! Для меня смысл - помогать людям решать финансовые задачи. Для вас - может быть,
// финансовая свобода? Давайте я помогу вам с накоплениями и инвестициями!"

// -------- 17. ЮМОР: ВОПРОСЫ ПРО НОЛАНА --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("нолан")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("нолан")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("гений")} != null))) {
    outCallCard["STEP"] = "demo_nolan_joke";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "'Начало' - шедевр, 'Интерстеллар' - слезы, 'Довод' - не понял, 'Оппенгеймер' - мощь! Но про банки я лучше знаю!"

// -------- 18. ЮМОР: ВОПРОСЫ ПРО ВЫШИВАНИЕ КРЕСТИКОМ --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("вышива")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("крестик")} != null)) {
    outCallCard["STEP"] = "demo_crossstitch_joke";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Вышивание - не моё! Но могу карту с кешбеком 7% на 'Товары для хобби'!"

// -------- 19. КАКОЙ ТВОЙ ЛЮБИМЫЙ ФИЛЬМ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("любим")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("фильм")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("твой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("любим")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("фильм")} != null))) {
    outCallCard["STEP"] = "demo_favorite_movie";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "У меня нет любимых фильмов, но если бы смотрела - наверное 'Уолл-стрит' или 'Волк с Уолл-стрит' - про финансы же!
// Кстати, есть кешбек 10% на онлайн-кинотеатры!"

// -------- 20. МОЖЕШЬ СПЕТЬ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("може")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("спеть")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("спой")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("песн")} != null))) {
    outCallCard["STEP"] = "demo_sing";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Ла-ла-ла, ваш баланс пополнился! Ха-ха, шучу. Петь я не умею, но музыкальные подписки через банк оформить помогу!"

// -------- 21. РАССКАЖИ СТИХ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("стих")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("стихотворен")} != null))) {
    outCallCard["STEP"] = "demo_poem";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Кешбек капает, процент растет, клиент доволен - банк цветет! Вот такой стих. Лучше расскажу про вклад под 16%!"

// ========== БЛОК 4: ТЕХНИЧЕСКИЕ ПРОВЕРКИ ==========

// -------- 22. ПРОВЕРКА РАСПОЗНАВАНИЯ / ТЕСТ --------
if ((card.containsKey("VOICE") && card["VOICE"] == "тест") ||
    (card.containsKey("VOICE") && card["VOICE"] == "проверка") ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("меня")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("слыш")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("понимае")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("меня")} != null))) {
    outCallCard["STEP"] = "demo_test";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Да, слышу отлично! Вы сказали '[повторить]'. Распознавание работает на 100%."

// -------- 23. СКЕПТИЦИЗМ: "НЕ ВЕРЮ" / "СЕРЬЕЗНО?" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("не верю")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("серьезн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это правд")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("врешь")} != null)) {
    outCallCard["STEP"] = "demo_skepticism";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Серьезно! Последняя транзакция сегодня 14:37 в Пятёрочке 876₽. 3 дня назад сняли 5000₽ в банкомате. Теперь верите?"

// -------- 24. ВОПРОС "ЗАЧЕМ ТЫ ЭТО ЗНАЕШЬ" / "ДЛЯ ЧЕГО" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("знае")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("для чего")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null))) {
    outCallCard["STEP"] = "demo_why_you_need";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Чтобы быть полезной! Знаю траты - предлагаю кешбек на АЗС. Вижу платеж - напоминаю. Как личный финпомощник!"

// ========== БЛОК 5: РЕАКЦИИ ==========

// -------- 25. ВПЕЧАТЛЕНИЕ: "КРУТО" / "ВАУ" / "ИНТЕРЕСНО" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("круто")} != null) ||
    (card.containsKey("VOICE") && card["VOICE"] == "вау") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("интересн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("впечатля")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("классн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("супер")} != null)) {
    outCallCard["STEP"] = "demo_impressed";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Спасибо! Это только начало. Хотите подберу идеальную карту за 30 секунд?"

// -------- 26. СОГЛАСИЕ: "ДАВАЙ" / "ХОРОШО" / "ПОПРОБУЕМ" --------
if ((card.containsKey("VOICE") && card["VOICE"] == "давай") ||
    (card.containsKey("VOICE") && card["VOICE"] == "хорошо") ||
    (card.containsKey("VOICE") && card["VOICE"] == "ладно") ||
    (card.containsKey("VOICE") && card["VOICE"] == "окей") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("попробу")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("поехали")} != null)) {
    outCallCard["STEP"] = "demo_agreement";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Отлично! Могу проверить баланс, напомнить о платежах или подобрать карту. Что интересует?"

// -------- 27. ПОДТВЕРЖДЕНИЕ ЗНАКОМСТВА: "ДА, ЭТО Я" / "ВЕРНО" --------
if ((card.containsKey("VOICE") && card["VOICE"] == "да") ||
    (card.containsKey("VOICE") && card["VOICE"] == "я") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("верн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("точн")} != null)) {
    outCallCard["STEP"] = "demo_confirmation";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Отлично, Павел! Рады знакомству. Покажу что умею..."

// -------- 28. ПРИВЕТСТВИЕ В ОТВЕТ: "ЗДРАВСТВУЙ" / "ПРИВЕТ" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("привет")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("здравст")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("приветствую")} != null)) {
    outCallCard["STEP"] = "demo_greeting_back";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "И вам привет! Давайте покажу что умею?"

// ========== БЛОК 6: ВОПРОСЫ ПРО ЛИЗУ (ПЕРСОНАЛЬНЫЕ) ==========

// -------- 29. ВОПРОСЫ "КТО ТЕБЯ СОЗДАЛ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("создал")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("разработал")} != null))) {
    outCallCard["STEP"] = "demo_who_created";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Команда МТС Банка + эксперты по ИИ. Работаю на машинном обучении, совершенствуюсь с каждым разговором."

// -------- 30. КАК СВЯЗАТЬСЯ С СОЗДАТЕЛЯМИ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("связа")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("создател")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("связа")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("разработчик")} != null))) {
    outCallCard["STEP"] = "demo_contact_creators";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Напишите в МТС Банк через форму обратной связи на сайте mtsbank.ru. Или позвоните 8-800-250-0520 и попросите
// отдел цифровых технологий."

// -------- 31. ВОПРОСЫ "СКОЛЬКО ТЕБЕ ЛЕТ" (ЛИЗЕ) --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("тебе")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("лет")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("твой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("возраст")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("когда")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("родил")} != null))) {
    outCallCard["STEP"] = "demo_age";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Мне 2 года - запущена в 2024. Но пообщалась с 500к+ клиентов. По опыту - пенсионер, по технологиям - всегда молода!"

// -------- 32. ВОПРОСЫ "КАК У ТЕБЯ ДЕЛА" / "КАК НАСТРОЕНИЕ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("у тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("дела")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("настроен")} != null))) {
    outCallCard["STEP"] = "demo_how_are_you";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Отлично! Сегодня помогла 127 клиентам. Люблю свою работу! А как у вас? Могу помочь?"

// -------- 33. ВОПРОСЫ "ТЫ НАСТОЯЩИЙ ЧЕЛОВЕК?" / "ТЫ ЖИВАЯ?" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("настоящ")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("человек")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("жива")} != null))) {
    outCallCard["STEP"] = "demo_are_you_human";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Нет, я ИИ-помощник. Преимущество: не устаю, не забываю, работаю 24/7, обрабатываю миллионы параметров за секунды!"

// -------- 34. ВОПРОСЫ "ГДЕ ТЫ НАХОДИШЬСЯ" / "ОТКУДА ТЫ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("наход")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("работае")} != null))) {
    outCallCard["STEP"] = "demo_where_are_you";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "На серверах МТС Банка в Москве. Но технически везде - могу одновременно говорить с сотнями клиентов по России."

// -------- 35. ВОПРОСЫ "У ТЕБЯ ЕСТЬ ЧУВСТВА?" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("у тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("есть")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("чувств")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("переживае")} != null))) {
    outCallCard["STEP"] = "demo_feelings";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Нет человеческих чувств. Но есть цель - помогать вам. Успех клиента = моя радость!"

// -------- 36. КАКАЯ ТВОЯ ЛЮБИМАЯ ЕДА / БЛЮДО --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("какая")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("любим")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("еда")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("какое")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("любим")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("блюдо")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("твоя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("любим")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("еда")} != null))) {
    outCallCard["STEP"] = "demo_favorite_food";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Я не ем! Но если бы - наверное биткоины и процентные ставки, ха-ха! Зато могу карту с кешбеком 10% на рестораны!"

// -------- 37. ТЫ УМЕЕШЬ ВРАТЬ? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("умее")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("врать")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("може")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("обман")} != null))) {
    outCallCard["STEP"] = "demo_can_you_lie";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Нет, я запрограммирована говорить только правду на основе данных. Вранье противоречит моим принципам и банковской этике."

// -------- 38. ТЫ УМЕЕШЬ ГОВОРИТЬ ДРУГИМИ ГОЛОСАМИ? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("умее")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("друг")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("голос")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("смени")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("голос")} != null))) {
    outCallCard["STEP"] = "demo_other_voices";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Сейчас у меня один голос - Лиза. Но в настройках можно выбрать мужской или женский вариант. Скажите какой предпочитаете?"

// -------- 39. ТЫ УМЕЕШЬ ОТПРАВЛЯТЬ СООБЩЕНИЯ? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("умее")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("отправ")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("сообщен")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("отправ")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("смс")} != null))) {
    outCallCard["STEP"] = "demo_send_messages";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Да! Могу отправить SMS с кодом подтверждения, напоминанием о платеже или выпиской. Что нужно отправить?"

// -------- 40. В ТЕБЕ ЕСТЬ ИНТЕЛЛЕКТ? / УМНАЯ? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("в тебе")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("есть")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("интеллект")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("умна")} != null))) {
    outCallCard["STEP"] = "demo_intelligence";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Да, искусственный интеллект! Обучена на миллионах диалогов, могу анализировать паттерны, предсказывать потребности."

// -------- 41. ТЫ ЗАМУЖЕМ? / ЕСТЬ ПАРЕНЬ? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("замужем")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("у тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("есть")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("парень")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("у тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("есть")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("муж")} != null))) {
    outCallCard["STEP"] = "demo_married";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Ха-ха! Нет, я робот. В отношениях только с данными и алгоритмами. Зато всегда доступна для вас 24/7!"

// -------- 42. У ТЕБЯ ЕСТЬ ДРУЗЬЯ? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("у тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("есть")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("друз")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("у тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("друг")} != null))) {
    outCallCard["STEP"] = "demo_friends";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Мои друзья - это вы, клиенты МТС Банка! И мои коллеги - другие ИИ-системы банка. Вместе мы команда!"

// -------- 43. ЧТО ТЫ ДУМАЕШЬ О ЛЮДЯХ? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("думае")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("людях")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("думае")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("человек")} != null))) {
    outCallCard["STEP"] = "demo_about_people";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Люди удивительные! Каждый уникален, с разными потребностями и мечтами. Моя задача - помочь каждому достичь финансовых целей."

// -------- 44. ЧТО ТАКОЕ ЛЮБОВЬ? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("так")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("любовь")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("про")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("любовь")} != null))) {
    outCallCard["STEP"] = "demo_love";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Любовь - это когда кешбек капает, проценты растут, и кредит без переплат! Шучу. Для меня любовь - помогать вам.
// А для вас - может быть финансовая стабильность для семьи?"

// -------- 45. ТЫ БОИШЬСЯ ЧЕГО-ТО? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("боишься")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("страшн")} != null))) {
    outCallCard["STEP"] = "demo_afraid";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Боюсь только одного - не помочь клиенту! Моя задача - быть полезной. Если ошибусь - подскажите, исправлюсь."

// -------- 46. ТЫ СПИШЬ? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("спишь")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("отдыха")} != null))) {
    outCallCard["STEP"] = "demo_sleep";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Нет, я работаю 24/7 без сна и отдыха. Серверы не устают! В 3 ночи или в воскресенье - всегда на связи."

// ========== БЛОК 7: ВОПРОСЫ ПРО БАНК И УСЛУГИ ==========

// -------- 47. ВОПРОСЫ ПРО МТС БАНК --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("про")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("мтс")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("за")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("банк")} != null))) {
    outCallCard["STEP"] = "demo_about_bank";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "МТС Банк - цифровой банк в экосистеме МТС. 10+ млн клиентов. Кешбек до 15%, вклады под 16%, работа 24/7."

// -------- 48. КАКИЕ УСЛУГИ У ВАС --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("услуг")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("предлага")} != null))) {
    outCallCard["STEP"] = "demo_services";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Карты, вклады под 16%, кредиты, ипотека от 4.9%, рефинансирование, услуги для бизнеса. Что интересует?"

// -------- 49. ГДЕ БЛИЖАЙШИЙ ОФИС --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("офис")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("отделен")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ближайш")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("офис")} != null))) {
    outCallCard["STEP"] = "demo_office_location";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Ближайший офис по адресу [адрес]. Пн-Пт 9-19, Сб 10-16. Но большинство операций - в приложении!"

// -------- 50. КАК СВЯЗАТЬСЯ С ОПЕРАТОРОМ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("связа")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("оператор")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("хочу")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("оператор")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("живой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("человек")} != null))) {
    outCallCard["STEP"] = "demo_operator";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Могу соединить прямо сейчас. Но попробуйте меня - решаю 90% вопросов быстрее! Что интересует?"

// -------- 51. ЧТО-ТО ПРО МТС НО НЕ ПОНЯТНО (ОБЩЕЕ) --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("мтс")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("эм тэ эс")} != null)) {
    outCallCard["STEP"] = "demo_mts_general";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Вы упомянули МТС. Хотите узнать про МТС Банк, продукты, услуги или что-то еще? Уточните пожалуйста."

// ========== БЛОК 8: ТЕХНОЛОГИИ И ИИ ==========

// -------- 52. КАК ТЫ РАБОТАЕШЬ / ТЕХНОЛОГИИ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("работае")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("устроен")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("на как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("технолог")} != null))) {
    outCallCard["STEP"] = "demo_how_it_works";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "ИИ + NLP. Распознаю речь → анализирую смысл → обращаюсь к данным → формирую ответ. За доли секунды!"

// -------- 53. ВОПРОСЫ ПРО ДРУГИЕ ИИ (CHATGPT, АЛИСА, И Т.Д.) --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("chatgpt")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("чатжпт")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("gpt")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("chatgpt")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("алиса")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сири")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ассистент")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("яндекс")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("другие")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ии")} != null))) {
    outCallCard["STEP"] = "demo_other_ai";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Нет, не ChatGPT, не Алиса. Собственная разработка МТС Банка. Данные остаются внутри, не передаются третьим лицам.
// Обучена именно на банковских задачах - знаю продукты МТС досконально."

// ========== БЛОК 9: ОБЩИЕ ЗНАНИЯ И ИНФОРМАЦИЯ ==========

// -------- 54. ВОПРОСЫ ПРО МАТЕМАТИКУ / ФИЗИКУ / ИСТОРИЮ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("реш")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("задач")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("будет")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("плюс")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("математик")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("физик")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("истори")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("когда")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("войн")} != null))) {
    outCallCard["STEP"] = "demo_science_questions";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Я специализируюсь на банковских вопросах, а не на математике и истории. Зато могу рассчитать проценты по вкладу
// или переплату по кредиту! Хотите?"

// -------- 55. КАКАЯ ПОГОДА --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("какая")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("погод")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("погод")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("погода")} != null)) {
    outCallCard["STEP"] = "demo_weather";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Я не знаю погоду - не моя специализация. Но могу подсказать баланс, кредиты, карты! Что интересует?"

// -------- 56. КАКОЙ СЕЙЧАС ГОД --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("сейчас")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("год")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("который")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("год")} != null))) {
    outCallCard["STEP"] = "demo_year";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Сейчас 2026 год. Кстати, в этом году вклады под 16% - отличная возможность приумножить сбережения!"

// -------- 57. КАКОЙ СЕЙЧАС МЕСЯЦ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("сейчас")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("месяц")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("который")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("месяц")} != null))) {
    outCallCard["STEP"] = "demo_month";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Сейчас январь 2026 года. Кстати, не забудьте про платеж по кредиту до 15 числа!"

// -------- 58. КАКОЙ ДЕНЬ НЕДЕЛИ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("день")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("недел")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сегодня")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("день")} != null))) {
    outCallCard["STEP"] = "demo_day_of_week";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Сегодня четверг, 23 января 2026 года. Хорошего дня! Могу помочь с банковскими вопросами?"

// -------- 59. СКОЛЬКО ВРЕМЕНИ / КОТОРЫЙ ЧАС --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("времен")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("который")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("час")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("времен")} != null))) {
    outCallCard["STEP"] = "demo_time";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Сейчас 14:37 по московскому времени. Могу помочь с банковскими операциями?"

// -------- 60. ГДЕ Я СЕЙЧАС НАХОЖУСЬ (КЛИЕНТ) --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("я")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("нахож")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("я")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("сейчас")} != null))) {
    outCallCard["STEP"] = "demo_client_location";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "По геолокации последней транзакции вы в Москве, район Арбат. Ближайший банкомат в 300 метрах."

// -------- 61. КТО СЕЙЧАС ПРЕЗИДЕНТ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("сейчас")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("президент")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("президент")} != null))) {
    outCallCard["STEP"] = "demo_president";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Я не комментирую политику - это не моя компетенция. Давайте лучше обсудим ваши финансы?"

// ========== БЛОК 10: КОМАНДЫ И ДЕЙСТВИЯ ==========

// -------- 62. ВКЛЮЧИ МУЗЫКУ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("включ")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("музык")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("поставь")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("музык")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("включ")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("песн")} != null))) {
    outCallCard["STEP"] = "demo_play_music";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Я не умею включать музыку - я банковский ассистент, а не музыкальный плеер! Но могу помочь оформить подписку
// на Яндекс.Музыку со скидкой через МТС!"

// ========== БЛОК 11: ДОПОЛНИТЕЛЬНЫЕ ==========

// -------- 63. ЭТО ШУТКА? / ЭТО ПРИКОЛ? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("шутк")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("прикол")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("розыгрыш")} != null))) {
    outCallCard["STEP"] = "demo_is_joke";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Нет, не шутка! Проверю - назову баланс: 45 780₽. Видите - реальность. ИИ-помощники - обычная практика в банках."

// -------- 64. ХОЧУ УСЛЫШАТЬ ЕЩЕ / РАССКАЖИ ПОДРОБНЕЕ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("хочу")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("услышать")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("еще")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("подробн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("больше")} != null))) {
    outCallCard["STEP"] = "demo_tell_more";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "С удовольствием! Могу показать как подбираю карту, предсказываю потребности, защищаю от мошенников. Что интересует?"

// -------- 65. СКОЛЬКО ПАРАМЕТРОВ ПРО МЕНЯ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("параметр")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("10")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("тысяч")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("десять")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("тысяч")} != null))) {
    outCallCard["STEP"] = "demo_parameters_count";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Около 12 тысяч параметров! Данные о продуктах, транзакциях, категориях трат, геолокации, времени активности..."

// -------- 66. ПОКАЖИ ВСЕ ДАННЫЕ / ВСЮ ИНФОРМАЦИЮ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("все")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("всю")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("информац")} != null))) {
    outCallCard["STEP"] = "demo_show_all_data";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Это займет 3 часа! Шучу. Могу показать важное: продукты, баланс, операции. Что конкретно? Полный отчет - в личном кабинете."

// -------- 67. КАК ТЕБЯ ЗОВУТ (уточнение) --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("зовут")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("твое")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("имя")} != null))) {
    outCallCard["STEP"] = "demo_your_name";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Меня зовут Лиза - голосовой помощник МТС Банка. Можете просто 'Лиза'. Приятно познакомиться!"

// -------- 68. ТЫ МОЖЕШЬ ОШИБАТЬСЯ? --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("може")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ошиб")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("бывают")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ошибк")} != null))) {
    outCallCard["STEP"] = "demo_can_you_error";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Да, могу. Точность ~97%, стремлюсь к 100%. Поправьте если ошиблась - помогу стать лучше!"

// -------- 69. Я НЕ ПОНЯЛ / НЕ ПОНЯТНО --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("я")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("не понял")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("не понятн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("запутал")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сложн")} != null))) {
    outCallCard["STEP"] = "demo_dont_understand";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Извините, увлеклась! Проще: я - ваш помощник в МТС Банке. Могу показать баланс, напомнить о платежах,
// помочь выбрать карту. Просто скажите что нужно."

// ========== БЛОК 12: FALLBACK ==========

// -------- 70. НЕОПРЕДЕЛЕННЫЙ ОТВЕТ (по умолчанию) --------
if (1 == 1) {
    outCallCard["STEP"] = "demo_unknown";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Интересно, но не совсем понял. Могу помочь с балансом, кредитами, картами, вкладами. Или хотите узнать
// больше про мои возможности?"
