def hauptstaedte():
    countries = (
        {'country': 'United States', 'capital': 'Washington'},
        {'country': 'Germany', 'capital': 'Berlin'},
        {'country': 'France', 'capital': 'Paris', 'language': 'French'},
        {'country': 'Spain', 'capital': 'Madrid'},
    )
    for e in countries:
        print(e['country'], e['capital'], e.get('language'), sep=' - ')

if __name__ == '__main__':
    hauptstaedte()
