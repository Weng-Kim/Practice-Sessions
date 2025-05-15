from math import gcd

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def lcm(a, b):
    return a * b // gcd(a, b)

# Given values
p = 75000325607193724293694446403116223058337764961074929316352803137087536131383
q = 69376057129404174647351914434400429820318738947745593069596264646867332546443
e = 16
c = 3708354049649318175189820619077599798890688075815858391284996256924308912935262733471980964003143534200740113874286537588889431819703343015872364443921848

# Compute necessary values
n = p * q
lambda_n = lcm(p-1, q-1)

try:
    d = modinv(e, lambda_n)
    m = pow(c, d, n)
    print("Decrypted message:", m)
    print("Hex representation:", hex(m))
except ValueError as e:
    print("Error:", e)
    print("Cannot compute inverse, try another approach")