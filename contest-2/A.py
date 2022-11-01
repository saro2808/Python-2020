N = int(input())
s = ''
for i in range(1, N + 1):
    if i % 3 == 0 and i % 5 != 0:
        s += 'Fizz'
    if i % 3 != 0 and i % 5 == 0:
        s += 'Buzz'
    if i % 3 == 0 and i % 5 == 0:
        s += 'Fizz Buzz'
    if i % 3 != 0 and i % 5 != 0:
        s += str(i)
    if i < N:
        s += ', '
print(s)
