def small_words(eingabe):
    for e in eingabe:
        if len(e) < 3:
            yield e # das ist schon eine generator funktion
    # g = (yield e for e in eingabe if e.len < 3)

if __name__ == '__main__':
    words = ['a', 'ab', 'abc', 'abcd', 'abcde']
    # res = (word for word in small_words(words)) ## Generator expression, nicht notwendig
    for r in small_words(words): #
        print(r)
