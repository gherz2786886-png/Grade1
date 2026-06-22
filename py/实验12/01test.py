import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
x = [2,3,5,0.1,0.2,0]
labels = list('abcde')
plt.plot(x,'b-')
plt.fugure()
plt.figure()
explode = [0,0,0.1,0.2,0]
plt.pie('x,explode=esplode, labels=labels,autopct=%1.11f')
plt.show()