from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import time
import unittest
import subprocess
import requests

class TestNotesAppV1(unittest.TestCase):
    """
    Тесты для Appium 1.22.3
    """
    
    def setUp(self):
        print(f"🎬 Подготовка к тесту: {self._testMethodName}")
        
        # Desired Capabilities для Appium 1.x
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '11.0',  # Укажите вашу версию Android
            'deviceName': 'emulator-5554',
            'appPackage': 'com.example.simplenotes',
            'appActivity': '.MainActivity',
            'automationName': 'UiAutomator2',
            'noReset': True,
            'newCommandTimeout': 60
        }
        
        try:
            # Подключаемся к Appium 1.x
            self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
            self.driver.implicitly_wait(10)
            print("✅ Успешное подключение к Appium 1.22.3!")
        except Exception as e:
            self.fail(f"❌ Не удалось подключиться: {e}")
    
    def test_01_simple_button_tap(self):
        """ПРОСТОЙ ТЕСТ: Тап по кнопке"""
        print("👆 ТЕСТ: Тап по кнопке")
        
        try:
            # Ждем загрузки приложения
            time.sleep(5)
            
            # Делаем скриншот ДО
            self.driver.save_screenshot("before_test.png")
            print("✅ Скриншот ДО: before_test.png")
            
            # Пробуем разные селекторы для кнопки
            button_selectors = [
                "//android.widget.Button[@text='Сохранить заметку']",
                "//*[@text='Сохранить заметку']",
                "//*[contains(@text, 'Сохранить')]",
                "//android.widget.Button"
            ]
            
            save_button = None
            for selector in button_selectors:
                try:
                    elements = self.driver.find_elements(AppiumBy.XPATH, selector)
                    if elements:
                        save_button = elements[0]
                        print(f"✅ Найден элемент с селектором: {selector}")
                        break
                except:
                    continue
            
            if save_button:
                # ТАП ПО КНОПКЕ!
                save_button.click()
                print("🎉 УСПЕХ: ТАП ПО КНОПКЕ ВЫПОЛНЕН!")
                
                # Скриншот ПОСЛЕ
                time.sleep(2)
                self.driver.save_screenshot("after_test.png")
                print("✅ Скриншот ПОСЛЕ: after_test.png")
            else:
                # Если кнопка не найдена, просто делаем тап по координатам
                print("⚠ Кнопка не найдена, делаем тап по координатам")
                self.driver.tap([(500, 500)], 100)
                print("🎉 ТАП ВЫПОЛНЕН ПО КООРДИНАТАМ!")
                
        except Exception as e:
            self.fail(f"❌ Ошибка: {e}")
    
    def test_02_app_elements(self):
        """Поиск элементов приложения"""
        print("🔍 Поиск элементов")
        
        time.sleep(3)
        
        # Сохраняем структуру страницы для отладки
        page_source = self.driver.page_source
        with open("page_layout.xml", "w", encoding="utf-8") as f:
            f.write(page_source)
        print("✅ Структура страницы сохранена в page_layout.xml")
        
        # Ищем элементы
        elements_to_find = [
            "Заметки",
            "Заголовок заметки",
            "Текст заметки",
            "Сохранить заметку"
        ]
        
        found_elements = []
        for element_text in elements_to_find:
            try:
                elements = self.driver.find_elements(AppiumBy.XPATH, f"//*[contains(@text, '{element_text}')]")
                if elements:
                    print(f"✅ Найден: {element_text}")
                    found_elements.append(element_text)
                else:
                    print(f"❌ Не найден: {element_text}")
            except Exception as e:
                print(f"⚠ Ошибка поиска {element_text}: {e}")
        
        print(f"📊 Итого найдено: {len(found_elements)}/{len(elements_to_find)}")
        
    def tearDown(self):
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except:
                pass
        print(f"✅ Тест завершен: {self._testMethodName}\n")

def check_appium_v1():
    """Проверка окружения для Appium 1.x"""
    print("🔍 ПРОВЕРКА ОКРУЖЕНИЯ ДЛЯ APPIUM 1.22.3")
    print("=" * 50)
    
    # Проверяем Appium
    try:
        result = subprocess.run(["npx", "appium", "--version"], capture_output=True, text=True, timeout=5)
        print(f"✅ Appium версия: {result.stdout.strip()}")
    except:
        print("❌ Appium не найден")
        return False
    
    # Проверяем эмулятор
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=5)
        if "device" in result.stdout:
            print("✅ Эмулятор запущен")
            # Выводим список устройств
            for line in result.stdout.strip().split('\n'):
                if 'device' in line and 'List' not in line:
                    print(f"   📱 Устройство: {line}")
        else:
            print("❌ Эмулятор не найден")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки ADB: {e}")
        return False
    
    # Проверяем доступность Appium Server
    try:
        response = requests.get('http://127.0.0.1:4723/wd/hub/status', timeout=5)
        if response.status_code == 200:
            print("✅ Appium Server доступен")
            return True
        else:
            print(f"❌ Appium Server недоступен, код: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Не удалось подключиться к Appium Server: {e}")
        print("   Убедитесь, что Appium запущен: npx appium")
        return False

if __name__ == '__main__':
    print("🚀 АВТОМАТИЧЕСКИЕ ТЕСТЫ ДЛЯ APPIUM 1.22.3")
    print("=" * 60)
    
    if check_appium_v1():
        print("\n🎯 ЗАПУСК ТЕСТОВ...")
        unittest.main(verbosity=2)
    else:
        print("\n❌ Настройте окружение перед запуском тестов")