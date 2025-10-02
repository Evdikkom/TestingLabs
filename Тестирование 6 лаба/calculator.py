class Calculator:
    """Класс калькулятора с базовыми математическими операциями"""
    
    def add(self, a, b):
        """Сложение двух чисел"""
        return a + b
    
    def divide(self, a, b):
        """Деление двух чисел"""
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно!")
        return a / b
    
    def is_prime_number(self, n):
        """Проверка, является ли число простым"""
        if not isinstance(n, int) or n <= 1:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        #Проверяем нечетные делители до квадратного корня из n
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True