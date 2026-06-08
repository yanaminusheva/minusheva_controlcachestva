print("=== СТАРТ АВТОМАТИЗИРОВАННЫХ PYTHON-ПРОВЕРОК ===")

def calculate_logic(expression):
    try:
        # Если в запущенную программу ввести буквы, она возвращает 0
        if any(c.isalpha() for c in expression):
            return 0
        
        # Вычисление строкового выражения
        result = eval(expression)
        return result
    except ZeroDivisionError:
        return "Error"
    except Exception:
        return "Системная ошибка"

# Тест 1: Позитивный сценарий
print("Запуск автотеста: Сложение целых чисел...")
assert calculate_logic("15 + 27") == 42
print("[PASSED] Тест сложения успешно пройден. Получено целое число.")

# Тест 2: Проверка дефекта форматирования целых чисел
print("\nЗапуск автотеста: Проверка формата вывода деления (Ожидалось целое 10)...")
actual_result = calculate_logic("50 / 5")

try:
    assert type(actual_result) == int, f"UI-дефект! Ожидалось целое число (int), но получено вещественное {actual_result} (float)"
    print("[PASSED] Результат соответствует формату целого числа.")
except AssertionError as e:
    print(f"[FAILED] {e}")

# Тест 3: Проверка обработки деления на ноль
print("\nЗапуск автотеста: Перехват ZeroDivisionError...")
test_zero = calculate_logic("10 / 0")
assert test_zero == "Error", f"Ожидался вывод Error, но получено: {test_zero}"
print("[PASSED] Тест перехвата деления на ноль успешно подтвержден.")

# Тест 4: Проверка обработки букв
print("\nЗапуск автотеста: Валидация текста...")
actual_text_result = calculate_logic("abc")

try:
    # Мы ожидаем, что буквы вообще НЕ должны обрабатываться
    # Если тест видит, что калькулятор принял буквы  — это баг!
    assert actual_text_result == "Ошибка ввода", "Критический баг валидации! Калькулятор не заблокировал буквы"
    print("[PASSED] Тест защиты от текстового ввода успешно подтвержден.")
except AssertionError as e:
    print(f"[FAILED] {e}")

print("\n=== ВСЕ PYTHON-ТЕСТЫ УСПЕШНО ЗАВЕРШЕНЫ ===")