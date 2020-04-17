import argparse


parser = argparse.ArgumentParser()
parser.add_argument("part")
parser.add_argument("--cipher")
parser.add_argument("--key")
parser.add_argument("--input-file")
parser.add_argument("--output-file")
parser.add_argument("--text-file")
parser.add_argument("--model-file")
args = parser.parse_args()


def is_latin(s: str) -> bool:
    return (65 <= ord(s) < 91) or (97 <= ord(s) < 123)


def word_to_keyword(s: str, key: str) -> str:
    s_ret = ''
    s_len = len(s)
    k_len = len(key)
    i = 0
    r = 0
    while i < s_len:
        while i < s_len and not is_latin(s[i]):
            s_ret += s[i]
            i += 1

        w_len = 0
        while i < s_len and is_latin(s[i]):
            w_len += 1
            i += 1

        delta = k_len - r
        if delta > w_len:
            s_ret += key[r:w_len + r]
            r = w_len + r
            continue
        #  else:
        s_ret += key[r:k_len]
        q = (w_len - delta) // k_len
        r = (w_len - delta) % k_len
        s_ret += key * q + key[0:r]

    return s_ret


def encode_vigenere(s: str, key: str) -> str:
    s_len = len(s)
    s_ret = ''
    keyed = word_to_keyword(s, key)
    for i in range(s_len):
        if is_latin(s[i]):
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
    s_len = len(s)
    s_new = ''
    key = int(key)
    i = 0
    while i < s_len:
        if not is_latin(s[i]):
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


def code_to_keyword(s: str, key: str) -> str:
    s_ret = ''
    s_len = len(s)
    k_len = len(key)
    i = 0
    r = 0
    while i < s_len:
        while i < s_len and not is_latin(s[i]):
            s_ret += s[i]
            i += 1

        w_len = 0
        while i < s_len and is_latin(s[i]):
            w_len += 1
            i += 1

        delta = k_len - r
        if delta > w_len:
            s_ret += key[r:w_len + r]
            r = w_len + r
            continue
        #  else:
        s_ret += key[r:k_len]
        q = (w_len - delta) // k_len
        r = (w_len - delta) % k_len
        s_ret += key * q + key[0:r]

    return s_ret


def decode_vigenere(s: str, key: str) -> str:
    s_len = len(s)
    s_ret = ''
    keyed = code_to_keyword(s, key)
    for i in range(s_len):
        if is_latin(s[i]):
            if s[i].isupper():
                k = keyed[i].upper()
                index = (ord(s[i]) - ord(k)) % 26 + 65
            else:
                k = keyed[i].lower()
                index = (ord(s[i]) - ord(k)) % 26 + 97
            s_ret += chr(index)
        else:
            s_ret += s[i]
    return s_ret


def decode_caesar(s: str, key: str) -> str:
    s_len = len(s)
    key = int(key)
    s_new = ''
    i = 0
    while i < s_len:
        if not is_latin(s[i]):
            s_new += s[i]
        else:
            if s[i].isupper():
                index = (ord(s[i]) - key - 65) % 26
                s_new += chr(65 + index)
            else:
                index = (ord(s[i]) - key - 97) % 26
                s_new += chr(97 + index)
        i += 1
    return s_new


def read_info() -> str:
    if args.input_file:
        with open(f"{args.input_file}", mode='r') as file:
            string = file.read()
    else:
        string = input()
    return string


def write_info(string: str) -> str:
    if not args.output_file:
        print(string)
    else:
        with open(f"{args.output_file}", mode='w') as file:
            file.write(string)
    return string


def find_caesar(s: str, _each_letter: list) -> list:
    s_len = len(s)
    s_new_list = []
    for key in range(26):
        s_new_list.append('')
        i = 0
        while i < s_len:
            if not is_latin(s[i]):
                s_new_list[key] += s[i]
            else:
                if s[i].isupper():
                    index = (ord(s[i]) - key - 65) % 26
                    s_new_list[key] += chr(65 + index)
                else:
                    index = (ord(s[i]) - key - 97) % 26
                    s_new_list[key] += chr(97 + index)
                _each_letter[key][index] += 1
            i += 1
    return s_new_list
# returns list of all possible strings


def compare_exactness(str_list: list, _each_letter: list, _etalon: list) -> str:
    total = []
    best = 0
    for i in range(26):
        total.append(0)
        for j in range(26):
            total[i] += (_each_letter[i][j] - float(_etalon[j])) ** 2
    for i in range(26):
        if total[i] < total[best]:
            best = i
    return str_list[best]
# takes find_caesar(s) and returns the best match


def count_percentage(letters: list, _all: int) -> list:
    if _all != 0:
        for i in range(26):
            for j in range(26):
                letters[i][j] /= _all  # _all == len(s)
    return letters


if args.part == 'encode':
    s = read_info()
    if args.cipher == 'caesar':
        s_new = encode_caesar(s, args.key)

    else:  # if args.cipher == 'vigenere':
        s_new = encode_vigenere(s, args.key)
    write_info(s_new)

elif args.part == 'decode':
    s = read_info()
    if args.cipher == 'caesar':
        s_new = decode_caesar(s, args.key)

    else:  # if cipher == 'vigenere':
        s_new = decode_vigenere(s, args.key)
    write_info(s_new)

elif args.part == 'train':

    if args.text_file:
        with open(f"{args.text_file}", mode='r') as file:
            s = file.read()
    else:
        s = input()
    total = 0

    __each_letter = []
    for i in range(26):
        __each_letter += [0]
    Len = len(s)
    i = 0
    while i < Len:
        if is_latin(s[i]):
            if s[i].isupper():
                __each_letter[ord(s[i]) - 65] += 1
            else:
                __each_letter[ord(s[i]) - 97] += 1
            total += 1
        i += 1
    _etalon = ''
    for i in range(26):
        _etalon += str(__each_letter[i] / total)
        _etalon += ' '
    with open(f"{args.model_file}", 'w') as file:
        file.write(_etalon)

elif args.part == 'hack':
    with open(f'{args.model_file}', 'r') as file:
        info = file.read()

    etalon = info.split()

    each_letter = []
    for i in range(26):
        each_letter.append([])
        for j in range(26):
            each_letter[i].append(0)

    s = read_info()
    each_letter = count_percentage(each_letter, len(s))
    all_strs = find_caesar(s, each_letter)
    best_str = compare_exactness(all_strs, each_letter, etalon)
    write_info(best_str)
