import pytest
import sys

from calculator import Calculator

class TestCalculator:
    """Тесты для класса Calculator"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Фикстура для инициализации калькулятора перед каждым тестом"""
        self.calc = Calculator()
        yield
    
    def _print_result(self, message, status="INFO"):
        """Вывод результата в stderr"""
        print(f"\n{status}: {message}", file=sys.stderr)
        sys.stderr.flush()
    
    #Тесты для метода add
    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),
        (-1, 1, 0),
        (0, 0, 0),
        (-5, -3, -8),
        (1.5, 2.5, 4.0),
    ])
    def test_add(self, a, b, expected):
        """Тестирование метода сложения с различными параметрами"""
        result = self.calc.add(a, b)
        assert result == expected
        self._print_result(f"add({a}, {b}) = {result} (ожидалось: {expected})", "SUCCESS")
    
    #Тесты для метода divide
    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5),
        (9, 3, 3),
        (5, 2, 2.5),
        (-10, 2, -5),
        (0, 5, 0),
    ])
    def test_divide(self, a, b, expected):
        """Тестирование метода деления с различными параметрами"""
        result = self.calc.divide(a, b)
        assert result == expected
        self._print_result(f"divide({a}, {b}) = {result} (ожидалось: {expected})", "SUCCESS")
    
    def test_divide_by_zero(self):
        """Тестирование обработки деления на ноль"""
        with pytest.raises(ZeroDivisionError) as exc_info:
            self.calc.divide(5, 0)
        
        assert "Деление на ноль невозможно" in str(exc_info.value)
        self._print_result("divide(5, 0) вызвал ожидаемое исключение ZeroDivisionError", "SUCCESS")
    
    #Тесты для метода is_prime_number
    @pytest.mark.parametrize("n,expected", [
        (2, True),
        (3, True),
        (5, True),
        (7, True),
        (11, True),
        (13, True),
        (17, True),
        (19, True),
        (4, False),
        (6, False),
        (8, False),
        (9, False),
        (10, False),
        (12, False),
        (25, False),
        (1, False),
        (0, False),
        (-5, False),
    ])
    def test_is_prime_number(self, n, expected):
        """Тестирование проверки простых чисел с различными параметрами"""
        result = self.calc.is_prime_number(n)
        assert result == expected
        status = "простым" if expected else "НЕ простым"
        self._print_result(f"Число {n} является {status}", "SUCCESS")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])