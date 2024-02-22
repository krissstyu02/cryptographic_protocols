class ModularExponentiation:
    def __init__(self, base, exponent, modulus):
        self.base = base
        self.exponent = exponent
        self.modulus = modulus

    def _modular_multiply(self, a, b):
        # Метод для умножения по модулю
        return (a * b) % self.modulus

    def _modular_add(self, a, b):
        # Метод для сложения по модулю
        return (a + b) % self.modulus

    def _modular_power_positive(self, base, exponent):
        # Метод для вычисления положительной степени по малой теореме Ферма
        result = 1
        base = base % self.modulus

        while exponent > 0:
            if exponent % 2 == 1:
                result = self._modular_multiply(result, base)
            exponent //= 2
            base = self._modular_multiply(base, base)

        return result

    def _modular_power_negative(self, base, exponent):
        # Метод для вычисления отрицательной степени по теореме Эйлера
        phi_modulus = self.modulus - 1  # phi(n) для простого модуля
        inverse_base = pow(base, phi_modulus - 1, self.modulus)  # a^(phi(n)-1) % n

        return self._modular_power_positive(inverse_base, -exponent)

    def calculate_power(self):
        if self.exponent >= 0:
            return self._modular_power_positive(self.base, self.exponent)
        else:
            return self._modular_power_negative(self.base, self.exponent)

# Пример использования класса
base = 2
exponent = 10
modulus = 1000000007

mod_exp = ModularExponentiation(base, exponent, modulus)
result = mod_exp.calculate_power()

print(f"{base}^{exponent} mod {modulus} = {result}")
