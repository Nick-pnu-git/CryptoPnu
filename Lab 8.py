import random
# Тест на простоту за Рабіном-Міллером
def is_prime(n, k=40):  # k - кількість ітерацій
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Представляємо n-1 у вигляді 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Тест Рабіна-Міллера
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # a^d % n
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# Генерація безпечного простого числа p = 2q + 1
def generate_safe_prime(bits=512):
    while True:
        q = random.getrandbits(bits - 1)
        q |= (1 << (bits - 2)) | 1
        if is_prime(q) and is_prime(2 * q + 1):
            return 2 * q + 1


# Перевірка, чи є g первісним коренем за модулем p
def is_primitive_root(g, p):
    required_set = set(range(1, p))
    actual_set = {pow(g, power, p) for power in range(1, p)}
    return required_set == actual_set


# Пошук первісного кореня
def find_primitive_root(p):
    # Факторизація p-1
    p_minus_1 = p - 1
    factors = set()
    n = p_minus_1
    for i in range(2, int(n ** 0.5) + 1):
        while n % i == 0:
            factors.add(i)
            n //= i
    if n > 1:
        factors.add(n)

    # Пошук g, який задовольняє умову
    for g in range(2, p):
        is_primitive = all(pow(g, p_minus_1 // q, p) != 1 for q in factors)
        if is_primitive:
            return g
    return None


# Реалізація обміну ключами за Діффі-Хеллманом
def diffie_hellman_key_exchange(bits=512):
    print("Генерація безпечного простого числа p...")
    p = generate_safe_prime(bits)
    print(f"p = {p}")

    print("Пошук первісного кореня g...")
    g = find_primitive_root(p)
    print(f"g = {g}")

    # Вибір приватних ключів
    a = random.randint(2, p - 2)
    b = random.randint(2, p - 2)
    print(f"Приватний ключ A: {a}")
    print(f"Приватний ключ B: {b}")

    # Обчислення публічних ключів
    A = pow(g, a, p)
    B = pow(g, b, p)
    print(f"Публічний ключ A: {A}")
    print(f"Публічний ключ B: {B}")

    # Обчислення спільного секрету
    shared_secret_A = pow(B, a, p)
    shared_secret_B = pow(A, b, p)
    print(f"Спільний секрет (A): {shared_secret_A}")
    print(f"Спільний секрет (B): {shared_secret_B}")

    assert shared_secret_A == shared_secret_B, "Спільні секрети не співпадають!"
    return shared_secret_A


# Виклик функції
shared_secret = diffie_hellman_key_exchange(bits=32)
print(f"Спільний секрет: {shared_secret}")
