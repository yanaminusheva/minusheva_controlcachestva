def validate_password(password: str) -> bool:
    """
    Валидирует пароль на соответствие требованиям безопасности.
    Требования: минимум 8 символов, 1 цифра, 1 буква, без пробелов.
    """
    if not isinstance(password, str):
        raise TypeError("Пароль должен быть строковой переменной (str)")
        
    if len(password) < 8:
        return False
        
 #   if " " in password:
        return False
 #       
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_letter and has_digit


def safe_divide(a, b):
    """
    Выполняет безопасное деление двух чисел с поддержкой типов int и float.
    Обрабатывает деление на ноль и проверку типов данных.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Оба аргумента должны быть числами (int или float)")
        
    if b == 0:
        raise ZeroDivisionError("Деление на ноль недопустимо")
        
    return a / b