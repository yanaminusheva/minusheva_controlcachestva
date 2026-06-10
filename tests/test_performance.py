import requests
import time
import statistics
import pytest

BASE = 'https://www.demoblaze.com'
REPEAT = 10 

# Проверяем главную страницу и файл конфигурации
ENDPOINTS = [
    ('/', 'Главная страница'),
    ('/config.json', 'Конфигурация'),
]

def measure(url, n=REPEAT):
    """Выполняет n запросов и собирает чистую статистику времени отклика."""
    times = []
    sizes = []
    statuses = []
    for _ in range(n):
        t0 = time.perf_counter()
        r = requests.get(url, timeout=15)
        elapsed = (time.perf_counter() - t0) * 1000  # Переводим в миллисекунды (мс)
        times.append(elapsed)
        sizes.append(len(r.content))
        statuses.append(r.status_code)
    return {
        'min': round(min(times), 1),
        'max': round(max(times), 1),
        'mean': round(statistics.mean(times), 1),
        'median': round(statistics.median(times), 1),
        'p95': round(sorted(times)[int(n*0.95)] if n > 1 else times[0], 1),
        'size_kb': round(statistics.mean(sizes)/1024, 1),
        'errors': statuses.count(200) - n
    }

def test_homepage_latency():
    """PERF-01: Замер latency главной страницы (10 запросов)."""
    stats = measure(BASE + '/')
    print(f'\nGET / → mean={stats["mean"]}мс p95={stats["p95"]}мс size={stats["size_kb"]}кб')
    assert stats['mean'] < 2000, f'Среднее время {stats["mean"]}мс превышает лимит!'

def test_all_endpoints_latency():
    """PERF-02: Сравнительный замер эндпоинтов."""
    print()
    for path, name in ENDPOINTS:
        try:
            s = measure(BASE + path, n=5)
            print(f'{name:25s} | mean={s["mean"]:7.1f}мс | p95={s["p95"]:7.1f}мс | {s["size_kb"]}кб')
        except Exception as e:
            print(f'{name:25s} | ОШИБКА: {e}')

def test_response_headers_analysis():
    """PERF-03: Анализ служебных заголовков ответа."""
    r = requests.get(BASE + '/', timeout=10)
    headers = r.headers
    print('\n=== Заголовки HTTP-ответа ===')
    for key in ['Content-Type', 'Content-Length', 'Content-Encoding', 'Cache-Control', 'Connection', 'Server']:
        val = headers.get(key, '(отсутствует)')
        print(f' {key}: {val}')