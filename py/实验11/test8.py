import pandas as pd

file_path = '2018世界杯球队数据.csv' 
try:
    df = pd.read_csv(file_path, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='gbk')

print("--- (2) 净胜球大于0的球队 ---")
mask_gd = (df['进球'] - df['失球']) > 0
print(df[mask_gd]['球队'].values)

print("\n--- (3) 被罚红牌的球队 ---")
mask_red = df['红牌'] > 0
print(df[mask_red]['球队'].values)

print("\n--- (4) 进球成功率超过10%的球队及其进球数和射门数 ---")
mask_rate = (df['进球'] / df['射门']) > 0.1
print(df[mask_rate][['球队', '进球', '射门']])

print("\n--- (5) 进球数超过平均数且被罚黄牌少于5张的球队及其进球数和黄牌数 ---")
mean_goals = df['进球'].mean()
mask_complex = (df['进球'] > mean_goals) & (df['黄牌'] < 5)
print(df[mask_complex][['球队', '进球', '黄牌']])

print("\n--- (6) 按照进球数降序输出所有球队及进球信息 ---")
print(df[['球队', '进球']].sort_values(by='进球', ascending=False))

print("\n--- (7) 按照所属区进行分组，按升序统计输出每个区的进球数 ---")
print(df.groupby('所属洲')['进球'].sum().sort_values(ascending=True))
