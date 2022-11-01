s = input()
s_rev = s[::-1]
Len = len(s)
left = 0
right = 0
while left < Len:
    sub_s = s[0:left + 1][::-1]
    index = s.find(sub_s)
    tmp = s[0:index + left + 1]
    if index == -1 or tmp != tmp[::-1]:
        break
    left += 1
while right < Len:
    sub_s = s_rev[0:right + 1][::-1]
    index = s_rev.find(sub_s)
    tmp = s_rev[0:index + right + 1]
    if index == -1 or tmp != tmp[::-1]:
        break
    right += 1
m = max(left, right)
print(Len - m)

