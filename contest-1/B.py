money = int(input())
percent = int(input())
years = int(input())
result = (1 + percent / 100) ** years
result = int(money * result)
print(result)
