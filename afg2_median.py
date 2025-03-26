def median(a, b, c):
    zahlen = [a, b, c]
    zahlen.sort()
    return zahlen[1]
    # Alternative Lösung mit short circuit evaluation
    # return ((c > a > b or b > a > c) and a) or ((a > b > c or c > b > a) and b) or c

