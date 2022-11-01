s = input()
s = s.split(' ')
max = 1
for i in s:
    if i != " ":
        k = s.count(i)
    if k > max:
        max = k
mx = max / len(s)
print(mx)
