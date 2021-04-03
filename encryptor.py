import argparse
import random
import string


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='part', help='what to do')

encode = subparsers.add_parser('encode', help='encode open text')
decode = subparsers.add_parser('decode', help='decode encrypted text')
train = subparsers.add_parser('train', help='train letter distribution info')
hack = subparsers.add_parser('hack', help='hack encrypted text')

encode.add_argument('--cipher', dest='cipher', help='cipher')
encode.add_argument('--key', dest='key', help='key')
encode.add_argument('--input-file', dest='input_file', help='input file')
encode.add_argument('--output-file', dest='output_file', help='output file')

decode.add_argument('--cipher', dest='cipher', help='cipher')
decode.add_argument('--key', dest='key', help='key')
decode.add_argument('--input-file', dest='input_file', help='input file')
decode.add_argument('--output-file', dest='output_file', help='output file')

train.add_argument('--text-file', dest='text_file', help='text file')
train.add_argument('--model-file', dest='model_file', help='model file')

hack.add_argument('--input-file', dest='input_file', help='input file')
hack.add_argument('--output-file', dest='output_file', help='output file')
hack.add_argument('--model-file', dest='model_file', help='model file')

args = parser.parse_args()


baudot_code = {
    'a': 4,
    'b': 9,
    'c': 13,
    'd': 15,
    'e': 2,
    'f': 11,
    'g': 10,
    'h': 14,
    'i': 3,
    'j': 12,
    'k': 28,
    'l': 30,
    'm': 26,
    'n': 27,
    'o': 7,
    'p': 31,
    'q': 29,
    'r': 25,
    's': 17,
    't': 21,
    'u': 5,
    'v': 23,
    'w': 19,
    'x': 18,
    'y': 1,
    'z': 22,
    '0': 0,
    '5': 6,
    '4': 8,
    '3': 16,
    '2': 20,
    '1': 24
}

space_punct_list = string.punctuation + string.whitespace
len_space_punct = len(space_punct_list)


def is_latin(s: str) -> bool:
    return (ord('A') <= ord(s) < ord('A') + 26) or (ord('a') <= ord(s) < ord('a') + 26)


def is_cyrillic(s: str) -> bool:
    return ord('А') <= ord(s) <= ord('Я') or ord('а') <= ord(s) <= ord('я')


def word_to_keyword(s: str, key: str) -> str:
    s_ret = ''
    s_len = len(s)
    k_len = len(key)
    i = 0
    r = 0
    while i < s_len:
        while i < s_len and not is_latin(s[i]) and not is_cyrillic(s[i]) and s[i] not in space_punct_list:
            s_ret += s[i]
            i += 1

        w_len = 0
        while i < s_len and (is_latin(s[i]) or is_cyrillic(s[i]) or s[i] in space_punct_list):
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
                index = (ord(s[i]) + ord(k) - 2 * ord('A')) % 26 + ord('A')
            else:
                k = keyed[i].lower()
                index = (ord(s[i]) + ord(k) - 2 * ord('a')) % 26 + ord('a')
            s_ret += chr(index)
        elif is_cyrillic(s[i]):
            if s[i].isupper():
                k = keyed[i].upper()
                index = (ord(s[i]) + ord(k) - 2 * ord('А')) % 32 + ord('А')
            else:
                k = keyed[i].lower()
                index = (ord(s[i]) + ord(k) - 2 * ord('а')) % 32 + ord('а')
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

        if not is_latin(s[i]) and not is_cyrillic(s[i]) and s[i] not in space_punct_list:
            s_new += s[i]
            i += 1
            continue
        if is_latin(s[i]):
            if s[i].isupper():
                index = (ord(s[i]) + key - ord('A')) % 26
                s_new += chr(ord('A') + index)
            else:
                index = (ord(s[i]) + key - ord('a')) % 26
                s_new += chr(ord('a') + index)
        elif is_cyrillic(s[i]):
            if s[i].isupper():
                index = (ord(s[i]) + key - ord('А')) % 32
                s_new += chr(ord('А') + index)
            else:
                index = (ord(s[i]) + key - ord('а')) % 32
                s_new += chr(ord('а') + index)
        elif s[i] in space_punct_list:
            s_new += space_punct_list[(key + space_punct_list.index(s[i])) % len_space_punct]
        i += 1
    return s_new


def decode_vigenere(s: str, key: str) -> str:
    s_len = len(s)
    s_ret = ''
    keyed = word_to_keyword(s, key)
    for i in range(s_len):
        if is_latin(s[i]):
            if s[i].isupper():
                k = keyed[i].upper()
                index = (ord(s[i]) - ord(k)) % 26 + ord('A')
            else:
                k = keyed[i].lower()
                index = (ord(s[i]) - ord(k)) % 26 + ord('a')
            s_ret += chr(index)
        elif is_cyrillic(s[i]):
            if s[i].isupper():
                k = keyed[i].upper()
                index = (ord(s[i]) - ord(k)) % 32 + ord('А')
            else:
                k = keyed[i].lower()
                index = (ord(s[i]) - ord(k)) % 32 + ord('а')
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
        if is_latin(s[i]):
            if s[i].isupper():
                index = (ord(s[i]) - key - ord('A')) % 26
                s_new += chr(ord('A') + index)
            else:
                index = (ord(s[i]) - key - ord('a')) % 26
                s_new += chr(ord('a') + index)
        elif is_cyrillic(s[i]):
            if s[i].isupper():
                index = (ord(s[i]) - key - ord('А')) % 32
                s_new += chr(ord('А') + index)
            else:
                index = (ord(s[i]) - key - ord('а')) % 32
                s_new += chr(ord('а') + index)
        elif s[i] in space_punct_list:
            s_new += space_punct_list[(space_punct_list.index(s[i]) - key) % len_space_punct]
        else:
            s_new += s[i]
        i += 1
    return s_new


def read_info() -> str:
    if args.input_file:
        try:
            with open(f"{args.input_file}", mode='r') as file:
                string = file.read()
        except OSError:
            print("error: could not open/read file")
    else:
        string = input()
    return string


def write_info(string: str):
    if args.output_file:
        try:
            with open(f"{args.output_file}", mode='w') as file:
                file.write(string)
        except OSError:
            print(f"error: could not open file {file} to write")
    else:
        print(string)
    return


# returns list of all possible strings
def find_caesar(s: str, _each_letter: list) -> list:
    s_len = len(s)
    s_new_list = []
    j = 0
    while j < len(s) and not is_latin(s[j]) and not is_cyrillic(s[j]):
        j += 1
    if is_latin(s[j]):
        for key in range(26):
            s_new_list.append('')
            i = 0
            while i < s_len:
                if is_latin(s[i]):
                    if s[i].isupper():
                        index = (ord(s[i]) - key - ord('A')) % 26
                        s_new_list[key] += chr(ord('A') + index)
                    else:
                        index = (ord(s[i]) - key - ord('a')) % 26
                        s_new_list[key] += chr(ord('a') + index)
                    _each_letter[key][index] += 1
                elif s[i] in space_punct_list:
                    s_new_list[key] += space_punct_list[(space_punct_list.index(s[i]) - key) % len_space_punct]
                else:
                    s_new_list[key] += s[i]
                i += 1
    elif is_cyrillic(s[j]):
        for key in range(32):
            s_new_list.append('')
            i = 0
            while i < s_len:
                if is_cyrillic(s[i]):
                    if s[i].isupper():
                        index = (ord(s[i]) - key - ord('А')) % 32
                        s_new_list[key] += chr(ord('А') + index)
                    else:
                        index = (ord(s[i]) - key - ord('а')) % 32
                        s_new_list[key] += chr(ord('а') + index)
                    _each_letter[key][index] += 1
                elif s[i] in space_punct_list:
                    s_new_list[key] += space_punct_list[(space_punct_list.index(s[i]) - key) % len_space_punct]
                else:
                    s_new_list[key] += s[i]
                i += 1
    return s_new_list


# takes find_caesar(s) and returns the best match
def compare_exactness(str_list: list, _each_letter: list, _etalon: list, alphabet_length: int) -> str:
    total = []
    best = 0
    if alphabet_length == 0:
        return 'error: your text does not contain any letters'
    for i in range(alphabet_length):
        total.append(0)
        for j in range(alphabet_length):
            total[i] += (_each_letter[i][j] - float(_etalon[j])) ** 2
    for i in range(alphabet_length):
        if total[i] < total[best]:
            best = i
    return str_list[best]


def count_percentage(letters: list, _all: int, alphabet_length: int) -> list:
    if _all != 0:
        for i in range(alphabet_length):
            for j in range(alphabet_length):
                letters[i][j] /= _all  # _all == len(s)
    return letters


# generates random key for Vernam cipher
def generate_key_vernam(s: str) -> str:
    key = ''
    for i in s:
        if i in baudot_code:
            key += get_key(random.randint(0, 32))
    return key


# checks if the Vernam key has the same length as the text
# and if the key consists of only Baudot symbols
def check_key_correctness(s: str, key: str) -> bool:
    total = 0
    for i in key:
        if i not in baudot_code:
            return False
    for i in s:
        if i in baudot_code:
            total += 1
    if total == len(key):
        return True
    return False


def get_key(val: int) -> str:
    for key, value in baudot_code.items():
        if value == val:
            return key


def encode_decode_vernam(s: str, key: str) -> str:
    s_new = ''
    i = 0
    i_key = 0
    while i < len(s):
        while i < len(s) and s[i] not in baudot_code:
            s_new += s[i]
            i += 1
        if i == len(s):
            break
        if s[i].isupper():
            s_new += chr(ord('A') - ord('a') +
                         ord(str(get_key(baudot_code[s[i].lower()] ^ baudot_code[key[i_key].lower()]))))
        else:
            s_new += str(get_key(baudot_code[s[i]] ^ baudot_code[key[i_key].lower()]))
        i += 1
        i_key += 1
    return s_new


def train():
    if args.text_file:
        try:
            with open(f"{args.text_file}", mode='r') as file:
                s = file.read()
        except OSError:
            print(f"error: could not open/read file {args.text_file}")
    else:
        s = input()

    j = 0
    while j < len(s) and not is_cyrillic(s[j]) and not is_latin(s[j]):
        j += 1
    alphabet_length = 32 * is_cyrillic(s[j]) + 26 * is_latin(s[j])
    total = 0
    _each_letter = [0] * alphabet_length
    s_len = len(s)
    i = 0
    while i < s_len:
        if is_latin(s[i]):
            if s[i].isupper():
                _each_letter[ord(s[i]) - ord('A')] += 1
            else:
                _each_letter[ord(s[i]) - ord('a')] += 1
            total += 1
        elif is_cyrillic(s[i]):
            if s[i].isupper():
                _each_letter[ord(s[i]) - ord('А')] += 1
            else:
                _each_letter[ord(s[i]) - ord('а')] += 1
            total += 1
        i += 1
    if total > 0:
        _etalon = ''
        for i in range(alphabet_length):
            _etalon += str(_each_letter[i] / total)
            _etalon += ' '
        with open(f"{args.model_file}", 'w') as file:
            file.write(_etalon)
    else:
        print("error: no latin and cyrillic letters found")


def hack():
    try:
        with open(f'{args.model_file}', 'r') as file:
            info = file.read()
    except OSError:
        print(f"error: could not open/read {file}")

    etalon = info.split()
    s = read_info()
    j = 0
    while j < len(s) and not is_cyrillic(s[j]) and not is_latin(s[j]):
        j += 1
    alphabet_length = 0
    if is_latin(s[j]):
        alphabet_length = 26
    elif is_cyrillic(s[j]):
        alphabet_length = 32
    each_letter = [[0] * alphabet_length for _ in range(alphabet_length)]
    each_letter = count_percentage(each_letter, len(s), alphabet_length)
    all_strs = find_caesar(s, each_letter)
    best_str = compare_exactness(all_strs, each_letter, etalon, alphabet_length)
    write_info(best_str)


def main():
    if args.part == 'encode':
        s = read_info()
        s_new = ''
        if args.cipher == 'caesar':
            s_new = encode_caesar(s, args.key)

        elif args.cipher == 'vigenere':
            s_new = encode_vigenere(s, args.key)

        elif args.cipher == 'vernam':
            if args.key:
                if check_key_correctness(s, args.key):
                    s_new = encode_decode_vernam(s, args.key)
                else:
                    print('error: the key should be of the length of the text')
            else:
                key = generate_key_vernam(s)
                s_new = encode_decode_vernam(s, key)
                print(f'The randomly generated key is {key}')

        else:
            print("error: incorrect cipher")
        write_info(s_new)

    elif args.part == 'decode':
        s = read_info()
        s_new = ''
        if args.cipher == 'caesar':
            s_new = decode_caesar(s, args.key)

        elif args.cipher == 'vigenere':
            s_new = decode_vigenere(s, args.key)

        elif args.cipher == 'vernam':
            if not args.key:
                print("error: can't hack Vernam cipher")
                return
            s_new = encode_decode_vernam(s, args.key)

        else:
            print("error: incorrect cipher")
        write_info(s_new)

    elif args.part == 'train':
        train()

    elif args.part == 'hack':
        hack()


if __name__ == '__main__':
    main()

