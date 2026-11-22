import struct

fichier = "S_1.wav"

with open(fichier, "rb") as f:
    h = f.read(44)
    canaux = struct.unpack("<H", h[22:24])
    freq = struct.unpack("<I", h[24:28])
    bits = struct.unpack("<H", h[34:36])
    print("Canaux :", canaux)
    print("Frequence :", freq)
    print("Bits :", bits)