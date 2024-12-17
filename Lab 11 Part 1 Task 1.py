def modular_sqrt(a, p):
    if a == 0:
        return 0
    # Перевірка, чи a є квадратичним лишком за модулем p
    if pow(a, (p - 1) // 2, p) != 1:
        return None  # Кореня немає

    # Спрощений випадок для малих чисел: перебираємо всі y
    for y in range(p):
        if (y * y) % p == a:
            return y
    return None


def find_points_on_curve(p):
    points = []

    for x in range(p):  # Перебір всіх x від 0 до p-1
        # Обчислюємо праву частину x^3 + x + 1 mod p
        rhs = (x ** 3 + x + 1) % p

        # Знаходимо квадратичний корінь з rhs (y^2 ≡ rhs mod p)
        y = modular_sqrt(rhs, p)

        if y is not None:  # Якщо корінь існує
            points.append((x, y))  # Точка (x, y)
            if y != 0:  # Додаємо симетричну точку (x, -y mod p)
                points.append((x, p - y))

    return points


if __name__ == "__main__":
    p = 23  # Просте число модуль
    print("Точки на еліптичній кривій y^2 ≡ x^3 + x + 1 mod 23:")
    points = find_points_on_curve(p)

    for point in sorted(points):
        print(point)

    print(f"\nЗагальна кількість точок: {len(points)}")
