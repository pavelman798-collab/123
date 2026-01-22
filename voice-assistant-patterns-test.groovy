/**
 * Тесты для регулярных выражений обработки речи голосового ассистента
 * Демонстрация работы паттернов на реальных примерах фраз
 */

// Загружаем класс с паттернами
evaluate(new File('voice-assistant-patterns.groovy'))

class VoiceAssistantPatternsTest {

    /**
     * Набор тестовых фраз с ожидаемыми категориями
     */
    static final TEST_CASES = [
        // ===== ПРИВЕТСТВИЯ =====
        [phrase: "Привет!", expected: ['greeting']],
        [phrase: "Приветствую!", expected: ['greeting']],
        [phrase: "Здравствуйте", expected: ['greeting']],
        [phrase: "Здравствуй, Лиза", expected: ['greeting']],
        [phrase: "Добрый день", expected: ['greeting']],
        [phrase: "Доброе утро", expected: ['greeting']],
        [phrase: "Хай", expected: ['greeting']],
        [phrase: "Алло", expected: ['greeting']],
        [phrase: "Привет Лиза", expected: ['greeting']],
        [phrase: "Ну привет", expected: ['greeting']],

        // ===== ВЕЖЛИВЫЕ ОТВЕТЫ =====
        [phrase: "Спасибо", expected: ['polite']],
        [phrase: "Спасибо большое", expected: ['polite']],
        [phrase: "Благодарю", expected: ['polite']],
        [phrase: "Очень приятно", expected: ['polite']],
        [phrase: "Приятно познакомиться", expected: ['polite']],
        [phrase: "Рад слышать", expected: ['polite']],
        [phrase: "Рада с вами познакомиться", expected: ['polite']],
        [phrase: "Отлично!", expected: ['polite']],
        [phrase: "Замечательно", expected: ['polite']],

        // ===== СОГЛАСИЕ / ПОДТВЕРЖДЕНИЕ =====
        [phrase: "Да", expected: ['confirmation']],
        [phrase: "Ага", expected: ['confirmation']],
        [phrase: "Угу", expected: ['confirmation']],
        [phrase: "Слушаю", expected: ['confirmation']],
        [phrase: "Да, слушаю", expected: ['confirmation']],
        [phrase: "Понял", expected: ['confirmation']],
        [phrase: "Поняла", expected: ['confirmation']],
        [phrase: "Ясно", expected: ['confirmation']],
        [phrase: "Давай", expected: ['confirmation']],
        [phrase: "Ладно", expected: ['confirmation']],
        [phrase: "Окей", expected: ['confirmation']],

        // ===== ВОПРОСЫ О ВОЗМОЖНОСТЯХ =====
        [phrase: "Что ты умеешь?", expected: ['capability_question']],
        [phrase: "Что вы можете?", expected: ['capability_question']],
        [phrase: "Чем можешь помочь?", expected: ['capability_question']],
        [phrase: "Чем ты можешь мне помочь?", expected: ['capability_question']],
        [phrase: "Что ты предлагаешь?", expected: ['capability_question']],
        [phrase: "Зачем ты нужна?", expected: ['capability_question']],
        [phrase: "Какие у тебя функции?", expected: ['capability_question']],
        [phrase: "Какие возможности?", expected: ['capability_question']],

        // ===== ВОПРОСЫ ПРО ДЕЛА =====
        [phrase: "Как дела?", expected: ['small_talk']],
        [phrase: "Как ты?", expected: ['small_talk']],
        [phrase: "Как у тебя дела?", expected: ['small_talk']],
        [phrase: "Что нового?", expected: ['small_talk']],
        [phrase: "Все хорошо?", expected: ['small_talk']],
        [phrase: "Как настроение?", expected: ['small_talk']],

        // ===== ВОПРОСЫ ИДЕНТИФИКАЦИИ =====
        [phrase: "Кто ты?", expected: ['identity_question']],
        [phrase: "Ты кто?", expected: ['identity_question']],
        [phrase: "Кто говорит?", expected: ['identity_question']],
        [phrase: "Представься", expected: ['identity_question']],
        [phrase: "Как тебя зовут?", expected: ['identity_question']],
        [phrase: "Назови себя", expected: ['identity_question']],
        [phrase: "Кто ты такая?", expected: ['identity_question']],

        // ===== ВОПРОСЫ О ЦЕЛИ ЗВОНКА =====
        [phrase: "Зачем звонишь?", expected: ['purpose_question']],
        [phrase: "Что нужно?", expected: ['purpose_question']],
        [phrase: "Что хотите?", expected: ['purpose_question']],
        [phrase: "По какому вопросу?", expected: ['purpose_question']],
        [phrase: "В чем дело?", expected: ['purpose_question']],
        [phrase: "Что случилось?", expected: ['purpose_question']],

        // ===== ОТКАЗЫ =====
        [phrase: "Не нужно", expected: ['rejection']],
        [phrase: "Не интересно", expected: ['rejection']],
        [phrase: "Отстань", expected: ['rejection']],
        [phrase: "Положи трубку", expected: ['rejection']],
        [phrase: "До свидания", expected: ['rejection']],
        [phrase: "Пока", expected: ['rejection']],
        [phrase: "Не звони больше", expected: ['rejection']],
        [phrase: "Мне это не нужно", expected: ['rejection']],

        // ===== ПЕРЕСПРОС =====
        [phrase: "Что?", expected: ['clarification']],
        [phrase: "А?", expected: ['clarification']],
        [phrase: "Чего?", expected: ['clarification']],
        [phrase: "Не расслышал", expected: ['clarification']],
        [phrase: "Не слышу", expected: ['clarification']],
        [phrase: "Плохо слышно", expected: ['clarification']],
        [phrase: "Повтори", expected: ['clarification']],
        [phrase: "Извините, что?", expected: ['clarification']],

        // ===== ПРОСЬБЫ ПОДОЖДАТЬ =====
        [phrase: "Секунду", expected: ['wait']],
        [phrase: "Минутку", expected: ['wait']],
        [phrase: "Сейчас", expected: ['wait']],
        [phrase: "Одну секунду", expected: ['wait']],
        [phrase: "Подожди", expected: ['wait']],

        // ===== ЗАНЯТ =====
        [phrase: "Я занят", expected: ['busy']],
        [phrase: "Занята", expected: ['busy']],
        [phrase: "Не могу говорить", expected: ['busy']],
        [phrase: "Перезвоните позже", expected: ['busy']],
        [phrase: "Я за рулем", expected: ['busy']],
        [phrase: "Сейчас неудобно", expected: ['busy']],

        // ===== ВОПРОСЫ О РОБОТЕ =====
        [phrase: "Ты робот?", expected: ['bot_question']],
        [phrase: "Ты бот?", expected: ['bot_question']],
        [phrase: "Это автоответчик?", expected: ['bot_question']],
        [phrase: "С кем я говорю?", expected: ['bot_question']],
        [phrase: "Живой человек?", expected: ['bot_question']],

        // ===== КОМБИНИРОВАННЫЕ ФРАЗЫ (несколько категорий) =====
        [phrase: "Привет! Спасибо за звонок", expected: ['greeting', 'polite']],
        [phrase: "Привет! Что ты умеешь?", expected: ['greeting', 'capability_question']],
        [phrase: "Здравствуйте. Рад слышать", expected: ['greeting', 'polite']],
        [phrase: "Приветствую! Чем можешь помочь?", expected: ['greeting', 'capability_question']],
        [phrase: "Привет. Кто ты?", expected: ['greeting', 'identity_question']],
        [phrase: "Добрый день. Зачем звонишь?", expected: ['greeting', 'purpose_question']],

        // ===== РЕАЛИСТИЧНЫЕ ФРАЗЫ =====
        [phrase: "Привет Лиза, очень приятно познакомиться", expected: ['greeting', 'polite']],
        [phrase: "Здравствуйте, а что вы предлагаете?", expected: ['greeting', 'capability_question']],
        [phrase: "Да, слушаю вас", expected: ['confirmation']],
        [phrase: "Ну давай, расскажи что умеешь", expected: ['confirmation', 'capability_question']],
        [phrase: "Извините, не расслышал вас", expected: ['clarification']],
        [phrase: "Сейчас не могу говорить, перезвоните", expected: ['wait', 'busy']],
    ]

    /**
     * Запуск всех тестов
     */
    static void runAllTests() {
        println "=" * 100
        println "ТЕСТИРОВАНИЕ РЕГУЛЯРНЫХ ВЫРАЖЕНИЙ ГОЛОСОВОГО АССИСТЕНТА"
        println "=" * 100
        println ""

        def totalTests = TEST_CASES.size()
        def passedTests = 0
        def failedTests = 0

        TEST_CASES.eachWithIndex { testCase, index ->
            def phrase = testCase.phrase
            def expected = testCase.expected
            def actual = VoiceAssistantPatterns.categorizeAll(phrase)

            // Проверяем, что все ожидаемые категории присутствуют
            def passed = expected.every { actual.contains(it) } &&
                         (actual.size() == expected.size() || actual.contains('unknown'))

            if (passed) {
                passedTests++
                println "[✓] ${(index + 1).toString().padLeft(3)}. ${phrase.padRight(50)} -> ${actual.join(', ')}"
            } else {
                failedTests++
                println "[✗] ${(index + 1).toString().padLeft(3)}. ${phrase.padRight(50)}"
                println "     Ожидалось: ${expected.join(', ')}"
                println "     Получено:  ${actual.join(', ')}"
            }
        }

        println ""
        println "=" * 100
        println "РЕЗУЛЬТАТЫ:"
        println "  Всего тестов: ${totalTests}"
        println "  Успешно: ${passedTests} (${(passedTests * 100 / totalTests).round(1)}%)"
        println "  Провалено: ${failedTests}"
        println "=" * 100
    }

    /**
     * Интерактивное тестирование
     */
    static void interactiveTest() {
        println "\n" + "=" * 100
        println "ИНТЕРАКТИВНОЕ ТЕСТИРОВАНИЕ"
        println "Введите фразу для распознавания (или 'exit' для выхода)"
        println "=" * 100

        def reader = System.in.newReader()
        while (true) {
            print "\nВаша фраза: "
            System.out.flush()
            def input = reader.readLine()

            if (!input || input.toLowerCase() == 'exit') {
                println "Завершение..."
                break
            }

            def categories = VoiceAssistantPatterns.categorizeAll(input)
            println "  Категории: ${categories.join(', ')}"

            // Детальная проверка по каждой группе паттернов
            println "  Детали:"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.GREETINGS))
                println "    - Приветствие"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.POLITE_RESPONSES))
                println "    - Вежливый ответ"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.CONFIRMATIONS))
                println "    - Подтверждение"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.CAPABILITY_QUESTIONS))
                println "    - Вопрос о возможностях"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.SMALL_TALK))
                println "    - Светская беседа"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.IDENTITY_QUESTIONS))
                println "    - Вопрос идентификации"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.PURPOSE_QUESTIONS))
                println "    - Вопрос о цели звонка"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.REJECTIONS))
                println "    - Отказ"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.CLARIFICATIONS))
                println "    - Переспрос"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.WAIT_REQUESTS))
                println "    - Просьба подождать"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.BUSY_RESPONSES))
                println "    - Занят"
            if (VoiceAssistantPatterns.matches(input, VoiceAssistantPatterns.BOT_QUESTIONS))
                println "    - Вопрос о роботе"
        }
    }

    /**
     * Тест производительности
     */
    static void performanceTest() {
        println "\n" + "=" * 100
        println "ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ"
        println "=" * 100

        def iterations = 10000
        def testPhrase = "Привет! Очень приятно познакомиться. Что ты умеешь делать?"

        println "Фраза для теста: ${testPhrase}"
        println "Количество итераций: ${iterations}"
        println ""

        // Прогрев
        100.times { VoiceAssistantPatterns.categorizeAll(testPhrase) }

        // Основной тест
        def startTime = System.currentTimeMillis()
        iterations.times {
            VoiceAssistantPatterns.categorizeAll(testPhrase)
        }
        def endTime = System.currentTimeMillis()

        def totalTime = endTime - startTime
        def avgTime = totalTime / iterations

        println "Результаты:"
        println "  Общее время: ${totalTime} мс"
        println "  Среднее время на 1 распознавание: ${avgTime.round(3)} мс"
        println "  Распознаваний в секунду: ${(1000 / avgTime).round(0)}"
        println "=" * 100
    }

    /**
     * Статистика по категориям
     */
    static void categoryStatistics() {
        println "\n" + "=" * 100
        println "СТАТИСТИКА ПО КАТЕГОРИЯМ"
        println "=" * 100

        def categoryCount = [:]

        TEST_CASES.each { testCase ->
            def categories = VoiceAssistantPatterns.categorizeAll(testCase.phrase)
            categories.each { category ->
                categoryCount[category] = (categoryCount[category] ?: 0) + 1
            }
        }

        println "\nКоличество фраз по категориям:"
        categoryCount.sort { -it.value }.each { category, count ->
            def percentage = (count * 100 / TEST_CASES.size()).round(1)
            println "  ${category.padRight(25)}: ${count.toString().padLeft(3)} (${percentage}%)"
        }

        println ""
        println "Общее количество тестовых фраз: ${TEST_CASES.size()}"
        println "=" * 100
    }
}

// =====================================================
// ЗАПУСК ТЕСТОВ
// =====================================================

println """
╔════════════════════════════════════════════════════════════════════════════════╗
║         ТЕСТИРОВАНИЕ ПАТТЕРНОВ РАСПОЗНАВАНИЯ РЕЧИ ГОЛОСОВОГО АССИСТЕНТА         ║
╚════════════════════════════════════════════════════════════════════════════════╝

Выберите режим тестирования:

  1. Запустить все автоматические тесты
  2. Интерактивное тестирование (ввод своих фраз)
  3. Тест производительности
  4. Статистика по категориям
  5. Запустить всё

Ваш выбор (1-5):
"""

def reader = System.in.newReader()
def choice = reader.readLine()?.trim()

switch (choice) {
    case '1':
        VoiceAssistantPatternsTest.runAllTests()
        break
    case '2':
        VoiceAssistantPatternsTest.interactiveTest()
        break
    case '3':
        VoiceAssistantPatternsTest.performanceTest()
        break
    case '4':
        VoiceAssistantPatternsTest.categoryStatistics()
        break
    case '5':
        VoiceAssistantPatternsTest.runAllTests()
        VoiceAssistantPatternsTest.categoryStatistics()
        VoiceAssistantPatternsTest.performanceTest()
        VoiceAssistantPatternsTest.interactiveTest()
        break
    default:
        println "Неверный выбор. Запускаем все тесты..."
        VoiceAssistantPatternsTest.runAllTests()
}
