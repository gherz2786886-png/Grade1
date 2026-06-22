x1 = eval (input ("Enter the first number: "))
x2 = eval (input ("Enter the second number: "))
y1 = eval (input ("Enter the third number: "))
y2 = eval (input ("Enter the fourth number: "))
distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
print ("The distance between the two points is", distance)