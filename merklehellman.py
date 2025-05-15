def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

b = [7352, 2356, 7579, 19235, 1944, 14029, 1084]
w = [184, 332, 713, 1255, 2688, 5243, 10448]
q = 20910
ciphertext = [8436, 22465, 30044, 22465, 51635, 10380, 11879, 50551,
              35250, 51223, 14931, 25048, 7352, 50551, 37606, 39550]

# Recover r by brute-force
r = None
for guess in range(1, q):
    if egcd(guess, q)[0] == 1:
        if all((w[i] * guess) % q == b[i] for i in range(len(w))):
            r = guess
            break

if r is None:
    print("Failed to recover r")
    exit()

print(f"Recovered r = {r}")
r_inv = modinv(r, q)

# Decrypt
flag = b""
for c in ciphertext:
    c_prime = (c * r_inv) % q
    bits = 0
    for i in reversed(range(len(w))):  # From MSB to LSB
        if w[i] <= c_prime:
            c_prime -= w[i]
            bits |= (1 << (6 - i))
    flag += bytes([bits])

print("Decrypted Flag:", flag.decode())
