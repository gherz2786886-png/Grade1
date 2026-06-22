import numpy as np

coeffs = [1, 0, 0, 2, 0, 1]

p = np.Polynomial(coeffs)

x1 = 2
x2 = 5
f_x1 = p(x1)
f_x2 = p(x2)

p_der1 = p.deriv(1)  # 一阶导数
p_der2 = p.deriv(2)  # 二阶导数

print("="*50)
print(f"原多项式 f(x) = {p}")
print("="*50)
print(f"x=2 时，f(2) = {f_x1}")
print(f"x=5 时，f(5) = {f_x2}")
print("="*50)
print(f"一阶导数 f\'(x) = {p_der1}")
print(f"二阶导数 f\'\'(x) = {p_der2}")