def gf_multiply(byte1, byte2):
    result = 0
    for i in range(8):
        if byte2 & 1:  # Якщо наймолодший біт byte2 дорівнює 1, додаємо byte1 до результату
            result ^= byte1
        # Зсув byte1 вліво на 1 (множення на x)
        if byte1 & 0x80:  # Перевірка старшого біта
            byte1 = (byte1 << 1) ^ 0x1B  # Якщо старший біт був 1, XOR з поліномом m(x)
        else:
            byte1 <<= 1  # Інакше просто зсув
        byte1 &= 0xFF  # Забезпечення, що byte1 залишається байтом
        byte2 >>= 1  # Зсув byte2 вправо на 1 для обробки наступного біта
    return result

byte1 = 0x57
byte2 = 0x83

result = gf_multiply(byte1, byte2)


print(f"57 * 83 = {hex(result).upper()[2:]}")
