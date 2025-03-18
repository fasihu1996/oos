def median(a, b, c):
    zahlen = [a, b, c]
    zahlen.sort()
    return zahlen[1]
    # Alternative Lösung mit short circuit evaluation
    # return ((c > a > b or b > a > c) and a) or ((a > b > c or c > b > a) and b) or c

"""ein1 = int(input("Zahl1: "))
ein2 = int(input("Zahl2: "))
ein3 = int(input("Zahl3: "))
print(aufgabe2(ein1, ein2, ein3))"""

def hauptstaedte():
    countries = (
        {'country': 'United States', 'capital': 'Washington'},
        {'country': 'Germany', 'capital': 'Berlin'},
        {'country': 'France', 'capital': 'Paris', 'language': 'French'},
        {'country': 'Spain', 'capital': 'Madrid'},
    )
    for e in countries:
        print(e['country'], e['capital'], e.get('language'), sep=' - ')

def check_sudoku(square):
    size = len(square)
    for i in range(size):
        for j in range(size):
            if square[i][j] != 0:
                pass

sudoku = [[4,2,3,0],[0,0,0,0],[4,2,3,0],[1,0,1,2]]
hauptstaedte()
