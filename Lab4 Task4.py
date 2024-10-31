def inverse_element_2(a, p):
    if p <= 1 or any(p % i == 0 for i in range(2, int(p ** 0.5) + 1)):
        return None  # Якщо p не є простим, обернений елемент не існує

    # Знаходимо обернений елемент за допомогою малої теореми Ферма
    return pow(a, p - 2, p)


a, p = 5, 18
inv = inverse_element_2(a, p)
if inv is None:
    print(f"Обернений елемент для a = {a} за модулем p = {p} не існує або p не є простим.")
else:
    print(f"Обернений елемент для a = {a} за модулем p = {p} дорівнює {inv}")
    print(f"Перевірка: ({a} * {inv}) % {p} = {(a * inv) % p}")
