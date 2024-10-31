def phi(m):
    result = m
    p = 2
    # Розкладаємо m на прості множники
    while p * p <= m:
        # Якщо p є дільником m
        if m % p == 0:
            # Видаляємо всі кратні p з m
            while m % p == 0:
                m //= p
            # Застосовуємо формулу для множника p
            result -= result // p
        p += 1
    # Якщо залишок m є простим числом більшим за sqrt(m)
    if m > 1:
        result -= result // m
    return result

m = 13
print(f"phi({m}) = {phi(m)}")
