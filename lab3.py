# Класс для представления полиномов в поле GF(2)
class Polynom:
    def __init__(self, body):
        self.body = body

    # Возвращает степень полинома
    def degree(self):
        return len(self.body) - 1

    # Создает полином заданной степени с ведущим коэффициентом 1
    @classmethod
    def by_degree(cls, degree):
        new_poly = [0] * (degree + 1)
        new_poly[degree] = 1
        return cls(new_poly)

    # Создает полином по числу, представляя его в двоичной системе
    @classmethod
    def by_number(cls, number):
        new_poly = []
        while number:
            new_poly.append(number % 2)
            number //= 2
        return cls(new_poly)

    # Переопределение строки для красивого вывода полинома
    def __str__(self):
        terms = ['x^{}'.format(i) if c else '1' for i, c in enumerate(self.body[::-1]) if c]
        return ' + '.join(terms)

    # Переопределение оператора сложения для полиномов
    def __add__(self, b):
        new_degree = max(self.degree(), b.degree())
        new_poly = [0] * (new_degree + 1)
        for i in range(new_degree + 1):
            if i > self.degree():
                new_poly[i] = b.body[i]
            elif i > b.degree():
                new_poly[i] = self.body[i]
            else:
                new_poly[i] = self.body[i] ^ b.body[i]

        zero_pad_left = next((i for i in range(new_degree, -1, -1) if new_poly[i] != 0), 0)
        new_poly = new_poly[:-zero_pad_left] if zero_pad_left > 0 else new_poly

        return Polynom(new_poly)

    # Переопределение оператора умножения для полиномов
    def __mul__(self, b):
        new_poly = [0] * (self.degree() + b.degree() + 1)
        for i in range(self.degree(), -1, -1):
            if not self.body[i]:
                continue
            for j in range(b.degree(), -1, -1):
                new_poly[i + j] ^= self.body[i] & b.body[j]

        return Polynom(new_poly)

    # Переопределение оператора "больше или равно" для полиномов
    def __ge__(self, b):
        if self.degree() == b.degree():
            return self.body >= b.body
        else:
            return self.degree() >= b.degree()

    # Переопределение оператора деления для полиномов
    def __truediv__(self, b):
        divided_poly = Polynom(self.body)
        while divided_poly.degree() > b.degree():
            division_part_degree = divided_poly.degree() - b.degree()
            division_part_poly = Polynom.by_degree(division_part_degree)
            sub_part_poly = b * division_part_poly
            divided_poly = divided_poly + sub_part_poly

        if divided_poly.degree() == b.degree():
            if divided_poly >= b:
                divided_poly = divided_poly + b

        return Polynom(divided_poly.body)

# Функция для вывода шагов проверки
def print_step(description, poly):
    print(f"{description}:", poly)

# Функция для проверки неприводимости полинома
def polynom_is_irreducible(poly):
    max_search_degree = poly.degree() // 2
    max_search_number = 2**(max_search_degree + 1) - 1
    for i in range(2, max_search_number + 1):
        check_poly = Polynom.by_number(i)
        print_step("Проверка", check_poly)
        remainder = poly / check_poly
        print_step("Остаток", remainder)
        if remainder.degree() == -1:
            return False
    return True

# Функция для проверки примитивности полинома в GF(2^n)
def polynom_is_primitive_in_gp(poly, gp_degree):
    if polynom_is_irreducible(poly):
        max_degree = 2**gp_degree - 1
        print("\nПроверка примитивности:")
        for i in range(1, max_degree + 1):
            poly_number = 2**i
            check_poly = Polynom.by_number(poly_number + 1)
            print_step("Проверка", check_poly)
            remainder = check_poly / poly
            print_step("Остаток", remainder)
            if remainder.degree() == -1:
                return False
        return True
    return False

if __name__ == "__main__":
    # x^5 + x^2 + 1.
    print("Проверка полинома: x^5 + x^2 + 1 ")
    poly_true = Polynom.by_number(32 + 4 + 1)
    print_step("Неприводимость", polynom_is_irreducible(poly_true))
    print()

    # x^8 + 1.
    print("Проверка полинома: x^8 + 1")
    poly_false = Polynom.by_number(128 + 1)
    print_step("Неприводимость", polynom_is_irreducible(poly_false))
    print()

    print_step("Примитивность", polynom_is_primitive_in_gp(poly_true, 5))
