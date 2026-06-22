'''NumPy速记
1. 属性：shape形状/ndim维度/size总数/dtype类型
2. 创建：array/arange/zeros/ones/randint
3. 索引：[行,列] / 切片 / 布尔筛选
4. 统计：mean均值/std方差/axis=0列1行
5. 文件：savetxt保存/loadtxt读取'''
import numpy as np
ar = np.ones((9, 9), dtype=int)  
print("修改前的数组：")
print(ar)

ar[0,:] = 0
ar[-1,:] = 0
ar[:,0] = 0
ar[:,-1] = 0
print(f"\nThe new aravge is:\n {ar}")

'''在区间[1, 6]内生成1000个随机整数，统计每个整数出现的次数。'''

ar = np.random.radint(1,6,1000)