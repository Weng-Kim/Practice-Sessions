from math import gcd
from itertools import product

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None  # No inverse exists
    return x % m

def nth_root_mod(c, e, p):
    """Find x such that x^e ≡ c mod p"""
    # Handle special case when c ≡ 0 mod p
    if c % p == 0:
        return [0]
    
    # Find generator/primitive root would be better, but this works for our case
    if p == 2:
        return [c]
    
    # For p-1 and e sharing factors
    phi = p - 1
    g = gcd(e, phi)
    if g == 1:
        d = modinv(e, phi)
        return [pow(c, d, p)]
    
    # When gcd(e, phi) > 1
    e_div_g = e // g
    phi_div_g = phi // g
    d = modinv(e_div_g, phi_div_g)
    if d is None:
        return []
    
    a = pow(c, d, p)
    
    # Find g-th roots of a mod p
    # Find primitive root would be better, but we'll brute-force for small g
    roots = set()
    for x in range(p):
        if pow(x, e_div_g, p) == a:
            roots.add(x)
    return sorted(roots)

def decrypt_unusual_rsa(c, e, p, q):
    n = p * q
    
    # Factor e into prime powers (16 = 2^4)
    factors = []
    temp = e
    while temp > 1:
        for f in [2, 3, 5, 7, 11, 13]:
            if temp % f == 0:
                factors.append(f)
                temp = temp // f
                break
    
    # Apply successive roots
    current_roots = [c]
    for f in factors:
        new_roots = []
        for root in current_roots:
            # Find roots modulo p and q
            roots_p = nth_root_mod(root % p, f, p)
            roots_q = nth_root_mod(root % q, f, q)
            
            # Combine with CRT
            for rp, rq in product(roots_p, roots_q):
                # Chinese Remainder Theorem
                g, x, y = extended_gcd(p, q)
                if (rq - rp) % g != 0:
                    continue  # No solution
                lcm = p // g * q
                combined = (rp + (rq - rp) // g * x % (q//g) * p) % lcm
                new_roots.append(combined)
        current_roots = list(set(new_roots))  # Remove duplicates
    
    return sorted(current_roots)

# Given values
p = 75000325607193724293694446403116223058337764961074929316352803137087536131383
q = 69376057129404174647351914434400429820318738947745593069596264646867332546443
e = 16
c = 3708354049649318175189820619077599798890688075815858391284996256924308912935262733471980964003143534200740113874286537588889431819703343015872364443921848

# Decrypt
possible_messages = decrypt_unusual_rsa(c, e, p, q)

# Output results
print(f"Found {len(possible_messages)} possible plaintexts:")
for i, m in enumerate(possible_messages, 1):
    print(f"\nOption {i}:")
    print(f"Decimal: {m}")
    try:
        hex_msg = hex(m)[2:]
        if len(hex_msg) % 2 != 0:
            hex_msg = '0' + hex_msg
        bytes_msg = bytes.fromhex(hex_msg)
        print(f"ASCII: {bytes_msg.decode('utf-8', errors='replace')}")
    except:
        print("Could not convert to ASCII")