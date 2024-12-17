import random


def is_prime_miller_rabin(p, k):
    if p <= 3:
        return p == 2 or p == 3

    if p % 2 == 0:
        return False

    # Розклад p-1 на 2^s * d
    s = 0
    d = p - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    def check_composite(a, p, d, s):
        x = pow(a, d, p)  # Обчислення (a^d) % p
        if x == 1 or x == p - 1:
            return False  # Число не є складеним у цьому раунді
        for _ in range(s - 1):
            x = (x * x) % p  # Підносимо до квадрата
            if x == p - 1:
                return False
        return True  # Число точно складене

    for _ in range(k):
        a = random.randint(2, p - 2)
        if check_composite(a, p, d, s):
            return "Число складене"

    probability = 1 - 4 ** (-k)
    return f"Число ймовірно просте з ймовірністю {probability:.5f}"

p = int(input("Введіть число p (p > 3, непарне): "))
k = int(input("Введіть кількість раундів k: "))

result = is_prime_miller_rabin(p, k)
print(result)
