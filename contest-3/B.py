s = input()
L = len(s)
st = set(s)
st = sorted(st)
for i in st:
    max = 0
    for j in range(L):
        k = 0
        while s[j] == i:
            if j == L - 1:
                k += 1
                if max < k:
                    max = k
                break
            j += 1
            k += 1
        if max < k:
            max = k
    print(i, max)
