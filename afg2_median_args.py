def med_avg(*args):
    """Diese Funktion akzeptiert eine beliebe Anzahl von Argumenten
    und berechnet den Median und Durchschnitt der Eingaben"""
    zahlen = []
    length = len(args)
    for e in args:
        zahlen.append(e)
    zahlen.sort()
    summe = 0
    for i in zahlen:
        summe += i
    average = summe / length
    if length % 2 == 0:
        med = (zahlen[int(length/2)] + zahlen[int((length/2) + 1)])
    else:
        med = zahlen[int(length/2)]
    return average, med

if __name__ == '__main__':
    print(med_avg(12,69,56,113,1))