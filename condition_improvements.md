# ПОЛНЫЙ АНАЛИЗ И РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ УСЛОВИЙ РАСПОЗНАВАНИЯ

**Проанализировано:** 22,648 обращений (16,651 уникальных реплик)

---

## КРИТИЧНЫЕ ПРОБЛЕМЫ (отсутствующие тематики)

### 1. НОВАЯ ТЕМАТИКА: МТС ФЛЕКС / ДВОЙНАЯ ВЫГОДА

**Статус:** ОТСУТСТВУЕТ В CONDITION.TXT
**Найдено:** 53 обращения

**ПРЕДЛАГАЕМОЕ УСЛОВИЕ:**
```groovy
⇒МТС Флекс / Двойная выгода

(card.find{key, value -> key.startsWith("VOICE") && value.contains("флекс")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("двойная выгода")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("мтс лекс")} != null)
&&
(card.find{key, value -> key.startsWith("VOICE") && !value.contains("рефлекс")} != null)
```

**Примеры реплик:**
- "мтс флекс" (18)
- "двойная выгода" (15)
- "программа двойная выгода" (2)
- "отключить флекс" (1)

**Рекомендация:** Добавить ПЕРЕД тематикой "МБ/FIX/SPUTNIK" (строка 363)

---

### 2. НОВАЯ ТЕМАТИКА: ВОЗВРАТ ДЕНЕЖНЫХ СРЕДСТВ

**Статус:** ОТСУТСТВУЕТ КАК ОТДЕЛЬНАЯ ТЕМАТИКА
**Найдено:** ~475 обращений

**ПРЕДЛАГАЕМОЕ УСЛОВИЕ:**
```groovy
⇒Возврат денежных средств

((card.find{key, value -> key.startsWith("VOICE") && value.contains("возврат")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("вернуть")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("где")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("деньг")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("куда")} != null) &&
 ((card.find{key, value -> key.startsWith("VOICE") && value.contains("деньг")} != null) ||
  (card.find{key, value -> key.startsWith("VOICE") && value.contains("ушл")} != null) ||
  (card.find{key, value -> key.startsWith("VOICE") && value.contains("делис")} != null))) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("пропал")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("деньг")} != null)))
&&
(card.find{key, value -> key.startsWith("VOICE") && !value.contains("вклад")} != null)
&&
(card.find{key, value -> key.startsWith("VOICE") && !value.contains("накоп")} != null)
&&
(card.find{key, value -> key.startsWith("VOICE") && !value.contains("кэшбэк")} != null)
```

**Примеры реплик:**
- "возврат денежных средств" (64)
- "возврат денег" (45)
- "возврат средств" (31)
- "где мои деньги" (19)
- "где деньги" (12)
- "куда делись деньги" (8)
- "пропали деньги" (7)
- "куда ушли мои деньги" (5)

**Рекомендация:** Добавить ПОСЛЕ "Списания" (строка 1417)

---

## УЛУЧШЕНИЯ СУЩЕСТВУЮЩИХ ТЕМАТИК

### 3. КЭШБЭК (строка 1032)

**ТЕКУЩЕЕ УСЛОВИЕ:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("кэш")} != null)
```

**ПРОБЛЕМА:** Слишком широкий паттерн "кэш" может ловить нерелевантные запросы.

**ПРЕДЛАГАЕМОЕ УЛУЧШЕНИЕ:**
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
  (card.find{key, value -> key.startsWith("VOICE") && value.contains("списа")} != null) ||
  (card.find{key, value -> key.startsWith("VOICE") && value.contains("бонус")} != null)))
```

**Новые реплики, которые будут пойманы:**
- "потратить кэшбэк" (6)
- "обмен кэшбэка" (3)
- "как перевести кэшбэк в рубли" (4)
- "списание кэшбэка" (2)
- "не списывается кэшбэк" (2)

**Эффект:** +20-30 обращений

---

### 4. ЗАЯВКА, ОБРАЩЕНИЕ (строка 313)

**ТЕКУЩЕЕ УСЛОВИЕ:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("заявк")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("обращен")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("претенз")} != null)
```

**ПРОБЛЕМА:** Не включает "жалоба" - очень частый запрос.

**ПРЕДЛАГАЕМОЕ УЛУЧШЕНИЕ:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("заявк")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("обращен")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("претенз")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("жалоб")} != null)
```

**Новые реплики:**
- "жалоба" (47)
- "оставить жалобу" (20)
- "написать жалобу" (3)
- "хочу оставить жалобу" (3)

**Эффект:** +130 обращений

---

### 5. ПРОБЛЕМЫ СО ВХОДОМ В ЛИЧНЫЙ КАБИНЕТ (строка 1161)

**ТЕКУЩЕЕ УСЛОВИЕ:** Обширное, но пропущены важные варианты.

**ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ к списку приложений:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("мтс деньги")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("эксибанк")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("кошел")} != null)
```

**Новые реплики:**
- "не могу войти в мтс деньги" (9)
- "не могу зайти в мтс деньги" (4)
- "эксибанк" (7)
- "мой кошелек" (8)

**Эффект:** +50 обращений

---

### 6. СПИСАНИЯ (строка 1417)

**ТЕКУЩЕЕ УСЛОВИЕ:**
```groovy
((card.find{key, value -> key.startsWith("VOICE") && value.contains("списа")} != null)
&&
(card.find{key, value -> key.startsWith("VOICE") && value.contains("карт")} != null))
```

**ПРОБЛЕМА:** Требует наличия "карт", но многие спрашивают без упоминания карты.

**ПРЕДЛАГАЕМОЕ УЛУЧШЕНИЕ:**
```groovy
((card.find{key, value -> key.startsWith("VOICE") && value.contains("списа")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("сняли")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("деньги")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("за что")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("сняли")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("списыва")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("деньги")} != null)))
&&
(card.find{key, value -> key.startsWith("VOICE") && !value.contains("распис")} != null)
&&
(card.find{key, value -> key.startsWith("VOICE") && !value.contains("бонус")} != null)
&&
(card.find{key, value -> key.startsWith("VOICE") && !value.contains("кэшбэк")} != null)
```

**Новые реплики:**
- "сняли деньги" (6)
- "за что сняли деньги" (5)
- "почему с меня списывают деньги" (2)
- "списывают деньги с карты" (2)

**Эффект:** +100 обращений

---

### 7. ДЕНЕЖНЫЕ ПЕРЕВОДЫ (строка 1073)

**ТЕКУЩЕЕ УСЛОВИЕ:** Хорошее, но много реплик про перевод кэшбэка.

**ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:**
```groovy
((card.find{key, value -> key.startsWith("VOICE") && value.contains("перевести")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("кэшбэк")} != null))
```

**КОММЕНТАРИЙ:** Возможно, реплики про "перевести кэшбэк" лучше отнести к тематике "Кэшбэк", а не "Денежные переводы". Нужно решить, куда их направлять.

**Примеры:**
- "как перевести кэшбэк в рубли" (4)
- "не могу перевести кэшбэк" (3)
- "перевести кэшбэк на карту" (2)

---

### 8. ПЕРЕВЫПУСК КАРТЫ (строка 330)

**ТЕКУЩЕЕ УСЛОВИЕ:** Содержит "перевыпус", но пропущены вариации.

**ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("перевыпус")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("перезапустить")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("заменить")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("карт")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("новую")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("карту")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("оформ")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("сломан")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("карт")} != null))
```

**Новые реплики:**
- "заменить карту" (3)
- "выпустить новую карту" (1)
- "заменить сломанную карту" (1)

**Эффект:** +15 обращений

---

### 9. ПРОСРОЧКА / ЗАДОЛЖЕННОСТЬ (строка 513)

**ТЕКУЩЕЕ УСЛОВИЕ:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("просроч")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("отдел")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("задолж")} != null))
```

**ПРОБЛЕМА:** Не ловит просто "задолженность" или "долг".

**ПРЕДЛАГАЕМОЕ УЛУЧШЕНИЕ:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("просроч")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("задолж")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("отдел")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("взыскани")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("откуда")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("долг")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("почему")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("задолж")} != null))
```

**Новые реплики:**
- "откуда задолженность" (2)
- "почему у меня задолженность" (2)
- "откуда у меня долг" (1)

**Эффект:** +50 обращений

---

### 10. БАНКОМАТЫ / ТЕРМИНАЛЫ (отсутствует отдельная тематика!)

**Статус:** НЕТ ОТДЕЛЬНОЙ ТЕМАТИКИ
**Найдено:** 237 обращений

**ПРЕДЛАГАЕМОЕ УСЛОВИЕ:**
```groovy
⇒Банкоматы и терминалы

(card.find{key, value -> key.startsWith("VOICE") && value.contains("банкомат")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("терминал")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("снять")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("наличн")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("съел")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("купюр")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("застрял")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("деньг")} != null))
```

**Примеры реплик:**
- "банкоматы" (6)
- "терминал оплаты" (4)
- "не работает терминал" (3)
- "забыл деньги в банкомате" (2)
- "банкомат съел купюру" (2)

**Рекомендация:** Добавить после "Способы оплаты" (строка 650)

---

### 11. ОФОРМИТЬ КАРТУ (строка 831)

**ТЕКУЩЕЕ УСЛОВИЕ:** Хорошее, но можно добавить варианты.

**ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("заказать карт")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("хочу")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("дебетов")} != null))
```

**Новые реплики:**
- "нет я хочу оформить дебетовую" (1)
- и подобные

**Эффект:** +10 обращений

---

### 12. ПОДКЛЮЧИТЬ УСЛУГИ (строка 1456)

**ТЕКУЩЕЕ УСЛОВИЕ:** Только "подключ" + (смс/услуги/уведомления).

**ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("систем.*быстр.*платеж")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("подключ")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("сбп")} != null))
```

**Новые реплики:**
- "подключить систему быстрых платежей" (2)
- "система быстрых платежей" (2)

**Эффект:** +10 обращений

---

### 13. ИЗМЕНЕНИЕ ПД (строка 1049)

**ТЕКУЩЕЕ УСЛОВИЕ:** Хорошее, но пропущены варианты с "запрет на обработку".

**ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:**
```groovy
((card.find{key, value -> key.startsWith("VOICE") && value.contains("запрет")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("персональн")} != null)) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("снять")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("запрет")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("данн")} != null))
```

**Новые реплики:**
- "снять запрет на обработку персональных данных" (4)
- "запрет на обработку персональных данных" (2)

**Эффект:** +15 обращений

---

### 14. КОМИССИЯ (строка 1234)

**ТЕКУЩЕЕ УСЛОВИЕ:** Требует комбинацию (обслуж + карт) или (год/мес + обслуж/комис).

**ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:**
```groovy
(card.containsKey("VOICE") && card["VOICE"] in ["комиссия", "комиссии"]) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("комисс")} != null) &&
 ((card.find{key, value -> key.startsWith("VOICE") && value.contains("за что")} != null) ||
  (card.find{key, value -> key.startsWith("VOICE") && value.contains("почему")} != null) ||
  (card.find{key, value -> key.startsWith("VOICE") && value.contains("снима")} != null)))
```

**Новые реплики:**
- "комиссия" (4)
- "комиссия банка" (2)
- "за что комиссия" (1)
- "почему взимают комиссию" (1)

**Эффект:** +20 обращений

---

### 15. ПРОПУЩЕННЫЙ ЗВОНОК ОТ БАНКА (строка 718)

**ТЕКУЩЕЕ УСЛОВИЕ:** Обширное и хорошее.

**ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ для вариаций:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("зачем звонили")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("что звонили")} != null) ||
(card.find{key, value -> key.startsWith("VOICE") && value.contains("от вас звонили")} != null)
```

**Новые реплики:**
- "зачем звонили" (4)
- "а зачем звонили" (2)
- "что звонили" (2)

**Эффект:** +10 обращений

---

### 16. СТАТУС ЗАЯВКИ НА КРЕДИТ/КАРТУ (строка 780)

**ТЕКУЩЕЕ УСЛОВИЕ:** Хорошее, но можно добавить.

**ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("статус заявлен")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("мне одобрен")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && !value.contains("отдел")} != null))
```

**Новые реплики:**
- "статус заявления" (3)
- "мне одобрено" (несколько вариаций)

**Эффект:** +15 обращений

---

### 17. ДОСТАВКА / КУРЬЕР (включено в "Статус заявки", строка 812)

**ТЕКУЩЕЕ УСЛОВИЕ:** Есть "доставк", но можно уточнить.

**ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("курьер")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("когда")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("приедет")} != null))
```

**Новые реплики:**
- "когда приедет курьер" (4)
- "где курьер" (2)

**Эффект:** +15 обращений

---

### 18. ВКЛАДЫ (строка 904)

**ТЕКУЩЕЕ УСЛОВИЕ:** Очень обширное с множеством вариаций.

**ПРЕДЛАГАЕМОЕ УТОЧНЕНИЕ (добавить исключение):**
```groovy
&& (card.find{key, value -> key.startsWith("VOICE") && !value.contains("кэшбэк")} != null)
&& (card.find{key, value -> key.startsWith("VOICE") && !value.contains("кешбэк")} != null)
```

**КОММЕНТАРИЙ:** Исключить реплики типа "сколько кэшбэка накопилось" - они должны идти в Кэшбэк, а не во Вклады.

---

### 19. МОШЕННИЧЕСТВО (строка 1035)

**ТЕКУЩЕЕ УСЛОВИЕ:** Хорошее.

**ПРЕДЛАГАЕМОЕ ДОПОЛНЕНИЕ:**
```groovy
(card.find{key, value -> key.startsWith("VOICE") && value.contains("безопасност")} != null) ||
((card.find{key, value -> key.startsWith("VOICE") && value.contains("отдел")} != null) &&
 (card.find{key, value -> key.startsWith("VOICE") && value.contains("безопас")} != null))
```

**Новые реплики:**
- "безопасность" (2)
- "отдел безопасности" (несколько)
- "свяжите с отделом безопасности" (1)

**Эффект:** +20 обращений

---

## РЕКОМЕНДУЕМЫЙ ПОРЯДОК УСЛОВИЙ

### Текущий порядок vs Предлагаемый порядок:

| # | Текущий порядок | Предлагаемый порядок | Изменение |
|---|----------------|---------------------|-----------|
| 1 | Молчание, ошибки ASR_TTS | Молчание, ошибки ASR_TTS | Без изменений |
| 2 | Счетчик ПИН | Счетчик ПИН | Без изменений |
| 3 | PIN | PIN | Без изменений |
| 4 | ОМТ | ОМТ | Без изменений |
| 5 | Страховка | Страховка | Без изменений |
| 6 | - | **МТС Флекс / Двойная выгода** | **ДОБАВИТЬ** |
| 7 | Баланс карты | Баланс карты | Без изменений |
| 8 | Увеличить лимит | Увеличить лимит | Без изменений |
| ... | ... | ... | ... |
| 15 | Заявка, обращение | Заявка, обращение | **+ "жалоб"** |
| ... | ... | ... | ... |
| 28 | Способы оплаты | Способы оплаты | Без изменений |
| 29 | - | **Банкоматы и терминалы** | **ДОБАВИТЬ** |
| 30 | Аресты | Аресты | Без изменений |
| ... | ... | ... | ... |
| 45 | Списания | Списания | **Улучшить** |
| 46 | - | **Возврат денежных средств** | **ДОБАВИТЬ** |
| ... | ... | ... | ... |

### Почему такой порядок:

1. **МТС Флекс** добавляется ПЕРЕД "МБ/FIX/SPUTNIK" (строка 363), чтобы слово "флекс" не попадало в другие тематики.

2. **Банкоматы и терминалы** добавляется ПОСЛЕ "Способы оплаты", так как это логически связанные темы.

3. **Возврат денежных средств** добавляется ПОСЛЕ "Списания", так как тематически связано (деньги исчезли → где они → хочу вернуть).

4. **Жалоба** добавляется в "Заявка, обращение", а не как отдельная тематика, чтобы не дублировать логику.

---

## СВОДКА ЭФФЕКТА

| Изменение | Дополнительные обращения |
|-----------|-------------------------|
| МТС Флекс / Двойная выгода (новая) | +53 |
| Возврат денежных средств (новая) | +475 |
| Банкоматы и терминалы (новая) | +237 |
| Кэшбэк (улучшение) | +30 |
| Заявка/обращение + жалоба | +130 |
| Проблемы со входом + МТС Деньги | +50 |
| Списания (улучшение) | +100 |
| Просрочка/задолженность | +50 |
| Изменение ПД | +15 |
| Прочие улучшения | +60 |
| **ИТОГО** | **~1200 обращений** |

---

## ОБЩИЕ РЕКОМЕНДАЦИИ

1. **Обрезанные слова ASR:** Много реплик содержат обрезанные слова ("атор" вместо "оператор", "ратор", "опера"). Это может влиять на другие тематики - проверьте, не ловят ли их случайно.

2. **Порядок важен:** Более специфичные условия должны идти РАНЬШЕ общих. Например, "МТС Флекс" должен проверяться до "МБ/FIX/SPUTNIK".

3. **Исключения:** Во всех условиях используйте исключения (`!value.contains`), чтобы избежать пересечений между тематиками.

4. **Тестирование:** После внедрения изменений рекомендуется прогнать тестовую выборку реплик, чтобы проверить корректность классификации.
