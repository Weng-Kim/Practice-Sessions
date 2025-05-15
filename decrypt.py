from collections import Counter

def recover_improved_key(ciphertext):
    # Get all nibbles
    nibbles = []
    for i in range(0, len(ciphertext), 4):
        bytes_stage1 = reverse_stage2(ciphertext[i:i+4])
        for byte in bytes_stage1:
            nibbles.append(byte >> 4)  # high nibble
            nibbles.append(byte & 0xF) # low nibble
    
    nib_counts = Counter(nibbles).most_common()
    
    # Expected frequency order in English (space, E, T, A, O, I, N, etc.)
    expected_order = [
        0x2,  # space high
        0x0,   # space low
        0x4,   # E high
        0x5,   # E low
        0x5,   # T high
        0x4,   # T low
        0x4,   # A high
        0x1,   # A low
    ]
    
    private_key = [None]*16
    used_cipher = set()
    
    # Map most frequent cipher nibbles to expected plaintext nibbles
    for i, (cipher_nib, _) in enumerate(nib_counts[:len(expected_order)]):
        plain_nib = expected_order[i]
        if private_key[plain_nib] is None and cipher_nib not in used_cipher:
            private_key[plain_nib] = cipher_nib
            used_cipher.add(cipher_nib)
    
    # Fill remaining positions
    unused = [x for x in range(16) if x not in private_key]
    for i in range(16):
        if private_key[i] is None:
            private_key[i] = unused.pop(0)
    
    return private_key

def main():
    with open('rbandgptwriteanovel.txt.enc', 'rb') as f:
        ciphertext = f.read()
    
    private_key = recover_improved_key(ciphertext)
    print(f"Improved PRIVATE_KEY: {private_key}")
    
    plaintext = decrypt(ciphertext, private_key)
    decoded = plaintext.decode('latin-1', errors='ignore')
    
    with open('improved_decrypted.txt', 'w', encoding='latin-1') as f:
        f.write(decoded)
    
    # More aggressive flag search
    flag_patterns = ["CYBERTHON{", "CHAPTER", "THE ", "AND ", "THAT "]
    found = False
    for pattern in flag_patterns:
        if pattern in decoded:
            print(f"Found pattern: {pattern}")
            if pattern == "CYBERTHON{":
                flag_end = decoded.index("}", decoded.index(pattern)) + 1
                print(f"FLAG FOUND: {decoded[decoded.index(pattern):flag_end]}")
                found = True
                break
    
    if not found:
        print("Flag not found. Please inspect improved_decrypted.txt manually")
        print("Look for any readable text fragments that might indicate partial decryption")

if __name__ == "__main__":
    main()