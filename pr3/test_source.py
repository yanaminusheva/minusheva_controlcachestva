import pytest
from source import validate_password, safe_divide

# =====================================================================
# ТЕСТЫ ДЛЯ ВАРИАНТА A: ВАЛИДАЦИЯ ПАРОЛЯ
# =====================================================================

@pytest.mark.parametrize("password, expected", [
    ("Pass1234", True),         # TC-A1: Позитивный сценарий
    ("P1abcdef", True),         # TC-A6: Граничный тест (ровно 8 символов)
    ("Valid2026Secure", True)   # Дополнительный длинный пароль
])
def test_validate_password_positive(password, expected):
    """Тестирование корректных паролей, удовлетворяющих всем условиям"""
    assert validate_password(password) == expected


@pytest.mark.parametrize("password", [
    "A1b",        # TC-A2: Граничный тест — длина меньше 8 символов
    "Abcdefgh",   # TC-A3: Негативный тест — отсутствует обязательная цифра
    "12345678",   # TC-A4: Негативный тест — отсутствует обязательная буква
    "Pass 1234"   # TC-A5: Негативный тест — строка содержит запрещенный пробел
])
def test_validate_password_negative(password):
    """Тестирование некорректных паролей (должны возвращать False)"""
    assert validate_password(password) is False


def test_validate_password_type_error():
    """TC-A7: Тест на передачу некорректного типа данных в валидатор"""
    with pytest.raises(TypeError):
        validate_password(12345678)


# =====================================================================
# ТЕСТЫ ДЛЯ ВАРИАНТА B: ДЕЛЕНИЕ ЧИСЕЛ
# =====================================================================

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0),       # TC-B1: Позитивный тест — деление целых чисел нацело
    (5.5, 2.0, 2.75),   # TC-B2: Позитивный тест — деление чисел с плавающей точкой
    (0, 5, 0.0),        # TC-B4: Граничный тест — ноль в числителе
    (-15, 3, -5.0)      # Дополнительный тест с отрицательным числом
])
def test_safe_divide_positive(a, b, expected):
    """Тестирование штатных математических операций деления"""
    assert safe_divide(a, b) == expected


def test_safe_divide_zero_division():
    """TC-B3: Тест на генерацию исключения при делении на 0"""
    with pytest.raises(ZeroDivisionError) as exc_info:
        safe_divide(10, 0)
    assert "Деление на ноль недопустимо" in str(exc_info.value)


@pytest.mark.parametrize("a, b", [
    ("10", 2),  # TC-B5: Тест на ошибочные данные — строка вместо числа в 'a'
    (10, "2"),  # Ошибочные данные — строка вместо числа в 'b'
    ([5], 2)    # Ошибочные данные — список объектов вместо числа
])
def test_safe_divide_type_error(a, b):
    """Тест на генерацию TypeError при передаче невалидных типов данных"""
    with pytest.raises(TypeError):
        safe_divide(a, b)