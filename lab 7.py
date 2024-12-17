import numpy as np

# Поле GF(2^8)
def gf_mult(a, b):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        carry = a & 0x80
        a = (a << 1) & 0xFF
        if carry:
            a ^= 0x1B
        b >>= 1
    return result

def gf_inverse(byte):
    if byte == 0:
        return 0
    for i in range(1, 256):
        if gf_mult(byte, i) == 1:
            return i
    return 0

def affine_transform(byte):
    c = 0x63
    result = byte
    for i in range(8):
        byte = (byte << 1) | (byte >> 7)
        result ^= byte & 0xFF
    return result ^ c

def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i, j] = affine_transform(gf_inverse(state[i, j]))
    return state

def shift_rows(state):
    for i in range(1, 4):
        state[i] = np.roll(state[i], -i)
    return state

def mix_columns(state):
    for i in range(4):
        col = state[:, i].copy()
        state[0, i] = gf_mult(col[0], 2) ^ gf_mult(col[1], 3) ^ col[2] ^ col[3]
        state[1, i] = col[0] ^ gf_mult(col[1], 2) ^ gf_mult(col[2], 3) ^ col[3]
        state[2, i] = col[0] ^ col[1] ^ gf_mult(col[2], 2) ^ gf_mult(col[3], 3)
        state[3, i] = gf_mult(col[0], 3) ^ col[1] ^ col[2] ^ gf_mult(col[3], 2)
    return state

def add_round_key(state, round_key):
    return state ^ round_key

def rcon(i):
    r = 1
    for _ in range(i - 1):
        r = gf_mult(r, 2)
    return r

def key_expansion(key):
    key_symbols = np.array(key, dtype=np.uint8).reshape(4, 4).T
    key_schedule = key_symbols.copy()

    for i in range(4, 44):
        temp = key_schedule[:, i - 1]
        if i % 4 == 0:
            temp = np.roll(temp, -1)
            temp = np.array([affine_transform(gf_inverse(b)) for b in temp], dtype=np.uint8)
            temp[0] ^= rcon(i // 4)
        key_schedule = np.column_stack((key_schedule, key_schedule[:, i - 4] ^ temp))
    return key_schedule.T.reshape(11, 4, 4)

def aes_encrypt(plaintext, key):
    state = np.array(plaintext, dtype=np.uint8).reshape(4, 4).T
    round_keys = key_expansion(key)

    state = add_round_key(state, round_keys[0])

    for i in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[i])

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[10])

    return state.T.flatten()

def aes_decrypt(ciphertext, key):
    state = np.array(ciphertext, dtype=np.uint8).reshape(4, 4).T
    round_keys = key_expansion(key)

    state = add_round_key(state, round_keys[10])
    state = shift_rows(state[::-1])
    state = sub_bytes(state)

    for i in range(9, 0, -1):
        state = add_round_key(state, round_keys[i])
        state = mix_columns(state[::-1])
        state = shift_rows(state[::-1])
        state = sub_bytes(state)

    state = add_round_key(state, round_keys[0])

    return state.T.flatten()


plaintext = [0x32, 0x33, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0xcf, 0xf8, 0x76, 0x34, 0x4a, 0x22]

ciphertext = aes_encrypt(plaintext, key)
decrypted_text = aes_decrypt(ciphertext, key)

print("Ciphertext:", ciphertext)
print("Decrypted text:", decrypted_text)
