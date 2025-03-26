def small_words(eingabe):
    for e in eingabe:
        if len(e) < 3:
            yield e
        else:
            yield None
    # g = (yield e for e in eingabe if e.len < 3)

if __name__ == '__main__':
    words = ['a', 'ab', 'abc', 'abcd', 'abcde']
    result = small_words(words)
    for r in result:
        print(r)