import math
import random

#НОД
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

#метод p-1
def pollards_p_minus_1(n):
    a = 2
    for j in range(2, 100):
        #возводим a^j mod n
        a = pow(a, j, n)
        #пробуем найти нод
        d = gcd(a - 1, n)
        #возращаем если нетривиален
        if 1 < d < n:
            return d
    return None

#метод rho
def pollards_rho(n):
    def f(x):
        #вспомогательная функция = x^2+1
        return (x ** 2 + 1) % n
    #нач значение=2
    x, y, d = 2, 2, 1
    #ищем x y
    while d == 1:
        x = f(x)
        y = f(f(y))
        #нод
        d = gcd(abs(x - y), n)
    #возращаем делитель если не 1
    return d

#вывод
def factorize_and_show_results(number):
    print(f"{number}. Первое число - найденный множитель")

    # (p-1)
    p_minus_1_result = pollards_p_minus_1(number)
    if p_minus_1_result:
        print(f"(p-1) Метод: {p_minus_1_result}*{number/p_minus_1_result}")
    else:
        print("(p-1) Метод: Не найдено")

    # Rho
    rho_result = pollards_rho(number)
    if rho_result:
        print(f"Rho Метод: {rho_result}*{number/rho_result}")
    else:
        print("Rho Метод: Не найдено")

    print()

# Примеры использования для различных чисел
numbers_to_factorize = [5959, 1234567, 987654321, 17,465784]
for num in numbers_to_factorize:
    factorize_and_show_results(num)
