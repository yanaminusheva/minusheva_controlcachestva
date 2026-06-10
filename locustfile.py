from locust import HttpUser, task, between

class ShopUser(HttpUser):
    # Имитируем поведение человека: пауза между кликами от 1 до 3 секунд
    wait_time = between(1, 3)
    host = 'https://www.demoblaze.com'

    @task(3)
    def view_homepage(self):
        """Пользователь заходит на главную страницу."""
        with self.client.get('/', catch_response=True) as r:
            if r.status_code != 200:
                r.failure(f'Главная: ожидался 200, получен {r.status_code}')

    @task(1)
    def view_config(self):
        """Пользователь подгружает конфигурацию."""
        self.client.get('/config.json')