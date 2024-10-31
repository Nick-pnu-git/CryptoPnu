def gcdex(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def inverse_element(a, n):
    d, x, _ = gcdex(a, n)
    if d != 1:
        return None  # Якщо НСД(a, n) != 1, оберненого елемента не існує
    else:
        return x % n  # Повертаємо обернений елемент за модулем n

a, n = 5, 18
inv = inverse_element(a, n)
if inv is None:
    print(f"Обернений елемент для a = {a} за модулем n = {n} не існує.")
else:
    print(f"Обернений елемент для a = {a} за модулем n = {n} дорівнює {inv}")
    print(f"Перевірка: ({a} * {inv}) % {n} = {(a * inv) % n}")
