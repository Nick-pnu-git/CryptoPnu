import random
from math import gcd

# Тест Міллера-Рабіна для перевірки простоти
def is_prime_miller_rabin(n, k=40):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Розкладання n-1 = 2^s * d
    s, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # Перевірка k разів
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # a^d % n
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# Генерація великого простого числа
def generate_large_prime(bits=128):
    while True:
        prime_candidate = random.getrandbits(bits)
        prime_candidate |= (1 << bits - 1) | 1  # Забезпечуємо непарність і бітову довжину
        if is_prime_miller_rabin(prime_candidate):
            return prime_candidate


# Перевірка, чи g є первісним коренем за модулем p
def is_primitive_root(g, p):
    required_set = {pow(g, i, p) for i in range(1, p)}
    return len(required_set) == p - 1


# Знаходження первісного кореня за модулем p
def find_primitive_root(p):
    def factorize(n):
        factors = set()
        while n % 2 == 0:
            factors.add(2)
            n //= 2
        for i in range(3, int(n**0.5) + 1, 2):
            while n % i == 0:
                factors.add(i)
                n //= i
        if n > 2:
            factors.add(n)
        return factors

    factors = factorize(p - 1)  # Факторизація p-1
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError("Первісний корінь не знайдено")


# Генерація ключів Ель-Гамаля
def generate_elgamal_keys(bits=128):
    print("Генерація простого числа p...")
    p = generate_large_prime(bits)
    print(f"Просте число p: {p}")

    print("Знаходження первісного кореня g...")
    g = find_primitive_root(p)
    print(f"Первісний корінь g: {g}")

    # Генерація закритого ключа x і відкритого ключа y
    x = random.randint(2, p - 2)  # Закритий ключ
    y = pow(g, x, p)  # Відкритий ключ

    print("Ключі згенеровані успішно!")
    public_key = (p, g, y)
    private_key = x
    return public_key, private_key


# Шифрування
def elgamal_encrypt(message, public_key):
    p, g, y = public_key
    m = int.from_bytes(message.encode(), 'big')
    if m >= p:
        raise ValueError("Повідомлення завелике для шифрування")

    k = random.randint(2, p - 2)  # Випадкове число
    a = pow(g, k, p)
    b = (pow(y, k, p) * m) % p
    return a, b


# Розшифрування
def elgamal_decrypt(ciphertext, private_key, p):
    a, b = ciphertext
    x = private_key
    s = pow(a, x, p)  # s = a^x % p
    s_inv = pow(s, -1, p)  # Модульно обернений елемент для s
    m = (b * s_inv) % p
    return m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()


if __name__ == "__main__":
    bits = 128  # Кількість біт для простого числа
    print("Генерація ключів Ель-Гамаля...")
    public_key, private_key = generate_elgamal_keys(bits)
    p, g, y = public_key
    print(f"Відкритий ключ: p={p}, g={g}, y={y}")
    print(f"Закритий ключ: x={private_key}")

    # Тестування шифрування та розшифрування
    message = "Hello, ElGamal!"
    print(f"\nОригінальне повідомлення: {message}")

    # Шифрування
    ciphertext = elgamal_encrypt(message, public_key)
    print(f"Зашифроване повідомлення: {ciphertext}")

    # Розшифрування
    decrypted_message = elgamal_decrypt(ciphertext, private_key, p)
    print(f"Розшифроване повідомлення: {decrypted_message}")
