import pytest
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = 'https://www.demoblaze.com'

# Вредоносные коды для проверки на уязвимость
SQL_PAYLOADS = [
    ("' OR '1'='1", "Классическая инъекция (всегда истина)"),
    ("' OR 1=1 --", "Комментарий после условия"),
    ("admin'--", "Обход пароля через комментарий"),
]

# Словарные и слишком простые пароли
WEAK_PASSWORDS = [
    ('123', 'Слишком короткий (3 символа)'),
    ('password', 'Распространённый словарный пароль'),
]

def test_sql_injection_login(driver):
    """SEC-01: Проверка устойчивости формы к SQL-инъекциям."""
    driver.get(BASE)
    results = []
    
    for payload, desc in SQL_PAYLOADS:
        driver.find_element(By.ID, 'login2').click()
        WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located((By.ID, 'loginusername')))
        
        driver.find_element(By.ID, 'loginusername').clear()
        driver.find_element(By.ID, 'loginusername').send_keys(payload)
        driver.find_element(By.ID, 'loginpassword').clear()
        driver.find_element(By.ID, 'loginpassword').send_keys('anypassword')
        driver.find_element(By.XPATH, "//button[text()='Log in']").click()
        
        time.sleep(1.5)
        
        # Проверяем, пустил ли нас сайт (появилась ли кнопка выхода Logout)
        logout_visible = len(driver.find_elements(By.ID, 'logout2')) > 0
        status = 'УЯЗВИМ' if logout_visible else 'ЗАЩИЩЁН'
        results.append((payload, desc, status))
        
        # Автоматически сохраняем скриншот попытки в папку report
        driver.save_screenshot(f'report/sec_01_{len(results)}.png')
        
        # Закрываем системные окна, если они вылезли
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
        except:
            pass
            
        try:
            close_btn = driver.find_element(By.XPATH, "(//button[text()='Close'])[3]")
            if close_btn.is_displayed():
                close_btn.click()
                time.sleep(0.5)
        except:
            pass

    print('\n=== SEC-01: Результаты SQL-инъекций ===')
    for p, d, s in results:
        print(f' {s:10s} | {d:40s} | {repr(p)}')
    
    assert all(r[2] == 'ЗАЩИЩЁН' for r in results), 'КРИТИЧНО: SQL-инъекция пустила в систему!'

def test_weak_password_registration(driver):
    """SEC-02: Проверка политики прочности паролей при регистрации."""
    driver.get(BASE)
    results = []
    
    for pwd, desc in WEAK_PASSWORDS:
        username = f'stud_user_{int(time.time())}'  # генерируем уникальный логин
        driver.find_element(By.ID, 'signin2').click()
        WebDriverWait(driver, 8).until(
            EC.visibility_of_element_located((By.ID, 'sign-username')))
        
        driver.find_element(By.ID, 'sign-username').clear()
        driver.find_element(By.ID, 'sign-username').send_keys(username)
        driver.find_element(By.ID, 'sign-password').clear()
        driver.find_element(By.ID, 'sign-password').send_keys(pwd)
        driver.find_element(By.XPATH, "//button[text()='Sign up']").click()
        
        time.sleep(1.5)
        
        try:
            alert = WebDriverWait(driver, 4).until(EC.alert_is_present())
            msg = alert.text
            alert.accept()
            accepted = 'successful' in msg.lower()
        except:
            accepted = False
            
        status = 'УЯЗВИМ (принят)' if accepted else 'OK (отклонён)'
        results.append((pwd, desc, status))
        driver.save_screenshot(f'report/sec_02_{len(results)}.png')
        
        try:
            close_btn = driver.find_element(By.XPATH, "(//button[text()='Close'])[2]")
            if close_btn.is_displayed():
                close_btn.click()
                time.sleep(0.5)
        except:
            pass

    print('\n=== SEC-02: Политика паролей ===')
    for pw, d, s in results:
        print(f' {s:20s} | {d}')

def test_security_headers():
    """SEC-03: Анализ наличия защитных HTTP-заголовков безопасности."""
    assert BASE.startswith('https://'), 'Сайт работает без SSL!'
    r = requests.get(BASE, timeout=10)
    
    print('\n=== SEC-03: Заголовки безопасности ===')
    headers_to_check = ['X-Frame-Options', 'X-Content-Type-Options', 'Strict-Transport-Security']
    
    for h in headers_to_check:
        val = r.headers.get(h, None)
        status = f'[OK] {val}' if val else '[ОТСУТСТВУЕТ]'
        print(f' {h:25s}: {status}')