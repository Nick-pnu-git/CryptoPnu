import random

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
        m = (3 * x1 ** 2 - 1) * modular_inverse(2 * y1, p) % p

    x3 = (m ** 2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)

def scalar_multiply(n, P, p):
    # Множення точки P на скаляр n за допомогою методу подвійного і додавання.
    result = (None, None)  # Початкова точка на нескінченності
    addend = P

    while n:
        if n % 2 == 1:  # Якщо n непарне
            result = add_points(result, addend, p)
        addend = add_points(addend, addend, p)  # Подвійне додавання
        n //= 2

    return result

def elgamal_encrypt(message, public_key, generator, p):
    k = random.randint(1, p - 1)  # Випадкове число
    C1 = scalar_multiply(k, generator, p)  # C1 = k * G
    shared_secret = scalar_multiply(k, public_key, p)  # k * Q
    C2 = add_points(message, shared_secret, p)  # C2 = P + k * Q
    return C1, C2

def elgamal_decrypt(C1, C2, private_key, p):
    shared_secret = scalar_multiply(private_key, C1, p)  # d * C1
    inverse_shared_secret = (shared_secret[0], (-shared_secret[1]) % p)  # -k * Q
    decrypted_message = add_points(C2, inverse_shared_secret, p)  # C2 - k * Q
    return decrypted_message

def main():
    # Задана еліптична крива: y^2 = x^3 - x + 3 (mod 127)
    p = 127
    a = -1
    b = 3

    # Базова точка (генератор)
    G = (75, 6)

    # Перевірка порядку точки
    private_key = random.randint(1, p - 1)  # Закритий ключ
    public_key = scalar_multiply(private_key, G, p)  # Публічний ключ

    print(f"Приватний ключ: {private_key}")
    print(f"Публічний ключ: {public_key}")

    # Повідомлення як точка на кривій
    message = (71, 46)

    # Шифрування
    C1, C2 = elgamal_encrypt(message, public_key, G, p)
    print(f"Шифротекст: C1 = {C1}, C2 = {C2}")

    # Розшифрування
    decrypted_message = elgamal_decrypt(C1, C2, private_key, p)
    print(f"Розшифроване повідомлення: {decrypted_message}")

if __name__ == "__main__":
    main()
