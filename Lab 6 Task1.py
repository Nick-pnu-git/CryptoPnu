def mul02(byte):
    # Зсув вліво
    result = byte << 1
    # Перевірка на переповнення (якщо старший біт = 1)
    if result & 0x100:  # Якщо результат вийшов за межі 8 бітів
        result ^= 0x11B  # XOR з модульним поліномом
    return result & 0xFF  # Залишаємо тільки 8 молодших бітів


def mul03(byte):
    return mul02(byte) ^ byte

byte1 = 0xD4  # Вхідний байт D4
byte2 = 0xBF  # Вхідний байт BF

result1 = mul02(byte1)  # D4 * 02
result2 = mul03(byte2)  # BF * 03

print(f"D4 * 02 = {hex(result1).upper()[2:]}")
print(f"BF * 03 = {hex(result2).upper()[2:]}")