from sympy import Symbol, GF

class Polynom:
    def __init__(self, body):
        self.body = body

    def degree(self):
        return len(self.body) - 1

    @classmethod
    def by_degree(cls, degree):
        new_poly = [0] * (degree + 1)
        new_poly[degree] = 1
        return cls(new_poly)

    @classmethod
    def by_number(cls, number):
        new_poly = []
        while number:
            new_poly.append(number % 2)
            number //= 2
        return cls(new_poly)

    def __str__(self):
        return ' + '.join(['x^{}'.format(i) if c else '1' for i, c in enumerate(self.body[::-1]) if c])

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

        zero_pad_left = 0
        for i in range(new_degree, -1, -1):
            if new_poly[i] == 0:
                zero_pad_left += 1
            else:
                break
        new_poly = new_poly[:-zero_pad_left] if zero_pad_left > 0 else new_poly

        return Polynom(new_poly)

    def __mul__(self, b):
        new_poly = [0] * (self.degree() + b.degree() + 1)
        for i in range(self.degree(), -1, -1):
            if not self.body[i]:
                continue
            for j in range(b.degree(), -1, -1):
                new_poly[i + j] ^= self.body[i] & b.body[j]

        return Polynom(new_poly)

    def __ge__(self, b):
        if self.degree() == b.degree():
            for i in range(b.degree(), -1, -1):
                if self.body[i] != b.body[i]:
                    return self.body[i] > b.body[i]
            return True
        else:
            return self.degree() >= b.degree()

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

def polynom_is_irreducible(poly):
    max_search_degree = poly.degree() // 2
    max_search_number = 2**(max_search_degree + 1) - 1
    for i in range(2, max_search_number + 1):
        check_poly = Polynom.by_number(i)
        print("check:", check_poly)
        remainder = poly / check_poly
        print("remainder is:", remainder)
        if remainder.degree() == -1:
            return False
    return True

def polynom_is_primitive_in_gp(poly, gp_degree):
    if polynom_is_irreducible(poly):
        max_degree = 2**gp_degree - 1
        print("\nprimitive check:")
        for i in range(1, max_degree + 1):
            poly_number = 2**i
            check_poly = Polynom.by_number(poly_number + 1)
            print("check:", check_poly)
            remainder = check_poly / poly
            print("remainder is:", remainder)
            if remainder.degree() == -1:
                return False
        return True
    return False

if __name__ == "__main__":
    # x^5 + x^2 + 1
    #неприводимый=True(из таблицы или не делится)
    #приводимый(делится на тот что из таблицы)

    poly_true = Polynom.by_number(4+2+1)
    print(polynom_is_irreducible(poly_true))
    print()

    poly_false = Polynom.by_number(8+1)
    print(polynom_is_irreducible(poly_false))
    print()

    print(polynom_is_primitive_in_gp(poly_true, 5))
