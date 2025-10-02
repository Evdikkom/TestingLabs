import pytest
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from contact_page import ContactPage

class TestOrderForm:
    @pytest.fixture(autouse=True)
    def setup(self):
        #Пути к браузеру и драйверу
        yandex_browser_path = "C:\\Users\\Евдик\\AppData\\Local\\Yandex\\YandexBrowser\\Application\\browser.exe"
        yandex_driver_path = "C:\\Users\\Евдик\\AppData\\Local\\Yandex\\YandexBrowser\\Application\\yandexdriver.exe"
        
        #Проверяем существование файлов
        if not os.path.exists(yandex_browser_path):
            self._print_result("Яндекс.Браузер не найден", "ERROR")
            pytest.skip("Яндекс.Браузер не найден")
        if not os.path.exists(yandex_driver_path):
            self._print_result("YandexDriver не найден", "ERROR")
            pytest.skip("YandexDriver не найден")
        
        #Настройка опций
        options = Options()
        options.binary_location = yandex_browser_path
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        #Инициализация драйвера
        service = Service(executable_path=yandex_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        
        #Установка размера окна
        try:
            self.driver.maximize_window()
        except WebDriverException:
            self.driver.set_window_size(1920, 1080)
        
        #Инициализация Page Object
        self.contact_page = ContactPage(self.driver)
        self.contact_page.open("http://localhost:5000/order")
        
        yield
        self.driver.quit()

    def _print_result(self, message, status="INFO"):
        print(f"\n{status}: {message}", file=sys.stderr)
        sys.stderr.flush()

    def test_positive_scenario_valid_data(self):
        """Позитивный тест: заполнение всех полей формы валидными данными"""
        #Заполнение формы
        self.contact_page.set_name("Иван Иванов")
        self.contact_page.set_email("ivan@example.com")
        self.contact_page.set_phone("+79161234567")
        self.contact_page.set_address("ул. Примерная, д. 1, кв. 1")
        self.contact_page.set_comment("Доставка после 18:00")
        
        #Отправка формы
        self.contact_page.submit_form()
        
        #Проверка успешного сообщения
        assert self.contact_page.is_success_message_displayed()
        assert "успешно" in self.contact_page.get_success_message().lower()
        
        self._print_result("Позитивный сценарий: УСПЕШНО", "SUCCESS")

    def test_negative_scenario_empty_required_field(self):
        """Негативный тест: попытка отправить форму с пустым обязательным полем"""
        #Заполнение всех полей, кроме имени
        self.contact_page.set_email("ivan@example.com")
        self.contact_page.set_phone("+79161234567")
        self.contact_page.set_address("ул. Примерная, д. 1, кв. 1")
        
        #Отправка формы
        self.contact_page.submit_form()
        
        #Проверка сообщения об ошибке
        assert self.contact_page.is_error_message_displayed() or self.contact_page.get_field_error("name") != ""
        error_text = self.contact_page.get_error_message() if self.contact_page.is_error_message_displayed() else self.contact_page.get_field_error("name")
        assert "обязательно" in error_text.lower() or "заполните" in error_text.lower()
        
        self._print_result("Негативный сценарий (пустое поле): ОЖИДАЕМАЯ ОШИБКА", "INFO")

    def test_negative_scenario_invalid_email(self):
        """Негативный тест: невалидный email"""
        #Заполнение формы с невалидным email
        self.contact_page.set_name("Евдокимов Артемий")
        self.contact_page.set_email("evdikkommail.ru")
        self.contact_page.set_phone("+79161234567")
        self.contact_page.set_address("ул. Первомайская, д. 1, кв. 1")
        
        #Отправка формы
        self.contact_page.submit_form()
        
        #Проверка сообщения об ошибке
        assert self.contact_page.is_error_message_displayed() or self.contact_page.get_field_error("email") != ""
        error_text = self.contact_page.get_error_message() if self.contact_page.is_error_message_displayed() else self.contact_page.get_field_error("email")
        assert "email" in error_text.lower() or "электронная почта" in error_text.lower()
        
        self._print_result("Негативный сценарий (невалидный email): ОЖИДАЕМАЯ ОШИБКА", "INFO")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])