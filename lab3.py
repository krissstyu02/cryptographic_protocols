class Polynom:
    #инициализация
    def __init__(self, body):
        self.body = body

    #степень полинома
    def degree(self):
        return len(self.body) - 1

    #создаем полином по степени(5=x^5)
    @classmethod
    def by_degree(cls, degree):
        new_poly = [0] * (degree + 1)
        new_poly[degree] = 1
        return cls(new_poly)

    #получить полином по числам(4+2+1=7=111) - метод класса
    @classmethod
    def by_number(cls, number):
        new_poly = []
        while number:
            #добавляем остаток от деления
            new_poly.append(number % 2)
            #переходим к след разряду
            number //= 2
        return cls(new_poly)

    #вывод в форме полинома
    def print(self):
        terms = []
        # Идем с конца последовательности
        for i, c in enumerate(self.body):
            #если эл-т=1
            if c:
                term = 'x^{}'.format(i) #форматриуем индекс под вид полинома
                terms.append(term)

        polynomial_str = ' + '.join(terms)  # Соединяем члены полинома в строку с разделителем ' + '

        return polynomial_str

    #сложение полиномов
    def add(self, b):
        #степень итогового полинома=макс степеней
        new_degree = max(self.degree(), b.degree())
        new_poly = [0] * (new_degree + 1)
        for i in range(new_degree + 1):
            #степень первого полинома меньше чем итоговый разряд
            if i > self.degree():
                #берем значение второго полинома
                new_poly[i] = b.body[i]
            # степень второго полинома меньше чем итоговый разряд
            elif i > b.degree():
                new_poly[i] = self.body[i]
            else:
            #операция xor
                new_poly[i] = self.body[i] ^ b.body[i]

        #убираем ведущие нули
        zero_pad_left = 0
        for i in range(new_degree, -1, -1):
            if new_poly[i] == 0:
                zero_pad_left += 1
            else:
                break
        new_poly = new_poly[:-zero_pad_left] if zero_pad_left > 0 else new_poly

        return Polynom(new_poly)

    #умножение полиномов
    def multiplications(self, b):
        #полином степени равной сумме степеней множителей self и b
        new_poly = [0] * (self.degree() + b.degree() + 1)
        #Цикл проходит по всем степеням полинома self от самой высокой до нулевой
        for i in range(self.degree(), -1, -1):
            #Если коэффициент при текущей степени в полиноме self равен нулю, то переходим к следующей итерации цикла.
            if not self.body[i]:
                continue
            for j in range(b.degree(), -1, -1):
            #Операция XOR между new_poly и результатом поразрядного умножения коэффициентов при степенях i и j в полиномах self и b
                new_poly[i + j] ^= self.body[i] & b.body[j]

        return Polynom(new_poly)

    #сравнение полиномов
    def equals(self, b):
        #если степени равны
        if self.degree() == b.degree():
            #сравниваем каждый бит
            for i in range(b.degree(), -1, -1):
                if self.body[i] != b.body[i]:
                    return self.body[i] > b.body[i]
            return True
        else:
            #если степени не равны-первый точно больше
            return self.degree() >= b.degree()

    #деление полиномов
    def division(self, b):
        divided_poly = Polynom(self.body)
        #пока степень делимого многочлена больше
        while divided_poly.degree() > b.degree():
            division_part_degree = divided_poly.degree() - b.degree()
            #берем полином степени(делимый многочлен-делитель)
            division_part_poly = Polynom.by_degree(division_part_degree)
            #умножаем полученный многочлен на подобранный
            sub_part_poly = division_part_poly.multiplications(b)
            #прибавляем делимый многочлен с умножаемым членом(т.к. в поле +=-)
            divided_poly = divided_poly.add(sub_part_poly)
        #если степени равны
        if divided_poly.degree() == b.degree():
    #если они равны
            if divided_poly.equals(b):
                #прибавляем b(получаем ост от деления)
                divided_poly = divided_poly.add(b)

        return Polynom(divided_poly.body)

#является ли полином неприводимым?
def polynom_is_irreducible(poly):
    # неприводимые полиномы из таблицы
    known_irreducible_polynomials = [2, 3, 7, 11, 13, 19, 25, 31, 37, 41, 47, 55, 59, 61, 67, 73, 87, 91, 97, 103, 109,
                                     115, 117, 131, 137, 143, 145, 157, 167, 171, 185, 191, 193, 203, 211, 213, 229]
    for poly_number in known_irreducible_polynomials:
        if(poly.body==Polynom.by_number(poly_number).body):
            return True
    #максимальная степень полинома для деления
    max_search_degree = poly.degree() // 2
    max_search_number = 2**(max_search_degree + 1)


    #проверяем неприводимость делением на неприводимые полиномы степени(degree/2)
    for poly_number in known_irreducible_polynomials:
        # Проверяем, что степень полинома не превышает max_search_degree
        if poly_number <= max_search_number:
            check_poly = Polynom.by_number(poly_number)
            print("Делим на:", check_poly.print())
            remainder = poly.division(check_poly)
            print("Остаток:", remainder.print())
            if remainder.degree() == -1:
                return False

    return True

#является ли полином примитивным?
#примитивный=неприводимый+делит многочлены поля вида x^(2^i)+1 с остатком
def polynom_is_primitive_in_gp(poly, gp_degree):
    #полином не приводим
    if polynom_is_irreducible(poly):
        #макс степень=степень поля
        max_degree = 2**gp_degree
        for i in range(1, max_degree):
            poly_number = 2**i
            check_poly = Polynom.by_number(poly_number + 1)
            print("Делимый полином:", check_poly.print())
            remainder = check_poly.division(poly)
            print("Остаток:", remainder.print())
            #остаток=0
            if remainder.degree() == -1:
                return False
        return True
    return False

if __name__ == "__main__":
    #неприводимый=True(из таблицы или не делится)
    #приводимый(делится на тот что из таблицы)  1100001

    poly_true = Polynom.by_number(64+32+1)
    # print("Проверка полинома на неприводимость: ", poly_true.print())
    # print(polynom_is_irreducible(poly_true))
    # print()

    # poly_false = Polynom.by_number(8+2)
    # print("Проверка полинома на неприводимость: ", poly_false.print())
    # print(polynom_is_irreducible(poly_false))
    # print()

    print("Проверка полинома на примитивность в GF(2): ", poly_true.print())
    print(polynom_is_primitive_in_gp(poly_true, 2))
