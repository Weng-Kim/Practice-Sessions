import secrets

def makeKey():
  key = list(range(16))
  secrets.SystemRandom().shuffle(key)
  return key

def processblock(block, key):
  block_bytes = block.encode()
  padded = block_bytes.ljust(4)
  stage1 = []
  for byte in padded:
    high = key[(byte >> 4)]
    low = key[(byte & 0xF)]
    out = (high << 4) | low
    stage1.append(bin(out)[2:].zfill(8))
  stage1 = ''.join(stage1)
  stage2 = []
  for i in [2, 8, 24, 6, 5, 20, 29, 1, 14, 23, 7, 28, 12, 31, 11, 22, 3, 26, 0, 4, 15, 27, 19, 9, 21, 18, 17, 16, 30, 10, 13, 25]:
    stage2.append(stage1[i])
  stage2 = ''.join(stage2)
  binary = int(stage2, 2).to_bytes(4, 'big')
  return binary

if __name__ == "__main__":
  PRIVATE_KEY = makeKey()
  print(f"PRIVATE_KEY: {PRIVATE_KEY}")
  plaintext = open("rbandgptwriteanovel.txt").read()
  plaintext = plaintext.upper()
  blocks = [plaintext[i:i+4] for i in range(0, len(plaintext), 4)]
  blocksout = [processblock(block, PRIVATE_KEY) for block in blocks]
  ciphertext = b''.join(blocksout)
  print(f"{len(plaintext)} bytes --> encrypted --> {len(ciphertext)} bytes")
  open("rbandgptwriteanovel.txt.enc", "wb").write(ciphertext)
