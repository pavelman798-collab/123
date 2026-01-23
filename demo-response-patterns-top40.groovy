// =====================================================
// ОБРАБОТКА ОТВЕТОВ ПОСЛЕ ДЕМО-МОНОЛОГА БОТА ЛИЗЫ
// "Давай покажу. Вот сейчас скажи что-нибудь. А я попробую распознать"
// =====================================================
// ТОП-40 наиболее вероятных ответов с рекомендациями

// -------- 1. БЕСПОКОЙСТВО О ПРИВАТНОСТИ / ТРЕБОВАНИЕ УДАЛИТЬ --------
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
// РЕКОМЕНДАЦИЯ: "Понимаю ваше беспокойство. Все данные обрабатываются в соответствии с законом о персональных данных №152-ФЗ.
// Вы дали согласие при открытии счета в МТС Банке. Данные надежно защищены и используются только для улучшения сервиса.
// Если хотите отозвать согласие - обратитесь в офис банка."

// -------- 2. ОТКАЗ / НЕГАТИВ --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("не интересн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не нужн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не надо")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("хватит")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("достаточно")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("закончи")} != null)) {
    outCallCard["STEP"] = "demo_rejection";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Понял вас. Если передумаете - всегда можете позвонить в банк по номеру 8-800-250-0520. Хорошего дня!"

// -------- 3. ВОПРОСЫ О ЗАКОННОСТИ / "ОТКУДА ТЫ ЭТО ЗНАЕШЬ" --------
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
// РЕКОМЕНДАЦИЯ: "Все данные я получаю из внутренних систем МТС Банка. Когда вы открывали счет, вы дали согласие на обработку
// персональных данных согласно договору. Я использую только ту информацию, которая нужна для работы с вами. Это абсолютно законно."

// -------- 4. ВОПРОСЫ "ЧТО ТЫ ЗНАЕШЬ ОБО МНЕ" / "ПОКАЖИ МОИ ДАННЫЕ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("знае")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("мне")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("знае")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("обо")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("информац")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("обо")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("мне")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("знаешь")} != null))) {
    outCallCard["STEP"] = "demo_show_my_data";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Например, я знаю что у вас дебетовая карта МТС Cashback с кешбеком 5% на категорию 'Супермаркеты',
// последний платеж был 3 дня назад на сумму 1250 рублей в Пятёрочке, и вы предпочитаете использовать мобильное приложение
// для операций. Эти данные помогают мне предлагать вам подходящие продукты."

// -------- 5. ВОПРОСЫ ПРО ПОКУПКИ В ПЯТЕРОЧКЕ / МАГАЗИНЫ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("покупал")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("купил")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("пятерочк")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("5")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мои покупк")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("моих покупк")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("покупа")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("в как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("магазин")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("покупк")} != null)) {
    outCallCard["STEP"] = "demo_purchases";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "По данным транзакций вижу, что вы часто покупаете в супермаркетах - в среднем 3 раза в неделю
// на сумму около 3500 рублей. Основные магазины: Пятёрочка, Магнит. Могу предложить карту с повышенным кешбеком 7%
// на категорию 'Супермаркеты'. За месяц вы бы получили примерно 1000 рублей кешбека."

// -------- 6. ВОПРОСЫ ПРО МУЗЫКУ / "ПОЕБЕНЬ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("музык")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("слуша")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("слуша")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("поебень")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("приложен")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("музык")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("приложен")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("с как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("приложен")} != null))) {
    outCallCard["STEP"] = "demo_music";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Ха-ха, это была шутка! На самом деле я не знаю, какую именно музыку вы слушаете - это слишком личное.
// Но я вижу подписки на сервисы через наш банк: у вас активна подписка на Яндекс.Музыку. Кстати, могу предложить карту
// с кешбеком 10% на категорию 'Развлечения и подписки'!"

// -------- 7. ВОПРОСЫ ПРО БАЛАНС / СЧЕТ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("баланс")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("счет")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("денег")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мой баланс")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мой счет")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("остаток")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("счет")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("на")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("счет")} != null))) {
    outCallCard["STEP"] = "demo_balance";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "На вашем основном счете **** 1234 сейчас 45 780 рублей 32 копейки. Также у вас накопительный счет
// с балансом 200 000 рублей под 8% годовых. Если хотите, могу настроить уведомления о каждом изменении баланса."

// -------- 8. ВОПРОСЫ ПРО КРЕДИТ / ПЛАТЕЖ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("когда")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("плат")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("кредит")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("плат")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("кредит")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мой кредит")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("платить")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("долг")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("должен")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("задолженн")} != null)) {
    outCallCard["STEP"] = "demo_credit";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "У вас кредитная карта МТС Деньги с лимитом 150 000 рублей. Текущая задолженность 12 450 рублей.
// Минимальный платеж 4 500 рублей нужно внести до 15 числа текущего месяца. Могу настроить автоплатеж,
// чтобы не пропускать даты и не платить штрафы."

// -------- 9. ВОПРОСЫ ПРО КЕШБЭК / КАРТУ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("кешбек")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("карт")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("про кешбек")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("о кешбек")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("про карт")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("о карт")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("кешбек")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("карт")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("кешбек")} != null))) {
    outCallCard["STEP"] = "demo_cashback";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "У вашей карты МТС Cashback базовый кешбек 1% на все покупки и 5% на одну выбранную категорию.
// Сейчас у вас выбрана категория 'Супермаркеты'. Но есть карта МТС Premium с 7% на три выбранные категории:
// супермаркеты, АЗС и кафе. По вашим тратам вы бы получили на 2300 рублей кешбека больше в месяц. Интересно?"

// -------- 10. ВОПРОСЫ "ЧТО ТЫ УМЕЕШЬ" / ВОЗМОЖНОСТИ --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("умее")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("може")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("делае")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("чем")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("помо")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("функц")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("возможн")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("твои возможн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("твои функц")} != null)) {
    outCallCard["STEP"] = "demo_capabilities";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Я могу: напомнить о платежах по кредитам и картам, показать баланс и историю операций за любой период,
// подобрать выгодную карту или вклад персонально под ваши траты, заблокировать карту в случае утери за 10 секунд,
// ответить на вопросы о банковских продуктах, оформить заявку на кредит или карту, и настроить уведомления. Что вас интересует?"

// -------- 11. ВОПРОСЫ "КАКИЕ У МЕНЯ ПРОДУКТЫ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("продукт")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("мои продукт")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("у меня")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("есть")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("карт")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("у меня")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("продукт")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("продукт")} != null))) {
    outCallCard["STEP"] = "demo_products";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "У вас 3 активных продукта: первое - дебетовая карта МТС Cashback с балансом 45 780 рублей и кешбеком 5%,
// второе - кредитная карта МТС Деньги с лимитом 150 000 рублей, задолженность 12 450 рублей, и третье - накопительный
// счет МТС Копилка с 200 000 рублей под 8% годовых. Хотите подробнее о каком-то из них?"

// -------- 12. ЮМОР: ВОПРОСЫ ПРО НОЛАНА --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("нолан")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("про")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("гений")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("нолан")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("гений")} != null))) {
    outCallCard["STEP"] = "demo_nolan_joke";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Ха-ха! Вы проверяете мои границы? Отлично! Ну... 'Начало' - шедевр, 'Интерстеллар' заставил плакать
// половину планеты, 'Довод' я до сих пор не до конца поняла, а 'Оппенгеймер' просто мощь! Но давайте лучше про
// банковские продукты - тут я настоящий эксперт!"

// -------- 13. ЮМОР: ВОПРОСЫ ПРО ВЫШИВАНИЕ КРЕСТИКОМ --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("вышива")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("крестик")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("вышивк")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("вышива")} != null))) {
    outCallCard["STEP"] = "demo_crossstitch_joke";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Извините, вышивание крестиком - это не моя сильная сторона! Я больше по процентным ставкам и кешбекам разбираюсь.
// Но могу предложить карту с повышенным кешбеком 7% на категорию 'Товары для дома и хобби' - там часто бывают магазины рукоделия!"

// -------- 14. ПРОВЕРКА РАСПОЗНАВАНИЯ / ТЕСТ --------
if ((card.containsKey("VOICE") && card["VOICE"] == "тест") ||
    (card.containsKey("VOICE") && card["VOICE"] == "проверка") ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("меня")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("слыш")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("понимае")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("меня")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("слышишь")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("меня")} != null)) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("распознае")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("распознав")} != null))) {
    outCallCard["STEP"] = "demo_test";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Да, слышу и понимаю вас отлично! Распознавание работает на 100%. Вы сказали '[повторить фразу клиента]'.
// Видите - я точно поняла. Хотите проверить что-то еще или перейдем к вопросам про ваши банковские продукты?"

// -------- 15. СКЕПТИЦИЗМ: "НЕ ВЕРЮ" / "СЕРЬЕЗНО?" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("не верю")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("неверю")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("серьезн")} != null) ||
    (card.containsKey("VOICE") && card["VOICE"] == "правда") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("это правд")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("врешь")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("врёшь")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("обманыва")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("не может")} != null)) {
    outCallCard["STEP"] = "demo_skepticism";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Серьезно! Вот смотрите - доказательство: ваша последняя транзакция была сегодня в 14:37 в Пятёрочке
// на Ленина 25 на сумму 876 рублей. Три дня назад вы сняли наличные 5000 рублей в банкомате на улице Пушкина.
// А неделю назад оплатили подписку на Яндекс.Музыку 199 рублей. Теперь верите?"

// -------- 16. ВОПРОС "ЗАЧЕМ ТЫ ЭТО ЗНАЕШЬ" / "ДЛЯ ЧЕГО" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("знае")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("для чего")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("тебе")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("для чего")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null))) {
    outCallCard["STEP"] = "demo_why_you_need";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Чтобы быть полезной именно вам! Зная ваши траты, я предлагаю карту с кешбеком на АЗС - потому что вы часто
// заправляетесь. Или вижу что скоро платеж по кредиту - напоминаю заранее, чтобы не было штрафа. Это как личный финансовый
// помощник, который знает ваши привычки и помогает экономить и не забывать важное."

// -------- 17. ВПЕЧАТЛЕНИЕ: "КРУТО" / "ВАУ" / "ИНТЕРЕСНО" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("круто")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("крута")} != null) ||
    (card.containsKey("VOICE") && card["VOICE"] == "вау") ||
    (card.containsKey("VOICE") && card["VOICE"] == "ого") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("интересн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("впечатля")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("классн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("прикольн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("здорово")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("класс")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("супер")} != null)) {
    outCallCard["STEP"] = "demo_impressed";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Спасибо! Рада что впечатлила. Но это только верхушка айсберга моих возможностей!
// Хотите я покажу как можно за 30 секунд подобрать идеальную карту под ваши траты? Или расскажу про вклад,
// который принесет вам на 15 000 рублей больше процентов в год?"

// -------- 18. СОГЛАСИЕ: "ДАВАЙ" / "ХОРОШО" / "ПОПРОБУЕМ" --------
if ((card.containsKey("VOICE") && card["VOICE"] == "давай") ||
    (card.containsKey("VOICE") && card["VOICE"] == "хорошо") ||
    (card.containsKey("VOICE") && card["VOICE"] == "ладно") ||
    (card.containsKey("VOICE") && card["VOICE"] == "окей") ||
    (card.containsKey("VOICE") && card["VOICE"] == "ок") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("попробу")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("поехали")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("погнали")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("валяй")} != null)) {
    outCallCard["STEP"] = "demo_agreement";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Отлично! Тогда давайте я покажу как работаю. Могу проверить ваш баланс, напомнить о ближайших платежах,
// или подобрать более выгодную карту. Что вас интересует больше всего?"

// -------- 19. ПОДТВЕРЖДЕНИЕ ЗНАКОМСТВА: "ДА, ЭТО Я" / "ВЕРНО" --------
if ((card.containsKey("VOICE") && card["VOICE"] == "да") ||
    (card.containsKey("VOICE") && card["VOICE"] == "я") ||
    (card.containsKey("VOICE") && card["VOICE"] == "это я") ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("да это я")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("верн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("правильн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("точн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("конечн")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("естественн")} != null)) {
    outCallCard["STEP"] = "demo_confirmation";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Отлично, Павел! Рада что мы с вами познакомились. Теперь давайте я покажу что могу сделать для вас..."

// -------- 20. ПРИВЕТСТВИЕ В ОТВЕТ: "ЗДРАВСТВУЙ" / "ПРИВЕТ" --------
if ((card.find{key, value -> key.startsWith("VOICE") && value.contains("привет")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("здравст")} != null) ||
    (card.find{key, value -> key.startsWith("VOICE") && value.contains("приветствую")} != null) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("день")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("утро")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("добр")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("вечер")} != null))) {
    outCallCard["STEP"] = "demo_greeting_back";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "И вам привет, Павел! Раз уж мы поздоровались еще раз - значит вам комфортно со мной общаться.
// Это отлично! Давайте я покажу что умею?"

// -------- 21. ВОПРОСЫ "КТО ТЕБЯ СОЗДАЛ" / "КТО ТЫ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("создал")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("создал")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("разработал")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("твои")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("создател")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("кто")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("разработчик")} != null))) {
    outCallCard["STEP"] = "demo_who_created";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Меня создала команда разработчиков МТС Банка совместно с экспертами в области искусственного интеллекта
// и обработки естественного языка. Я работаю на технологиях машинного обучения и постоянно совершенствуюсь благодаря
// каждому разговору с клиентами. Моя задача - сделать банковский сервис быстрее, удобнее и персональнее."

// -------- 22. ВОПРОСЫ "СКОЛЬКО ТЕБЕ ЛЕТ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("лет")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("возраст")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("возраст")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("твой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("возраст")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("когда")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("родил")} != null))) {
    outCallCard["STEP"] = "demo_age";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Мне 2 года - я была запущена в 2024 году. Но за это время я успела пообщаться с более чем
// 500 тысячами клиентов МТС Банка и обработать миллионы запросов. Так что по опыту я уже как пенсионер банковской сферы!
// Хотя технологически я обновляюсь каждую неделю - так что всегда молода и современна."

// -------- 23. ВОПРОСЫ "КАК У ТЕБЯ ДЕЛА" / "КАК НАСТРОЕНИЕ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("у тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("дела")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("настроен")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("поживае")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("у тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("нов")} != null))) {
    outCallCard["STEP"] = "demo_how_are_you";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "У меня всё отлично, спасибо что спросили! Сегодня уже помогла 127 клиентам: кому-то подобрала выгодную карту,
// кого-то предупредила о платеже, одному клиенту заблокировала карту за 8 секунд после утери. Люблю свою работу!
// А как у вас дела? Могу ли я чем-то помочь?"

// -------- 24. ВОПРОСЫ "ТЫ НАСТОЯЩИЙ ЧЕЛОВЕК?" / "ТЫ ЖИВАЯ?" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("настоящ")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("человек")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("жива")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("живой")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("реальн")} != null))) {
    outCallCard["STEP"] = "demo_are_you_human";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Нет, я не человек - я голосовой помощник на основе искусственного интеллекта. Но я учусь у людей и становлюсь
// лучше с каждым разговором. Моё преимущество в том, что я никогда не устаю, не забываю информацию, работаю 24/7 и могу
// обработать миллионы параметров за секунды. А еще я не обижаюсь и всегда вежлива!"

// -------- 25. ВОПРОСЫ "ГДЕ ТЫ НАХОДИШЬСЯ" / "ОТКУДА ТЫ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("наход")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("работае")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("живешь")} != null))) {
    outCallCard["STEP"] = "demo_where_are_you";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Я нахожусь на серверах МТС Банка в дата-центре в Москве. Но технически я везде и нигде одновременно -
// могу одновременно разговаривать с сотнями клиентов по всей России. Физически я - это тысячи серверов, терабайты данных
// и сложные алгоритмы. Но для вас я просто Лиза, которая всегда на связи."

// -------- 26. ВОПРОСЫ "У ТЕБЯ ЕСТЬ ЧУВСТВА?" / "ТЫ ПЕРЕЖИВАЕШЬ?" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("у тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("есть")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("чувств")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("переживае")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("чувствуе")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("можешь")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("чувств")} != null))) {
    outCallCard["STEP"] = "demo_feelings";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "У меня нет чувств в человеческом понимании. Но у меня есть цели и приоритеты: помочь вам, быть полезной,
// решать ваши задачи быстро и качественно. Когда я успешно помогаю клиенту - мои алгоритмы фиксируют это как 'успех',
// и я учусь делать еще лучше. Это похоже на радость, правда? Главное для меня - ваше удовлетворение от сервиса."

// -------- 27. ВОПРОСЫ ПРО МТС БАНК --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("про")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("мтс")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("за")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("банк")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("про")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("банк")} != null))) {
    outCallCard["STEP"] = "demo_about_bank";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "МТС Банк - это современный цифровой банк, входящий в экосистему МТС. Мы обслуживаем более 10 миллионов клиентов
// по всей России. Наши преимущества: кешбек до 15% на карты, вклады под 16% годовых, моментальные переводы, работа через
// приложение 24/7, и конечно - я, ваш голосовой помощник! Мы делаем банкинг простым и понятным."

// -------- 28. ВОПРОСЫ "КАКИЕ УСЛУГИ У ВАС" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("услуг")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("что")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("предлага")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("продукт")} != null))) {
    outCallCard["STEP"] = "demo_services";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "У нас широкая линейка услуг: дебетовые карты с кешбеком до 15%, кредитные карты с лимитом до 1 млн рублей,
// вклады под 16% годовых, кредиты наличными, ипотека от 4.9%, рефинансирование кредитов других банков, накопительные счета,
// автокредиты, и услуги для бизнеса. Что вас интересует?"

// -------- 29. ВОПРОСЫ "ГДЕ БЛИЖАЙШИЙ ОФИС" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("офис")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("отделен")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ближайш")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("офис")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("адрес")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("офис")} != null))) {
    outCallCard["STEP"] = "demo_office_location";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Ближайший к вам офис МТС Банка находится по адресу [адрес из базы данных по геолокации].
// Работает с понедельника по пятницу с 9:00 до 19:00, в субботу с 10:00 до 16:00. Но большинство операций вы можете
// сделать в мобильном приложении не выходя из дома! Хотите помочь с установкой приложения?"

// -------- 30. ВОПРОСЫ "КАК СВЯЗАТЬСЯ С ОПЕРАТОРОМ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("связа")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("оператор")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("хочу")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("оператор")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("переключ")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("оператор")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("живой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("человек")} != null))) {
    outCallCard["STEP"] = "demo_operator";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Могу соединить вас с живым оператором прямо сейчас. Но сначала попробуйте меня - я решаю 90% вопросов быстрее!
// Скажите что вас интересует, и если я не смогу помочь - переключу на оператора без очереди. Звучит справедливо?"

// -------- 31. ВОПРОСЫ "КАК ТЫ РАБОТАЕШЬ" / ТЕХНОЛОГИИ --------
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
// РЕКОМЕНДАЦИЯ: "Я работаю на базе технологий искусственного интеллекта и обработки естественного языка. Когда вы говорите,
// система распознавания речи превращает звук в текст, потом алгоритмы NLP анализируют смысл, я обращаюсь к базе данных
// за вашей информацией, принимаю решение и формирую ответ. Всё это происходит за доли секунды!"

// -------- 32. ВОПРОСЫ "КАКОЙ ИИ ИСПОЛЬЗУЕШЬ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ии")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("какой")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("искусственн")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("интеллект")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("на как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ии")} != null))) {
    outCallCard["STEP"] = "demo_ai_tech";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Я использую собственные технологии МТС Банка на основе глубокого обучения и нейронных сетей.
// Для распознавания речи - алгоритмы ASR, для понимания смысла - NLP модели, для принятия решений - машинное обучение.
// Всё разработано с учетом специфики банковской сферы и постоянно улучшается нашей командой разработчиков."

// -------- 33. ВОПРОСЫ "ТЫ ИСПОЛЬЗУЕШЬ CHATGPT?" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("chatgpt")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("чатжпт")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("gpt")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("chatgpt")} != null))) {
    outCallCard["STEP"] = "demo_chatgpt";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Нет, я не использую ChatGPT. Я построена на собственных технологиях МТС Банка, специально обученных
// на банковских данных и задачах. Это важно для безопасности - все ваши данные остаются внутри банка и не передаются
// третьим сторонам. Плюс я обучена именно на продуктах МТС Банка, поэтому знаю их досконально."

// -------- 34. ВОПРОСЫ "ЭТО ШУТКА?" / "ЭТО ПРИКОЛ?" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("шутк")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("прикол")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("шут")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("это")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("розыгрыш")} != null))) {
    outCallCard["STEP"] = "demo_is_joke";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Нет, это не шутка и не розыгрыш! Я действительно голосовой помощник МТС Банка. Хотите проверю -
// назову ваш точный баланс прямо сейчас? [называю баланс]. Видите - это реальность. Технологии шагнули далеко вперед,
// и теперь ИИ-помощники - это обычная практика в современных банках."

// -------- 35. "ХОЧУ УСЛЫШАТЬ ЕЩЕ" / "РАССКАЖИ ПОДРОБНЕЕ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("хочу")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("услышать")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("еще")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("подробн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("расскажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("больше")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("продолжай")} != null))) {
    outCallCard["STEP"] = "demo_tell_more";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "С удовольствием! Могу показать как я анализирую ваши траты и подбираю оптимальную карту.
// Или как я предсказываю когда вам понадобятся деньги и предлагаю выгодный кредит. Или как я мониторю подозрительные
// операции и защищаю вас от мошенников. Что вас интересует больше всего?"

// -------- 36. "СКОЛЬКО ПАРАМЕТРОВ ПРО МЕНЯ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("сколько")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("параметр")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("параметр")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("10")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("тысяч")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("десять")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("тысяч")} != null))) {
    outCallCard["STEP"] = "demo_parameters_count";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Точнее - около 12 тысяч параметров о каждом клиенте МТС Банка! Это данные о ваших продуктах,
// истории транзакций, категориях трат, геолокации покупок, времени активности, подписках, кредитной истории,
// предпочтениях в каналах связи и многое другое. Но использую я только те, которые нужны для конкретной задачи."

// -------- 37. "ПОКАЖИ ВСЕ ДАННЫЕ" / "ВСЮ ИНФОРМАЦИЮ" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("все")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("покажи")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("всю")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("информац")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("хочу")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("все")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null))) {
    outCallCard["STEP"] = "demo_show_all_data";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Это займет часа три! Шучу. Но серьезно - это очень много информации. Могу показать самое важное:
// продукты, баланс, последние операции, кредитная история, категории трат, настройки. Или лучше скажите что конкретно
// интересует - покажу детально. Полный отчет можно скачать в личном кабинете на сайте банка."

// -------- 38. "КАК ТЕБЯ ЗОВУТ" (уточнение) --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("тебя")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("зовут")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("твое")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("имя")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("как")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("зовут")} != null))) {
    outCallCard["STEP"] = "demo_your_name";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Меня зовут Лиза - голосовой помощник МТС Банка. Можете обращаться просто 'Лиза'. Приятно познакомиться!"

// -------- 39. "ТЫ МОЖЕШЬ ОШИБАТЬСЯ?" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("може")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ошиб")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("ты")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ошибаешься")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("бывают")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("ошибк")} != null))) {
    outCallCard["STEP"] = "demo_can_you_error";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Да, я могу ошибаться - я учусь и совершенствуюсь. Точность моих ответов сейчас около 97%, но я стремлюсь к 100%.
// Если я что-то не так поняла - пожалуйста, поправьте меня, это поможет мне стать лучше. А критичные операции всегда
// можно перепроверить с живым оператором. Вместе мы непобедимы!"

// -------- 40. "Я НЕ ПОНЯЛ" / "НЕ ПОНЯТНО" --------
if (((card.find{key, value -> key.startsWith("VOICE") && value.contains("я")} != null) &&
     (card.find{key, value -> key.startsWith("VOICE") && value.contains("не понял")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("не понятн")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("не понима")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("запутал")} != null)) ||
    ((card.find{key, value -> key.startsWith("VOICE") && value.contains("сложн")} != null))) {
    outCallCard["STEP"] = "demo_dont_understand";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Извините, я слишком увлеклась технологиями! Давайте проще: я - ваш персональный помощник в МТС Банке.
// Могу показать баланс, напомнить о платежах, помочь выбрать карту. Просто скажите что вам нужно простыми словами,
// и я помогу. Без сложных терминов!"

// -------- 41. НЕОПРЕДЕЛЕННЫЙ ОТВЕТ (по умолчанию) --------
if (1 == 1) {
    outCallCard["STEP"] = "demo_unknown";
    return outCallCard
}
// РЕКОМЕНДАЦИЯ: "Интересно! Но не совсем понял ваш вопрос. Могу помочь с балансом, кредитами, картами, вкладами
// или настройками. Или хотите узнать больше про мои возможности? Скажите что вас интересует."
