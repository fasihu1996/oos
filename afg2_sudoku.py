def check_sudoku(square, limit):
    """Diese Funktion akzeptiert eine quadratisch verschachtelte Liste, sowie ein
    Limit als Größe der einzelen Quadratboxen. Sie geht jede Reihe, Spalte und Box
    durch und fügt einzigartige Zahlen einer Menge hinzu. Falls eine Zahl zweimal
    auftaucht, wird False und die Fehlerstelle ausgegeben."""
    size = len(square)
    rows = set()
    columns = set()
    boxes = set()

    # Jede Reihe auf Gültigkeit prüfen
    for i in range(size):
        for j in range(size):
            value = square[i][j]
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


if __name__ == '__main__':
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

    sudoku_large = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
               [6, 0, 0, 1, 9, 5, 0, 0, 0],
               [0, 9, 8, 0, 0, 0, 0, 6, 0],
               [8, 0, 0, 0, 6, 0, 0, 0, 3],
               [4, 0, 0, 8, 0, 3, 0, 0, 1],
               [7, 0, 0, 0, 2, 0, 0, 0, 6],
               [0, 6, 0, 0, 0, 0, 2, 8, 0],
               [0, 0, 0, 4, 1, 9, 0, 0, 5],
               [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    print(check_sudoku(sudoku_invalid, 2))
    print(check_sudoku(sudoku_valid, 2))
    print(check_sudoku(sudoku_large, 3))

