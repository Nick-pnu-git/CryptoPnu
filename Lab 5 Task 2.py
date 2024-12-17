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
            x = pow(x, 2, n)  # x^2 % n
            if x == n - 1:
                break
        else:
            return False  # Число складене
    return True

# Генерація великого простого числа
def generate_large_prime(bits=1024):
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1  # Забезпечуємо, що число непарне і має потрібну довжину
        if is_prime_miller_rabin(num):
            return num

# Розширений алгоритм Евкліда для знаходження оберненого елемента
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Обернений елемент не існує")
    return x % phi

# Генерація ключів RSA
def generate_rsa_keys(bits=1024):
    print("Генерація простих чисел...")
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    print("Прості числа згенеровані.")
    n = p * q
    phi = (p - 1) * (q - 1)

    # Вибір відкритого ключа e
    e = 65537  # Стандартне значення для e
    if gcd(e, phi) != 1:
        raise ValueError("e не є взаємно простим з phi")

    # Обчислення закритого ключа d
    d = mod_inverse(e, phi)

    print("Ключі успішно згенеровані.")
    return (e, n), (d, n)

# Шифрування
def encrypt(message, public_key):
    e, n = public_key
    message_int = int.from_bytes(message.encode(), 'big')
    if message_int >= n:
        raise ValueError("Повідомлення завелике для заданого ключа")
    cipher = pow(message_int, e, n)
    return cipher

# Розшифрування
def decrypt(cipher, private_key):
    d, n = private_key
    decrypted_int = pow(cipher, d, n)
    message_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big')
    return message_bytes.decode()

# Основна програма
if __name__ == "__main__":
    bits = 1024
    print("Генерація ключів RSA...")
    public_key, private_key = generate_rsa_keys(bits)
    print(f"Відкритий ключ: {public_key}")
    print(f"Закритий ключ: {private_key}")

    # Повідомлення для шифрування
    message = "Hello, RSA!"
    print(f"\nОригінальне повідомлення: {message}")

    # Шифрування
    cipher = encrypt(message, public_key)
    print(f"Зашифроване повідомлення: {cipher}")

    # Розшифрування
    decrypted_message = decrypt(cipher, private_key)
    print(f"Розшифроване повідомлення: {decrypted_message}")
