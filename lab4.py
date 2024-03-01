def is_primitive_poly(poly):
    degree = len(poly) - 1
    max_order = 2**degree - 1
    order = 1
    current_poly = poly[:]
    x_power = [0] * (max_order + 1)
    x_power[1] = 1

    for i in range(2, max_order + 1):
        x_power[i] = (x_power[i - 1] << 1) % (2**degree)
        if x_power[i] >= 2**degree:
            x_power[i] ^= poly

    for i in range(1, max_order):
        current_poly = multiply_polynomials(current_poly, poly)
        if current_poly == [0]:
            return False

        order += 1
        if order == max_order:
            return True

        if x_power[order] != 1:
            return False

def multiply_polynomials(poly1, poly2):
    result = [0] * (len(poly1) + len(poly2) - 1)
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            result[i + j] ^= poly1[i] & poly2[j]
    return result

# Многочлен 1100001
polynomial = [1, 1, 0, 0, 0, 0, 1]

if is_primitive_poly(polynomial):
    print("Многочлен примитивен в поле GF(2)")
else:
    print("Многочлен не примитивен в поле GF(2)")
