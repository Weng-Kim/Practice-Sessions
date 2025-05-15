import base64

data = b'6UOh"Ci=?)?YO%bDff?.0Q1`6FD,5mF#7cFG;3T@ATN8'

try:
    decoded = base64.a85decode(data, adobe=False)
    print("Decoded:", decoded.decode(errors="replace"))
except Exception as e:
    print("Ascii85 decode failed:", e)
