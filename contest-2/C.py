t = input().split()
N = int(t[0])
M = int(t[1])
for i in range(N):
    s = ''
    for j in range(M):
        s += str((i + 1) * (j + 1)) + ' '
    print(s)
