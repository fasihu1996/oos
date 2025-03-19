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

# hauptstaedte()

def check_sudoku(square, limit):
    size = len(square)
    rows = set()
    columns = set()
    boxes = set()

    # Jede Reihe auf Gültigkeit prüfen
    for i in range(size):
        for j in range(size):
            value = square[i][j]
            print(value)
            if value != 0:
                if value in rows:
                    print(f"Das Sudoku enthält einen Reihenfehler in Zeile {i+1} und Spalte {j+1}")
                    return False
                else:
                    rows.add(value)
            j+=1
        rows.clear()

    # Gleicher Loop aber für Spalten
    for i in range(size):
        for j in range(size):
            value = square[j][i]
            print(value)
            if value != 0:
                if value in columns:
                    print(f"Das Sudoku enthält einen Spaltenfehler in Zeile {j+1} und Spalte {i+1}")
                    return False
                else:
                    columns.add(value)
        columns.clear()

    # doppelt verschachtelter Loop, jede Box prüfen, darin jedes Zeile/Spalte prüfen
    for box_row in range(0, size, limit):
        for box_column in range(0, size, limit):
            for i in range (box_column, box_row, limit):
                for j in range (box_column, box_row, limit):
                    value = square[i][j]
                    if value != 0:
                        if value in boxes:
                            print(f"Das Sudoku enthält einen Boxfehler an der Stelle: {i} {j}")
                            return False
                        else:
                            boxes.add(value)
            boxes.clear()

    # falls vorher kein false ausgegeben wurde, ist das Sudoku gültig
    return True


sudoku_invalid = [[4,2,3,1],
                  [2,0,0,0],
                  [1,3,2,0],
                  [3,0,3,2]
]

sudoku_valid = [[4,1,3,2],
                [3,2,4,0],
                [2,4,1,3],
                [1,3,2,4]
]

sudoku2 = [[4,2,3,1,5,6],
           [2,0,0,0,6,5],
           [1,3,2,0,0,0],
           [0,0,0,0,0,0],
           [0,0,4,0,0,0],
           [3,0,1,2,5,0]
]
print(check_sudoku(sudoku_invalid, 2))

def med_avg(*args):
    input = []
    length = len(args)
    for e in args:
        input.append(e)
    input.sort()
    sum = 0
    for i in input:
        sum += i
    average = sum / length
    if length % 2 == 0:
        med = (input[int(length/2)] + input[int((length/2) + 1)])
    else:
        med = input[int(length/2)]
    return average, med

print(med_avg(12,69,56,113,1))