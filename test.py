from pprint import pprint
def p(words):
    pprint(words)
    print(len(words))
with open('words.txt', 'r') as file:
    lines = file.read()
    words = lines.split('\n')
    for letter in 'aler':
        words_copy = words[:]
        for word in words_copy:
            if letter in word:
                words.remove(word)
    for letter in 't':
        words_copy = words[:]
        for word in words_copy:
            if letter not in word[4]:
                words.remove(word)

    for letter in 's':
        words_copy = words[:]
        for word in words_copy:
            if letter not in word[0]:
                words.remove(word)
    
    for letter in 'n':
        words_copy = words[:]
        for word in words_copy:
            if letter not in word:
                words.remove(word)
    for letter in 't':
        words_copy = words[:]
        for word in words_copy:
            if letter not in word[4]:
                words.remove(word)
    for letter in 'aler':
        words_copy = words[:]
        for word in words_copy:
            if letter in word:
                words.remove(word)

    p(words)

