a = input()
b = max(a[0], a[1], a[2])
c = min(a[0], a[1], a[2])
d = a
b = 3 * b + 3 * '9'
c = 3 * c + 3 * '0'

while int(d) >= int(c) and int(d[0]) + int(d[1]) + int(d[2]) != int(d[3]) + int(d[4]) + int(d[5]):
    d = str(int(d) - 1)

e = int(d)
d = a

while ((int(d) <= int(b)) and (int(d[0]) + int(d[1]) + int(d[2]) != int(d[3]) + int(d[4]) + int(d[5]))) :
    d = str(int(d) + 1)

f = int(d)
a = int(a)

if (a - e <= f - a) :
    print(e)
else :
    print(f)
