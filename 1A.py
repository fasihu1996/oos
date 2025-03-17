def aufgabe1():
    a = 7
    x = 3
    print("Original", x)
    a = x
    a = a+1
    print("1. Änderung", x)
    a = x
    x = a
    print("2. Änderung", x)
    x = x + 1
    x = x
    print("3. Änderung: ", x)

aufgabe1()


