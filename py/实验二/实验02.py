import random
a=random.randint(1,6)
b=random.uniform(60,100)
c=random.randint(0,49) * 2 + 1
seq=['0200001','0200002','0200003','0200004']
d=random.sample(seq, 2)
e=random.shuffle(seq)
print(a)
print(b)    
print(c)
print(d)
print(seq)
print(e)