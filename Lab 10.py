def left_rotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF


def to_bytes_le(value, length):
    return [(value >> (8 * i)) & 0xFF for i in range(length)]


def from_bytes_le(byte_list):
    return sum(b << (8 * i) for i, b in enumerate(byte_list))


def md5(message):
    # Константи
    s = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    ]

    def math_sin(value):
        x = value * 3.141592653589793 / 180
        result, term, n = x, x, 1
        while abs(term) > 1e-10:
            term *= -x * x / ((2 * n) * (2 * n + 1))
            result += term
            n += 1
        return result

    K = [int(abs(math_sin(i + 1)) * (2 ** 32)) & 0xFFFFFFFF for i in range(64)]



    # Початкові хеш значення
    a0, b0, c0, d0 = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)

    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8

    message += b"\x80"

    # Додайти від 0 до 512 бітів '0', щоб довжина повідомлення в бітах була конгруентною 448 (mod 512)
    while len(message) % 64 != 56:
        message += b"\x00"

    # Додайти початкову довжину повідомлення в бітах у кінець
    length_bytes = to_bytes_le(original_bit_len, 8)
    message += bytes(length_bytes)

    # Обробити повідомлення у послідовних блоках розміром 512 біт
    for chunk_offset in range(0, len(message), 64):
        chunk = message[chunk_offset:chunk_offset + 64]
        M = [from_bytes_le(chunk[i:i + 4]) for i in range(0, 64, 4)]

        A, B, C, D = a0, b0, c0, d0

        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | (~D & C)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | ~D)
                g = (7 * i) % 16

            F = (F + A + K[i] + M[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + left_rotate(F, s[i])) & 0xFFFFFFFF

        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

    # Створити підсумкове хеш-значення як 128-бітне число
    return ''.join(f'{byte:02x}' for value in (a0, b0, c0, d0) for byte in to_bytes_le(value, 4))

input_message = b"Hello, World!"
hash_value = md5(input_message)
print(f"MD5({input_message.decode()}) = {hash_value}")
