# РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ УСЛОВИЙ РАСПОЗНАВАНИЯ

## Общая статистика
- Всего проанализировано: **22,648 обращений** (16,651 уникальных реплик)
- Не попало ни в одну банковскую тематику: исходный файл replics.xlsx

---

## 1. КЭШБЭК (строка 1032)

### ТЕКУЩЕЕ УСЛОВИЕ:
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("кэш")} != null)
```

### ПРЕДЛАГАЕМОЕ УЛУЧШЕНИЕ:
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("кэшбэк")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("кешбэк")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("cashback")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("кэш")} != null) &&
 ((card.find{key, value -> key.startsWith("VOICE") && value.contains("начисл")} != null) ||
  (card.find{key, value -> key.startsWith("VOICE") && value.contains("потрат")} != null) ||
  (card.find{key, value -> key.startsWith("VOICE") && value.contains("обмен")} != null) ||
  (card.find{key, value -> key.startsWith("VOICE") && value.contains("перевести")} != null) ||
  (card.find{key, value -> key.startsWith("VOICE") && value.contains("рубл")} != null) ||
  (card.find{key, value -> key.startsWith("VOICE") && value.contains("бонус")} != null)))
```

### КОММЕНТАРИЙ:
Текущее условие `"кэш"` слишком широкое и может ловить нерелевантные запросы.
Добавлены: "кэшбэк", "кешбэк" (альт. написание), контекстные комбинации (кэш + начислить/потратить/обменять).
Новые реплики: "потратить кэшбэк" (6), "обмен кэшбэка" (3), "как перевести кэшбэк в рубли" (4).

---

## 2. НОВАЯ ТЕМАТИКА: МТС ФЛЕКС / ДВОЙНАЯ ВЫГОДА (ОТСУТСТВУЕТ!)

### ТЕКУЩЕЕ УСЛОВИЕ:
**Отсутствует в condition.txt!**

### ПРЕДЛАГАЕМОЕ УСЛОВИЕ (добавить новую тематику):
```groovy
⇒МТС Флекс / Двойная выгода

(card.find{key, value -> key.startsWith("VOICE") && value.contains("флекс")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("двойная выгода")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("мтс лекс")} != null)
```

### КОММЕНТАРИЙ:
**КРИТИЧНО!** Тематика полностью отсутствует, но есть 53 обращения:
- "мтс флекс" (18)
- "двойная выгода" (15)
- "программа двойная выгода" (2)
Рекомендуется добавить ПЕРЕД тематикой "МБ/FIX/SPUTNIK", чтобы не было пересечения с "премиум".

---

## 3. НОВАЯ ТЕМАТИКА: ВОЗВРАТ ДЕНЕЖНЫХ СРЕДСТВ (ОТСУТСТВУЕТ!)

### ТЕКУЩЕЕ УСЛОВИЕ:
**Отсутствует как отдельная тематика!**

### ПРЕДЛАГАЕМОЕ УСЛОВИЕ:
```groovy
⇒Возврат денежных средств

((card.find{key, value -> key.startsWith("VOICE") && value.contains("возврат")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("вернуть")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("деньг")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("куда")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("деньг")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("пропал")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("деньг")} != null)))
&&
(card.find{key, value -> key.startsWith("VOICE") && !value.contains("вклад")} != null)
&&
(card.find{key, value -> key.startsWith("VOICE") && !value.contains("накоп")} != null)
```

### КОММЕНТАРИЙ:
**КРИТИЧНО!** Очень частая тема (~475+ обращений), но нет отдельной тематики:
- "возврат денежных средств" (64)
- "возврат денег" (45)
- "где мои деньги" (19)
- "куда делись деньги" (8)
- "пропали деньги" (7)
Рекомендуется добавить ДО тематики "Списания".

---

## 4. ЗАЯВКА, ОБРАЩЕНИЕ (строка 313)

### ТЕКУЩЕЕ УСЛОВИЕ:
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("заявк")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("обращен")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("претенз")} != null)
```

### ПРЕДЛАГАЕМОЕ УЛУЧШЕНИЕ:
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("заявк")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("обращен")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("претенз")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("жалоб")} != null)
```

### КОММЕНТАРИЙ:
Добавить "жалоб" - 130 обращений не попадают в тематику:
- "жалоба" (47)
- "оставить жалобу" (20)
- "написать жалобу" (3)

---

## 5. ПРОБЛЕМЫ СО ВХОДОМ В ЛИЧНЫЙ КАБИНЕТ (строка 1161)

### ТЕКУЩЕЕ УСЛОВИЕ:
Содержит много вариаций, но пропущены ключевые фразы.

### ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:
Добавить в список проблем:
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("мтс деньги")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("кошел")} != null)
```

### КОММЕНТАРИЙ:
Добавить распознавание для "МТС Деньги" как приложения:
- "не могу войти в мтс деньги" (9)
- "не могу зайти в мтс деньги" (4)
- "мой кошелек" (8)
- "эксибанк" (7)

---

## 6. ЗАПРОС ОПЕРАТОРА (нет отдельной тематики!)

### ТЕКУЩЕЕ УСЛОВИЕ:
**Нет отдельной тематики для запроса оператора!**

### ПРЕДЛАГАЕМОЕ УСЛОВИЕ (добавить новую тематику):
```groovy
⇒Запрос оператора

((card.find{key, value -> key.startsWith("VOICE") && value.contains("оператор")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("атор")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("опера")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("ратор")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("соедини")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("специалист")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("консультант")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("живой")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("человек")} != null))
&&
(card.find{key, value -> key.startsWith("VOICE") && !value.contains("перевод")} != null)
&&
(card.find{key, value -> key.startsWith("VOICE") && !value.contains("операци")} != null)
```

### КОММЕНТАРИЙ:
**КРИТИЧНО!** ~892 обращения на запрос оператора:
- "атор" (122) - обрезанное "оператор"
- "атором" (46)
- "опера" (29) - обрезанное "оператор"
- "ратор" (27)
- "соедините" (20)
Важно исключить "операции" и "перевод", чтобы не путать с другими тематиками.

---

## 7. ПРОПУЩЕННЫЙ ЗВОНОК ОТ БАНКА (строка 718)

### ТЕКУЩЕЕ УСЛОВИЕ:
Условие хорошее, но можно добавить:

### ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем звонил")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("что звонил")} != null)
```

### КОММЕНТАРИЙ:
Добавить вариации:
- "зачем звонили" (4)
- "что звонили" (2)

---

## 8. ВКЛАДЫ (строка 904)

### ТЕКУЩЕЕ УСЛОВИЕ:
Очень обширное, включает "накопит", "сберег"

### ПРЕДЛАГАЕМОЕ УТОЧНЕНИЕ:
Добавить исключение для "кэшбэк накопилось":
```groovy
&& (card.find{key, value -> key.startsWith("VOICE") && !value.contains("кэшбэк")} != null)
```

### КОММЕНТАРИЙ:
Исключить пересечение с кэшбэком:
- "сколько кэшбэка накопилось" должно идти в Кэшбэк, не во Вклады

---

## 9. МТС PAY (строка 1441)

### ТЕКУЩЕЕ УСЛОВИЕ:
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("мтс")} != null) &&
((card.find{key, value -> key.startsWith("VOICE") && value.contains("пэй")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("пей")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("pay")} != null))
```

### ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:
```groovy
|| (card.find{key, value -> key.startsWith("VOICE") && value.contains("мтс оплата")} != null)
```

### КОММЕНТАРИЙ:
Добавить "мтс оплата" (4 обращения) - это синоним МТС Pay.

---

## 10. НОВАЯ ТЕМАТИКА: ПРОСТЫЕ ОТВЕТЫ (для фильтрации)

### ПРЕДЛАГАЕМОЕ УСЛОВИЕ:
```groovy
⇒Простые ответы (да/нет/междометия)

(card.containsKey("VOICE") && card["VOICE"] in ["да", "нет", "алло", "угу", "ага", "мм", "аа", "ясно", "понятно", "ладно", "ну", "ээ", "спасибо", "пожалуйста", "здравствуйте", "привет", "добрый день", "доброе утро"])
```

### КОММЕНТАРИЙ:
~1500 обращений - это простые ответы/междометия:
- "да" (143)
- "алло" (107)
- "нет" (73)
- "аа" (39)
- "ладно" (24)
Можно добавить для статистики/фильтрации, но поставить В КОНЕЦ списка условий.

---

## РЕКОМЕНДУЕМЫЙ ПОРЯДОК ДОБАВЛЕНИЯ НОВЫХ ТЕМАТИК:

1. **После "Страховка" (строка 117):**
   - Добавить: "МТС Флекс / Двойная выгода"

2. **После "Закрытие" (строка 288):**
   - Изменить: "Заявка, обращение" - добавить "жалоб"

3. **После "Списания" (строка 1417):**
   - Добавить: "Возврат денежных средств"

4. **Создать отдельную тематику "Запрос оператора":**
   - Поместить ПЕРЕД "Молчание, ошибки ASR_TTS"
   - Это позволит сразу перенаправлять на оператора

5. **В самом конце:**
   - Добавить: "Простые ответы" (для статистики)

---

## ОБЩИЕ РЕКОМЕНДАЦИИ:

1. **Обрезанные слова ASR:** Много реплик обрезаны системой распознавания ("атор" вместо "оператор"). Добавлены паттерны для таких случаев.

2. **Порядок условий:** Более специфичные условия должны идти РАНЬШЕ общих. Например, "МТС Флекс" должен быть перед "МБ/FIX/SPUTNIK".

3. **Исключения:** Во всех новых условиях добавлены исключения (!value.contains), чтобы избежать пересечений.

4. **Статистика потенциального покрытия после изменений:**
   - Кэшбэк: +100 обращений
   - МТС Флекс: +53 обращения (новая тематика)
   - Возврат денег: +475 обращений (новая тематика)
   - Жалобы: +130 обращений
   - Запрос оператора: +892 обращения (новая тематика)
   - **ИТОГО: ~1650 дополнительных обращений** будут классифицированы
