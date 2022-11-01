s1 = input()
s2 = input()
st = set(s2)
for character in st:
    if character != ' ':
        news = s1.replace(character, "")
        s1 = news
print(s1)
