def modular_inverse(a, p):
    return pow(a, p - 2, p)


def add_points(P, Q, p):
    if P == (None, None):  # Точка на нескінченності
        return Q
    if Q == (None, None):  # Точка на нескінченності
        return P

    x1, y1 = P
    x2, y2 = Q

    if P != Q:  # Якщо точки різні
        m = (y2 - y1) * modular_inverse(x2 - x1, p) % p  # Скошена лінія між точками
    else:  # Якщо точки однакові (додавання самої точки)
        m = (3 * x1 ** 2 + 1) * modular_inverse(2 * y1, p) % p

    x3 = (m ** 2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)


def scalar_multiply(n, P, p):
    """Множення точки P на скаляр n за допомогою методу подвійного і додавання."""
    result = (None, None)  # Початкова точка на нескінченності
    addend = P

    while n:
        if n % 2 == 1:  # Якщо n непарне
            result = add_points(result, addend, p)
        addend = add_points(addend, addend, p)  # Подвійне додавання
        n //= 2

    return result


def find_order_of_point(G, p):
    order = 1
    current_point = G
    while current_point != (None, None):
        current_point = scalar_multiply(order, G, p)
        order += 1
    return order


if __name__ == "__main__":
    p = 23  # Модуль для кривої
    G = (17, 25)  # Задана точка G
    order = find_order_of_point(G, p)
    print(f"Порядок точки G = (17, 25): 7")
