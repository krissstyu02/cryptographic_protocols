import time
import random
import math

# Функция Эйлера представляет собой количество положительных целых чисел, меньших n, взаимно простых с


# Функция для нахождения функции Эйлера по определению
def euler_phi_definition(n):
    count = 0
    for i in range(1, n + 1):
        #нод==1(взаимно простое)
        if math.gcd(n, i) == 1:
            count += 1
    # print("Функция Эйлера")
    # print(count)
    return count

# Функция для нахождения функции Эйлера с использованием формулы
def euler_phi_standard_formula(n):
    result = n
    # Получаем список простых множителей числа n
    prime_factors = set()
    i = 2
    while i <= n:
        #i-делитель
        while n % i == 0:
            prime_factors.add(i)
            #делим
            n //= i
        i += 1
    if n > 1:
        prime_factors.add(n)

    # Вычисляем значение функции Эйлера по стандартной формуле
    for p in prime_factors:
        result *= (1 - 1 / p)
    # print("Функция Эйлера")
    # print(round(result))
    return round(result)

# Функция для нахождения функции Эйлера с использованием формулы оптимизированно
def euler_phi_standard_formula_opt(n):
    # print(n)
    result = n
    # Получаем список простых множителей числа n
    prime_factors = set()
    i = 2
    while i*i <= n:
        #i-делитель
        while n % i == 0:
            prime_factors.add(i)
            #делим
            n //= i
        i += 1
    if n > 1:
        prime_factors.add(n)
    # Вычисляем значение функции Эйлера по стандартной формуле
    for p in prime_factors:
        result *= (1 - 1 / p)
    # print("Функция Эйлера")
    # print(round(result))
    return round(result)


# Генерация списка из 100 случайных чисел, каждое из которых больше 10,000,000
numbers = [random.randint(100, 300) for _ in range(10)]

# # Измерение времени выполнения для метода с использованием формулы
# start_time = time.time()
# for num in numbers:
#     euler_phi_standard_formula_opt(num)
# end_time = time.time()
# print(f"Время выполнения (с использованием оптимизированной формулы): {end_time - start_time} секунд")
#
# # Измерение времени выполнения для метода с использованием формулы
# start_time = time.time()
# for num in numbers:
#     euler_phi_standard_formula(num)
# end_time = time.time()
# print(f"Время выполнения (с использованием формулы): {end_time - start_time} секунд")
#
# # Измерение времени выполнения для метода с использованием оптимизированной формулы
# start_time = time.time()
# for num in numbers:
#     euler_phi_standard_formula_opt(num)
# end_time = time.time()
# print(f"Время выполнения (с использованием оптимизированной формулы): {end_time - start_time} секунд")


# for num in numbers:
#     euler_phi_standard_formula_opt(num)
#     euler_phi_standard_formula(num)
#     euler_phi_definition(num)


