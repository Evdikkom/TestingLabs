import pytest
import requests
import sys

BASE_URL = "https://reqres.in/api"

class TestReqResAPI:
    """Тесты для API reqres.in с использованием pytest и requests"""
    
    def _print_result(self, message, status="INFO"):
        """Вывод результата в stderr"""
        print(f"\n{status}: {message}", file=sys.stderr)
        sys.stderr.flush()
    
    @pytest.fixture
    def api_headers(self):
        """Фикстура с заголовками для API запросов"""
        self._print_result("Подготавливаем заголовки для API запросов")
        return {
            "x-api-key": "reqres-free-v1",
            "Content-Type": "application/json"
        }

    def test_get_user(self, api_headers):
        """Тест GET запроса для получения пользователя"""
        self._print_result("Выполняем GET запрос для получения пользователя")
        response = requests.get(f"{BASE_URL}/users/2", headers=api_headers)
        
        # Проверка статус-кода
        assert response.status_code == 200
        self._print_result(f"Статус-код: {response.status_code} - OK", "SUCCESS")
        
        # Проверка структуры JSON
        json_data = response.json()
        assert "data" in json_data
        assert all(key in json_data["data"] for key in ["id", "email", "first_name", "last_name", "avatar"])
        self._print_result("Структура JSON ответа корректна", "SUCCESS")
        
        # Проверка значений полей
        assert json_data["data"]["id"] == 2
        assert json_data["data"]["first_name"] == "Janet"
        assert json_data["data"]["last_name"] == "Weaver"
        self._print_result("Значения полей соответствуют ожидаемым", "SUCCESS")
        
        self._print_result("GET тест пройден успешно", "SUCCESS")

    def test_create_user(self, api_headers):
        """Тест POST запроса для создания пользователя"""
        self._print_result("Выполняем POST запрос для создания пользователя")
        payload = {
            "name": "artemy",
            "job": "leader"
        }
        
        response = requests.post(f"{BASE_URL}/users", json=payload, headers=api_headers)
        
        # Проверка статус-кода
        assert response.status_code == 201
        self._print_result(f"Статус-код: {response.status_code} - Created", "SUCCESS")
        
        # Проверка структуры JSON
        json_data = response.json()
        assert all(key in json_data for key in ["name", "job", "id", "createdAt"])
        self._print_result("Структура JSON ответа корректна", "SUCCESS")
        
        # Проверка значений полей
        assert json_data["name"] == payload["name"]
        assert json_data["job"] == payload["job"]
        self._print_result("Значения полей соответствуют ожидаемым", "SUCCESS")
        
        self._print_result("POST тест пройден успешно", "SUCCESS")

    def test_update_user(self, api_headers):
        """Тест PUT запроса для обновления пользователя"""
        self._print_result("Выполняем PUT запрос для обновления пользователя")
        payload = {
            "name": "artemy",
            "job": "gen prezident"
        }
        
        response = requests.put(f"{BASE_URL}/users/2", json=payload, headers=api_headers)
        
        # Проверка статус-кода
        assert response.status_code == 200
        self._print_result(f"Статус-код: {response.status_code} - OK", "SUCCESS")
        
        # Проверка структуры JSON
        json_data = response.json()
        assert all(key in json_data for key in ["name", "job", "updatedAt"])
        self._print_result("Структура JSON ответа корректна", "SUCCESS")
        
        # Проверка значений полей
        assert json_data["name"] == payload["name"]
        assert json_data["job"] == payload["job"]
        self._print_result("Значения полей соответствуют ожидаемым", "SUCCESS")
        
        self._print_result("PUT тест пройден успешно", "SUCCESS")

if __name__ == "__main__":
    # Запуск pytest с аргументами
    pytest.main([__file__, "-v", "-s"])        