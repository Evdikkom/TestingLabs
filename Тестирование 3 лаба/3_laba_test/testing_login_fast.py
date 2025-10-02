import pytest
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

class TestFlaskLogin:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Пути к браузеру и драйверу
        yandex_browser_path = "C:\\Users\\Евдик\\AppData\\Local\\Yandex\\YandexBrowser\\Application\\browser.exe"
        yandex_driver_path = "C:\\Users\\Евдик\\AppData\\Local\\Yandex\\YandexBrowser\\Application\\yandexdriver.exe"
        
        # Проверяем существование файлов
        if not os.path.exists(yandex_browser_path):
            self._print_result("Яндекс.Браузер не найден", "ERROR")
            pytest.skip("Яндекс.Браузер не найден")
        if not os.path.exists(yandex_driver_path):
            self._print_result("YandexDriver не найден", "ERROR")
            pytest.skip("YandexDriver не найден")
        
        # Настройка опций
        options = Options()
        options.binary_location = yandex_browser_path
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        # Инициализация драйвера
        service = Service(executable_path=yandex_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Установка размера окна
        try:
            self.driver.maximize_window()
        except WebDriverException:
            self.driver.set_window_size(1920, 1080)
        
        # Открытие страницы
        self.driver.get("http://localhost:5000/login")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        yield
        self.driver.quit()

    def _print_result(self, message, status="INFO"):
        """Вспомогательная функция для вывода результатов"""
        # Выводим напрямую в stderr, чтобы обойти перехват pytest
        print(f"\n{status}: {message}", file=sys.stderr)
        sys.stderr.flush()

    def test_successful_login(self):
        """Тест успешного входа в систему"""
        # Ввод данных
        login_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите логин']"))
        )
        login_field.clear()
        login_field.send_keys("a.r.evdokimov")
        
        password_field = self.driver.find_element(By.XPATH, "//input[@placeholder='Введите пароль']")
        password_field.clear()
        password_field.send_keys("Vfksi123") 
        
        # Нажатие кнопки входа
        login_button = self.driver.find_element(By.XPATH, "//button[text()='Вход']")
        login_button.click()
        
        # Проверка успешного входа
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Главная страница')]"))
        )
        
        # Проверка имени пользователя
        user_name = self.driver.find_element(By.XPATH, "//strong[contains(text(), 'А.Р. Евдокимов')]")
        assert user_name.is_displayed()
        
        # Вывод результата
        self._print_result("Авторизация: УСПЕШНО", "SUCCESS")

    def test_login_with_invalid_credentials(self):
        """Тест входа с неверными учетными данными"""
        # Переход на страницу входа
        self.driver.get("http://localhost:5000/login")
        
        # Ввод неверных данных
        login_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите логин']"))
        )
        login_field.clear()
        login_field.send_keys("invalid_login")
        
        password_field = self.driver.find_element(By.XPATH, "//input[@placeholder='Введите пароль']")
        password_field.clear()
        password_field.send_keys("invalid_password")
        
        # Нажатие кнопки входа
        login_button = self.driver.find_element(By.XPATH, "//button[text()='Вход']")
        login_button.click()
        
        # Проверка сообщения об ошибке
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "error-message"))
        )
        assert "Неверные учетные данные" in error_message.text
        
        # Вывод результата
        self._print_result("Авторизация с неверными данными: ОЖИДАЕМАЯ НЕУДАЧА", "INFO")

if __name__ == "__main__":
    # Запускаем тесты с выводом в консоль
    pytest.main([__file__, "-v", "-s"])