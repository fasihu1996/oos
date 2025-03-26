import random

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

def aufgabe4():
    s = "Accelerate"
    t = "Adventure"
    print(s[0:3] + t[3:])

def aufgabe5():
    a = "my zipper is really zippy"
    # Lösung 1
    offset = (a.find("zip"))+3
    short = a[offset:]
    print(short.find("zip") + offset)
    # Lösung 2
    print(a.find("zip", a.find("zip")+1))

def aufgabe6():
    x = random.uniform(0, 10)
    print(x)
    print(int(x))


#aufgabe1()
#aufgabe4()
aufgabe5()

