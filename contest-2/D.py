import math

i = int(input())
k = 1
n = 2
while k < i:
    n += 1
    ind = 0
    for d in range(2, math.floor(math.sqrt(n) + 1)) :
        if n % d == 0:
            ind = 1
    if ind == 0:
        k += 1
print(n)
