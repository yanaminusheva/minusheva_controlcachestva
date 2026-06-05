import requests

print("=== СТАРТ МИНИМАЛЬНОЙ АВТОМАТИЗАЦИИ ===")

# 1. Автотест функции
def add(a, b):
    return a + b

print("Запуск автотеста функции add...")
assert add(2, 2) == 4
assert add(15, 27) == 42
print("[PASSED] Функция add(a, b) работает корректно.")

# 2. Проверка API через requests
print("\nЗапуск проверки API через requests...")
response = requests.get("https://api.mathjs.org/v4/?expr=5%2B5")

assert response.status_code == 200
print("[PASSED] Статус ответа сервера: 200 OK")

assert response.text == "10"
print("[PASSED] Тело ответа совпадает с ожидаемым (5 + 5 = 10)")

print("\n=== ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ ===")