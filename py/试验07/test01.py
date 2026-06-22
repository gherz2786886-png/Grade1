a = {1,2,3,4,5}
b = {2,4,6}
c = a & b
print("属于a但不属于b的元素：", a - b)
print('属于a，b的元素：',a | b)
print('属于ab之一的元素：',a ^ b)