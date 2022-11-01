def find_anna(s):
    a1 = 'anna' in s
    a2 = 'annA' in s
    a3 = 'anNa' in s
    a4 = 'anNA' in s
    a5 = 'aNna' in s
    a6 = 'aNnA' in s
    a7 = 'aNNa' in s
    a8 = 'aNNA' in s
    b1 = 'Anna' in s
    b2 = 'AnnA' in s
    b3 = 'AnNa' in s
    b4 = 'AnNA' in s
    b5 = 'ANna' in s
    b6 = 'ANnA' in s
    b7 = 'ANNa' in s
    b8 = 'ANNA' in s
    A = a1 or a2 or a3 or a4 or a5 or a6 or a7 or a8
    B = b1 or b2 or b3 or b4 or b5 or b6 or b7 or b8
    return A or B


def weak_or_strong(password):
    lst = list(password)
    st = set(lst)
    if len(st) < 4 or len(password) < 8:
        return 'weak'
    if find_anna(password):
        return 'weak'
    a = password.isupper()
    b = password.islower()
    if a or b:
        return 'weak'
    if any(char.isdigit() for char in password):
        return 'strong'
    return 'weak'

password = input()
print(weak_or_strong(password))

