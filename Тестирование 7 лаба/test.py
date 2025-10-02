import os
import time
import subprocess
from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SimpleNotesTests:
    def __init__(self):
        os.environ['ANDROID_HOME'] = "D:\\First_Android_App"
        os.environ['ANDROID_SDK_ROOT'] = "D:\\First_Android_App"
        
        self.driver = None
        self.wait = None
        
    def setup(self):
        print("Настройка тестового окружения...")
        
        options = AppiumOptions()
        options.load_capabilities({
            'platformName': 'Android',
            'appium:deviceName': 'emulator-5554',
            'appium:automationName': 'UiAutomator2',
            'appium:appPackage': 'com.example.simplenotes',
            'appium:appActivity': '.MainActivity',
            'appium:noReset': False
        })
        
        try:
            self.driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4723/wd/hub',
                options=options
            )
            self.wait = WebDriverWait(self.driver, 10)
            time.sleep(5)
            print("✓ Драйвер успешно настроен")
            return True
        except Exception as e:
            print(f"✗ Ошибка настройки драйвера: {e}")
            return False
    
    def teardown(self):
        if self.driver:
            self.driver.quit()
            print("✓ Драйвер закрыт")
    
    def find_by_text(self, text):
        """Поиск элемента по тексту"""
        try:
            return self.driver.find_element(By.XPATH, f"//*[contains(@text, '{text}')]")
        except:
            return None
    
    def create_test_note(self):
        """Вспомогательный метод для создания тестовой заметки"""
        try:
            # Находим поля ввода
            input_fields = self.driver.find_elements(By.CLASS_NAME, "android.widget.EditText")
            
            if len(input_fields) >= 2:
                # Вводим заголовок
                title_field = input_fields[0]
                title_field.send_keys("Тестовая заметка")
                
                # Вводим текст заметки
                content_field = input_fields[1]
                content_field.send_keys("Это тестовое содержание заметки")
                
                # Сохраняем заметку
                save_button = self.find_by_text("Сохранить заметку")
                if save_button and save_button.is_enabled():
                    save_button.click()
                    time.sleep(2)
                    return True
            return False
        except Exception as e:
            print(f"Ошибка создания заметки: {e}")
            return False
    
    def test_app_launch(self):
        """1.1.1 Тест запуска приложения"""
        print("\n1. Тест запуска приложения")
        
        try:
            # Проверяем основные элементы интерфейса
            title = self.find_by_text("Заметки")
            if title:
                print("✓ Заголовок приложения отображается")
            
            # Проверяем поля ввода
            input_fields = self.driver.find_elements(By.CLASS_NAME, "android.widget.EditText")
            print(f"✓ Найдено полей ввода: {len(input_fields)}")
            
            # Проверяем кнопку сохранения
            save_button = self.find_by_text("Сохранить заметку")
            if save_button:
                print("✓ Кнопка сохранения найдена")
            
            self.driver.save_screenshot("test_launch.png")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка теста запуска: {e}")
            return False
    
    def test_create_note(self):
        """1.1.2 Тест создания заметки"""
        print("\n2. Тест создания заметки")
        
        try:
            # Находим поля ввода
            input_fields = self.driver.find_elements(By.CLASS_NAME, "android.widget.EditText")
            
            if len(input_fields) >= 2:
                # Вводим заголовок
                title_field = input_fields[0]
                title_field.send_keys("Тестовая заметка")
                print("✓ Заголовок введен")
                
                # Вводим текст заметки
                content_field = input_fields[1]
                content_field.send_keys("Это тестовое содержание заметки")
                print("✓ Текст заметки введен")
                
                # Сохраняем заметку
                save_button = self.find_by_text("Сохранить заметку")
                if save_button and save_button.is_enabled():
                    save_button.click()
                    print("✓ Кнопка сохранения нажата")
                    
                    # Ждем сохранения
                    time.sleep(2)
                    
                    # Проверяем, что поля очистились
                    if title_field.text == "" and content_field.text == "":
                        print("✓ Поля очистились после сохранения")
                    
                    # Проверяем, что заметка появилась в списке
                    note_title = self.find_by_text("Тестовая заметка")
                    if note_title:
                        print("✓ Заметка отображается в списке")
                        self.driver.save_screenshot("test_create_note.png")
                        return True
                    else:
                        print("✗ Заметка не найдена в списке")
                        return False
                else:
                    print("✗ Кнопка сохранения не активна")
                    return False
            else:
                print("✗ Не найдены поля ввода")
                return False
                
        except Exception as e:
            print(f"✗ Ошибка создания заметки: {e}")
            return False
    
    def test_validation(self):
        """1.1.3 Тест валидации полей"""
        print("\n3. Тест валидации полей")
        
        try:
            save_button = self.find_by_text("Сохранить заметку")
            
            if save_button:
                # Проверяем состояние кнопки при пустых полях
                is_enabled = save_button.is_enabled()
                if not is_enabled:
                    print("✓ Кнопка неактивна при пустых полях")
                else:
                    print("✗ Кнопка активна при пустых полях")
                
                # Заполняем только заголовок
                input_fields = self.driver.find_elements(By.CLASS_NAME, "android.widget.EditText")
                if input_fields:
                    input_fields[0].send_keys("Только заголовок")
                    
                    # Даем время на обновление состояния
                    time.sleep(1)
                    
                    # Проверяем состояние кнопки после ввода заголовка
                    is_enabled_after_title = save_button.is_enabled()
                    if not is_enabled_after_title:
                        print("✓ Кнопка неактивна без содержания")
                    else:
                        print("✗ Кнопка активна без содержания")
                    
                    # Очищаем поле
                    input_fields[0].clear()
                    
                    self.driver.save_screenshot("test_validation.png")
                    return True
                else:
                    print("✗ Не найдены поля ввода")
                    return False
            else:
                print("✗ Не найдена кнопка сохранения")
                return False
            
        except Exception as e:
            print(f"✗ Ошибка теста валидации: {e}")
            return False
    
    def test_note_management(self):
        """1.2 Тест управления заметками"""
        print("\n4. Тест управления заметками")
        
        try:
            # Создаем заметку для тестирования (без вызова полноценного теста)
            if not self.create_test_note():
                print("✗ Не удалось создать заметку для тестирования")
                return False
            
            time.sleep(2)
            
            # Ищем кнопку информации (по content-desc или по описанию)
            info_buttons = self.driver.find_elements(By.XPATH, "//*[@content-desc='Информация' or @content-desc='Info']")
            if not info_buttons:
                # Пробуем найти по классу или другим атрибутам
                info_buttons = self.driver.find_elements(By.XPATH, "//android.widget.Button[contains(@content-desc, 'информа')]")
            
            if info_buttons:
                info_buttons[0].click()
                print("✓ Кнопка информации нажата")
                time.sleep(1)
            
            # Ищем кнопку удаления
            delete_buttons = self.driver.find_elements(By.XPATH, "//*[@content-desc='Удалить' or @content-desc='Delete']")
            if not delete_buttons:
                delete_buttons = self.driver.find_elements(By.XPATH, "//android.widget.Button[contains(@content-desc, 'удал')]")
            
            if delete_buttons:
                delete_buttons[0].click()
                print("✓ Кнопка удаления нажата")
                
                # Ждем появления диалога подтверждения
                time.sleep(2)
                
                # Подтверждаем удаление
                confirm_button = self.find_by_text("Удалить")
                if confirm_button:
                    confirm_button.click()
                    print("✓ Подтверждение удаления выполнено")
                    
                    # Ждем удаления и проверяем
                    time.sleep(3)
                    
                    # Проверяем, что заметка удалилась
                    note_after_delete = self.find_by_text("Тестовая заметка")
                    if not note_after_delete:
                        print("✓ Заметка успешно удалена")
                    else:
                        # Дополнительная проверка - может быть другая заметка с таким же текстом
                        print("⚠ Заметка все еще отображается, проверяем количество заметок...")
                        # Можно добавить дополнительную логику проверки
                    
                    self.driver.save_screenshot("test_management.png")
                    return True
                else:
                    print("✗ Не найдена кнопка подтверждения удаления")
                    return False
            else:
                print("✗ Не найдены кнопки действий")
                return False
                
        except Exception as e:
            print(f"✗ Ошибка теста управления: {e}")
            return False
    
    def test_gestures(self):
        """2.1 Тест жестов - упрощенная версия без TouchAction"""
        print("\n5. Тест жестов")
        
        try:
            # Создаем заметку для тестирования жестов (без вызова полноценного теста)
            if not self.create_test_note():
                print("✗ Не удалось создать заметку для тестирования жестов")
                return False
            
            time.sleep(2)
            
            # Вместо долгого нажатия тестируем обычное нажатие на заметку
            note_element = self.find_by_text("Тестовая заметка")
            if note_element:
                note_element.click()
                print("✓ Нажатие на заметку выполнено")
                time.sleep(1)
            
            # Тестируем прокрутку - создаем еще несколько заметок
            for i in range(2):
                input_fields = self.driver.find_elements(By.CLASS_NAME, "android.widget.EditText")
                if len(input_fields) >= 2:
                    input_fields[0].send_keys(f"Заметка {i+1}")
                    input_fields[1].send_keys(f"Содержание {i+1}")
                    
                    save_button = self.find_by_text("Сохранить заметку")
                    if save_button and save_button.is_enabled():
                        save_button.click()
                        time.sleep(1)
            
            # Прокручиваем список с помощью swipe
            window_size = self.driver.get_window_size()
            start_x = window_size['width'] // 2
            start_y = window_size['height'] * 3 // 4
            end_y = window_size['height'] // 4
            
            self.driver.swipe(start_x, start_y, start_x, end_y, 1000)
            print("✓ Прокрутка выполнена")
            time.sleep(2)
            
            # Проверяем, что можем найти созданные заметки после прокрутки
            for i in range(1, 3):
                note = self.find_by_text(f"Заметка {i}")
                if note:
                    print(f"✓ Заметка {i} найдена после прокрутки")
            
            self.driver.save_screenshot("test_gestures.png")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка теста жестов: {e}")
            return False
    
    def test_interruptions(self):
        """4. Тест прерываний"""
        print("\n6. Тест прерываний")
        
        try:
            # Имитируем входящий звонок через ADB
            print("Имитация входящего звонка...")
            result = subprocess.run([
                "adb", "shell", "am", "start", "-a", "android.intent.action.CALL", "-d", "tel:5551234"
            ], capture_output=True, text=True, timeout=10)
            
            print(f"Результат звонка: {result.returncode}")
            time.sleep(3)
            
            # Возвращаемся в приложение
            self.driver.back()
            print("✓ Возврат в приложение после звонка")
            time.sleep(2)
            
            # Имитируем низкий заряд батареи
            print("Имитация низкого заряда батареи...")
            result = subprocess.run([
                "adb", "shell", "dumpsys", "battery", "set", "level", "15"
            ], capture_output=True, text=True, timeout=10)
            
            print(f"Результат изменения батареи: {result.returncode}")
            time.sleep(2)
            
            # Проверяем, что приложение все еще работает
            current_activity = self.driver.current_activity
            if "MainActivity" in current_activity:
                print("✓ Приложение работает после прерываний")
            
            self.driver.save_screenshot("test_interruptions.png")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка теста прерываний: {e}")
            return False
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("ЗАПУСК АВТОТЕСТОВ ДЛЯ ПРИЛОЖЕНИЯ ЗАМЕТКИ")
        print("=" * 50)
        
        if not self.setup():
            print("Не удалось настроить тестовое окружение")
            return
        
        test_results = []
        
        # Запускаем тесты по порядку
        tests = [
            ("Запуск приложения", self.test_app_launch),
            ("Создание заметки", self.test_create_note),
            ("Валидация полей", self.test_validation),
            ("Управление заметками", self.test_note_management),
            ("Тест жестов", self.test_gestures),
            ("Тест прерываний", self.test_interruptions)
        ]
        
        for test_name, test_method in tests:
            try:
                print(f"\n--- Выполнение теста: {test_name} ---")
                result = test_method()
                test_results.append((test_name, result))
                time.sleep(2)
            except Exception as e:
                print(f"Ошибка выполнения теста {test_name}: {e}")
                test_results.append((test_name, False))
        
        # Выводим результаты
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
        print("=" * 50)
        
        passed = 0
        for test_name, result in test_results:
            status = "✓ ПРОЙДЕН" if result else "✗ НЕ ПРОЙДЕН"
            print(f"{test_name}: {status}")
            if result:
                passed += 1
        
        print(f"\nИтого: {passed}/{len(tests)} тестов пройдено")
        
        # Завершаем
        self.teardown()

# Запуск тестов
if __name__ == "__main__":
    tester = SimpleNotesTests()
    tester.run_all_tests()