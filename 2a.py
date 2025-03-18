def aufgabe2(zahl1, zahl2, zahl3):
    zahlen = [zahl1, zahl2, zahl3]
    zahlen.sort()
    return zahlen[1]

ein1 = int(input("Zahl1: "))
ein2 = int(input("Zahl2: "))
ein3 = int(input("Zahl3: "))
print(aufgabe2(ein1, ein2, ein3))