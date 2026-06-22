import random
a = random.randint(100,200)
hundred=(a//100)
tens=((a//10) %10)
units=(a%10)
print(hundred)
print(tens)
print(units)
result=hundred**2+tens**2+units**2
print(result)
