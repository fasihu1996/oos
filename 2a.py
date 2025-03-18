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

def check_sudoku(square):
    size = len(square)
    i = j = 0
    k = l = 0
    rows = set()
    columns = set()
    print("Zeilen: ")
    while i < size:
        while j < size:
            value = square[i][j]
            print(value)
            if value != 0:
                if value in rows:
                    return False
                else:
                    rows.add(value)
            j+=1
        rows.clear()
        i+=1
        j = 0
    print("Spalten: ")
    i = j = 0
    while i < size:
        while j < size:
            value = square[j][i]
            print(value)
            if value != 0:
                if value in columns:
                    return False
                else:
                    columns.add(value)
            j += 1
        columns.clear()
        i += 1
        j = 0
    return True


sudoku = [[4,2,3,1],
          [2,0,0,0],
          [1,3,2,0],
          [3,0,3,2]
]

sudoku2 = [[4,2,3,1,5,6],
           [2,0,0,0,6,5],
           [1,3,2,0,0,0],
           [0,0,0,0,0,0],
           [0,0,4,0,0,0],
           [3,0,1,2,5,0]
]
print(check_sudoku(sudoku2))

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