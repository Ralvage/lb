NOEKEON_KEY = [0, 0, 0, 0]
NUMBER_OF_ROUNDS = 16
WORKING_KEY = NOEKEON_KEY

def Round(Key, State, K1, K2):
    State[0] ^= K1
    State = Theta(Key, State)
    State[0] ^= K2
    State = Pi1(State)
    State = Gamma(State)
    State = Pi2(State)
    return State

def Gamma(a):
    a[1] ^= (~a[3] & ~a[2]) & 0xFFFFFFFF
    a[0] ^= (a[2] & a[1]) & 0xFFFFFFFF

    tmp = a[3]
    a[3] = a[0]
    a[0] = tmp
    a[2] ^= a[0] ^ a[1] ^ a[3]

    a[1] ^= (~a[3] & ~a[2]) & 0xFFFFFFFF
    a[0] ^= (a[2] & a[1]) & 0xFFFFFFFF
    return a

def Theta(k, a):
    temp = a[0] ^ a[2]
    temp = temp ^ ROTR32(temp, 8) ^ ROTL32(temp, 8)
    a[1] ^= temp
    a[3] ^= temp

    a[0] ^= k[0]
    a[1] ^= k[1]
    a[2] ^= k[2]
    a[3] ^= k[3]

    temp = a[1] ^ a[3]
    temp = temp ^ ROTR32(temp, 8) ^ ROTL32(temp, 8)
    a[0] ^= temp
    a[2] ^= temp
    return a

def Pi1(a):
    a[1] = ROTL32(a[1], 1)
    a[2] = ROTL32(a[2], 5)
    a[3] = ROTL32(a[3], 2)
    return a

def Pi2(a):
    a[1] = ROTR32(a[1], 1)
    a[2] = ROTR32(a[2], 5)
    a[3] = ROTR32(a[3], 2)
    return a

def ROTL32(v, n):
    if n <= 31:
        return 0xFFFFFFFF & ((v << n) | (v >> (32 - n)))
    else:
        print("ROTL32 -- Rotation Error")
        return v

def ROTR32(v, n):
    if n <= 31:
        return 0xFFFFFFFF & ((v >> n) | (v << (32 - n)))
    else:
        print("ROTR32 -- Rotation Error")
        return v

def NoekeonEncrypt(WorkingKey, State):
    Roundct = [0x80, 0x1B, 0x36, 0x6C,
               0xD8, 0xAB, 0x4D, 0x9A,
               0x2F, 0x5E, 0xBC, 0x63,
               0xC6, 0x97, 0x35, 0x6A, 0xD4]

    for i in range(NUMBER_OF_ROUNDS):
        State = Round(WorkingKey, State, Roundct[i], 0)

    State[0] ^= Roundct[NUMBER_OF_ROUNDS]
    State = Theta(WorkingKey, State)
    return State

def NoekeonDecrypt(WorkingKey, State):
    Roundct = [0x80, 0x1B, 0x36, 0x6C,
               0xD8, 0xAB, 0x4D, 0x9A,
               0x2F, 0x5E, 0xBC, 0x63,
               0xC6, 0x97, 0x35, 0x6A, 0xD4]

    WorkingKey = Theta([0, 0, 0, 0], WorkingKey)

    for i in range(NUMBER_OF_ROUNDS, 0, -1):
        State = Round(WorkingKey, State, 0, Roundct[i])

    State = Theta(WorkingKey, State)
    State[0] ^= Roundct[0]
    return State

def text_to_state(text):
    state = [0, 0, 0, 0]
    for i in range(4):
        state[i] = int.from_bytes(text[i * 4:(i + 1) * 4], 'big')
    return state

def state_to_text(state):
    text = b''
    for i in range(4):
        text += state[i].to_bytes(4, 'big')
    return text

def encrypt_text(WorkingKey, text):
    ciphertext = b''
    for i in range(0, len(text), 16):
        block = text_to_state(text[i:i + 16])
        encrypted_block = NoekeonEncrypt(WorkingKey, block)
        ciphertext += state_to_text(encrypted_block)
    return ciphertext

def decrypt_text(WorkingKey, ciphertext):
    plaintext = b''
    for i in range(0, len(ciphertext), 16):
        block = text_to_state(ciphertext[i:i + 16])
        decrypted_block = NoekeonDecrypt(WorkingKey, block)
        plaintext += state_to_text(decrypted_block)
    return plaintext

def enc(file):
    plaintext = open(file, 'rb').read()
    new = 0
    while len(plaintext) % 16 != 0:
        plaintext += b'|'
        new += 1

    ciphertext = encrypt_text(WORKING_KEY, plaintext)
    open(file, "wb").write(ciphertext)
    return True

def dec(file):
    file_dec = open(file, "rb").read()
    # one = file.split('/')
    # two = one[-1]
    # one[-1] = "copy_" + two[:-4]
    # file = '/'.join(one)

    decrypted_text = decrypt_text(WORKING_KEY, file_dec)

    while decrypted_text[-1] == "|":
        decrypted_text = decrypted_text[:-1]

    open(file, "wb").write(decrypted_text)
    return True
