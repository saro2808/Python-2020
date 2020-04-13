import sys


def word_to_keyword(s: str, key: str) -> str:
    slen = len(s)
    klen = len(key)
    q = slen // klen
    r = slen % klen
    s_ret = q * key
    s_ret += key[0:r]
    return s_ret


def word_to_code(s: str, key: str) -> str:
    s_ret = ''
    keyed = word_to_keyword(s, key)
    for i in range(len(s)):
        if s[i].isalpha():
            if s[i].isupper():
                k = keyed[i].upper()
                index = (ord(s[i]) + ord(k) - 2 * 65) % 26 + 65
            else:
                k = keyed[i].lower()
                index = (ord(s[i]) + ord(k) - 2 * 97) % 26 + 97
            s_ret += chr(index)
        else:
            s_ret += s[i]
    return s_ret


def encode_caesar(s: str, key: str) -> str:
    s_new = ''
    key = int(key)
    i = 0
    while i < Len:
        if s[i].isspace():
            s_new += s[i]
        elif not s[i].isalpha():
            s_new += s[i]
        else:
            if s[i].isupper():
                index = (ord(s[i]) + key - 65) % 26
                s_new += chr(65 + index)
            else:
                index = (ord(s[i]) + key - 97) % 26
                s_new += chr(97 + index)
        i += 1
    return s_new


def encode_vigenere(s: str, key: str) -> str:
    s_new = ''
    i = 0
    while i < Len:
        while i < Len and s[i].isspace():
            s_new += s[i]
            i += 1
        start = i
        while i < Len and not s[i].isspace():
            i += 1
        word = word_to_code(s[start:i:1], key)
        s_new += word
    return s_new


cipher = sys.argv[1]
key = sys.argv[2]
arglen = len(sys.argv)
if arglen > 3:
    with open("{}".format(sys.argv[3]), mode='r') as file:
        s = file.read()
else:
    s = input()

Len = len(s)

if cipher == 'caesar':
    s_new = encode_caesar(s, key)

else:  # if cipher == 'vigenere':
    s_new = encode_vigenere(s, key)


if arglen <= 4:
    print(s_new)
else:
    with open("{}".format(sys.argv[4]), mode='w') as file:
        file.write(s_new)
