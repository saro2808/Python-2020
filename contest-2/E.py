t = input()
u = t.split()
n = int(u[0])
q = int(u[1])
s = str(n % q)
n = int(n / q)
while (n > 0) :
    s = s + str(n % q)
    n = int(n / q)
s = s[::-1]
print(s)
