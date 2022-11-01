s = input()
Len = len(s)
if Len % 4 == 3:
    bl = "True"
else:
    bl = "False"
max = 0
min = Len
k = 0
l = 0
q = 0
for i in list(s):
    s_new = s[:2 * q + 1]
    dct = {i : list(s_new).count(i) for i in set(s_new)}
    people = 0
    for p in dct.values():
        people += (p % 2)
    if q % 2 != 0:
        people -= 1
    if people > max and q < Len:
        max = people
        k = q
    if people < min and q > 1:
        min = people
        l = q
    q += 1
if min == 0 and l > Len / 2:
    l = -1
print(bl, l + 1, k + 1)
