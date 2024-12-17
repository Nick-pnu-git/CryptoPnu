import random
from hashlib import sha256


# Функція для знаходження оберненого елемента
def modular_inverse(a, p):
    return pow(a, p - 2, p)


# Додавання двох точок на еліптичній кривій
def add_points(P, Q, p):
    if P == (None, None):
        return Q
    if Q == (None, None):
        return P
    x1, y1 = P
    x2, y2 = Q

    if P != Q:
        m = (y2 - y1) * modular_inverse(x2 - x1, p) % p
    else:
        m = (3 * x1 ** 2 + 1) * modular_inverse(2 * y1, p) % p

    x3 = (m ** 2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)


# Множення точки на скаляр
def scalar_multiply(n, P, p):
    result = (None, None)
    addend = P
    while n:
        if n % 2 == 1:
            result = add_points(result, addend, p)
        addend = add_points(addend, addend, p)
        n //= 2
    return result


# Генерація закритого і відкритого ключів
def generate_keys(p, a, b, G):
    # Генерація закритого ключа
    private_key = random.randint(1, p - 1)
    # Генерація відкритого ключа (y = private_key * G)
    public_key = scalar_multiply(private_key, G, p)
    return private_key, public_key


# Підписування повідомлення
def ecdsa_sign(message, private_key, p, a, b, G):
    # Хешування повідомлення
    Hm = int(sha256(message.encode()).hexdigest(), 16)  # Використовуємо SHA-256
    while True:
        # Вибір випадкового числа k
        k = random.randint(1, p - 1)
        # Обчислення точки k * G
        P = scalar_multiply(k, G, p)
        r = P[0] % p  # Використовуємо x-координату точки
        if r == 0:
            continue
        s = modular_inverse(k, p - 1) * (Hm + r * private_key) % (p - 1)
        if s == 0:
            continue
        return r, s


# Перевірка підпису
def ecdsa_verify(message, signature, public_key, p, a, b, G):
    r, s = signature
    if r <= 0 or r >= p or s <= 0 or s >= p - 1:
        return False
    # Хешування повідомлення
    Hm = int(sha256(message.encode()).hexdigest(), 16)
    w = modular_inverse(s, p - 1)
    u1 = (Hm * w) % (p - 1)
    u2 = (r * w) % (p - 1)
    P1 = scalar_multiply(u1, G, p)
    P2 = scalar_multiply(u2, public_key, p)
    P = add_points(P1, P2, p)
    if P[0] % p == r:
        return True
    else:
        return False


# Задати параметри кривої y^2 = x^3 + x + 1 (mod 23)
p = 23
a = 1
b = 1
G = (17, 20)  # Базова точка (генератор)

# Генерація ключів
private_key, public_key = generate_keys(p, a, b, G)
print(f"Закритий ключ: {private_key}")
print(f"Відкритий ключ: {public_key}")

# Підписування
message = "Hello, ECDSA!"
signature = ecdsa_sign(message, private_key, p, a, b, G)
print(f"Підпис: {signature}")

# Перевірка підпису
is_valid = ecdsa_verify(message, signature, public_key, p, a, b, G)
print(f"Підпис {'' if is_valid else 'не '}є дійсним.")

