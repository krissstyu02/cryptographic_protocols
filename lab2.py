from lab1 import euler_phi_standard_formula_opt


class ModularExponentiation:
    def __init__(self, base, exponent, modulus):
        # Инициализация объекта с основанием, степенью и модулем
        self.base = base
        self.exponent = exponent
        self.modulus = modulus

    def _modular_multiply(self, a, b):
        # Метод для умножения по модулю
        return (a * b) % self.modulus

    def _are_coprime(self, a, b):
        # Метод для проверки взаимной простоты(Алгоритм Евклида)
        while b:
            a, b = b, a % b
        return a == 1

    # Малая теорема Ферма утверждает, что: если p — простое число, то для любого целого числа a, не кратного p,
    # a^(p-1) при делении на p дает остаток 1.
    def _modular_power_positive(self, base, exponent):
        result = 1
        # приводим основание к модулю
        base = base % self.modulus

        # Проверка взаимной простоты между основанием и модулем
        if not self._are_coprime(base, self.modulus):
            raise ValueError("Основание и модуль должны быть взаимно просты")

        while exponent > 0:
            # степень числа нечетная
            if exponent % 2 == 1:
                # умножаем наше число на себя (сделать степень четной)
                result = self._modular_multiply(result, base)
            # уменьшаем степень вдвое
            exponent //= 2
            # возводим основание в квадрат по модулю
            base = self._modular_multiply(base, base)

        return result

    def _modular_power_negative(self, base, exponent):
        # Метод для вычисления отрицательной степени по теореме Эйлера
        # проверяем взаимную простоту между основанием и модулем
        if not self._are_coprime(base, self.modulus):
            raise ValueError("Основание и модуль должны быть взаимно просты")

        # находим функцию Эйлера от модуля
        phi_modulus = euler_phi_standard_formula_opt((self.modulus))
        # находим обратный эл-т по теореме Эйлера
        inverse_base = pow(base, phi_modulus - 1, self.modulus)  # a^(phi(n)-1) % n

        return self._modular_power_positive(inverse_base, -exponent)

    def calculate_power(self):
        # Вычисление степени в зависимости от знака экспоненты
        if self.exponent >= 0:
            return self._modular_power_positive(self.base, self.exponent)
        else:
            return self._modular_power_negative(self.base, self.exponent)


# Пример использования класса
base = 3
exponent = 5
modulus = 11

mod_exp = ModularExponentiation(base, exponent, modulus)
result = mod_exp.calculate_power()

print(f"{base}^{exponent} mod {modulus} = {result}")
