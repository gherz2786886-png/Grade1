import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

# ===================== 全局配置：中文兼容+绘图样式 =====================
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.dpi'] = 100

# ===================== 1. 生成兼容的女装电商数据集 =====================
def generate_women_clothing_data(n_samples=10000, seed=42):
    """生成与之前逻辑一致的女装电商数据，含时间、地域、款式、促销、销量字段"""
    np.random.seed(seed)
    regions = ['华东', '华南', '华北', '西南', '华中', '西北', '东北']
    styles = ['T恤', '连衣裙', '羽绒服', '牛仔裤', '针织衫', '大衣', '半身裙']
    seasons = ['春', '夏', '秋', '冬']
    
    data = {
        '地域': np.random.choice(regions, n_samples, p=[0.3, 0.25, 0.15, 0.1, 0.1, 0.05, 0.05]),
        '服装款式': np.random.choice(styles, n_samples),
        '季节': np.random.choice(seasons, n_samples),
        '价格': np.round(np.random.lognormal(mean=5.0, sigma=0.8, size=n_samples), 2),
        '折扣力度': np.round(np.random.uniform(0.3, 1.0, n_samples), 2),
    }
    df = pd.DataFrame(data)
    df['价格'] = df['价格'].clip(lower=19.9)
    
    # 大促标签（互斥）
    rand_promo = np.random.rand(n_samples)
    df['是否618'] = (rand_promo < 0.05).astype(int)
    df['是否双11'] = ((rand_promo >= 0.05) & (rand_promo < 0.10)).astype(int)
    # 生成促销类型分类列，用于分组对比
    df['促销类型'] = np.where(
        df['是否618'] == 1, '618大促',
        np.where(df['是否双11'] == 1, '双11大促', '日常')
    )
    
    # 时间字段（近1年随机日期）
    start_date = pd.to_datetime('2025-06-01')
    random_days = np.random.randint(0, 365, n_samples)
    df['销售日期'] = start_date + pd.to_timedelta(random_days, unit='d')
    df['月份'] = df['销售日期'].dt.month  # 提取月份用于趋势图
    
    # 销量生成（注入因果逻辑）
    base_sales = np.random.poisson(lam=50, size=n_samples)
    price_effect = np.exp(-df['价格'] / 500)
    discount_effect = 1 + (1 - df['折扣力度']) * 2.5
    promo_effect = np.where(df['是否618'] == 1, 3.5, np.where(df['是否双11'] == 1, 4.2, 1.0))
    season_effect = np.ones(n_samples)
    season_effect = np.where((df['服装款式'] == '羽绒服') & (df['季节'] == '冬'), 3.0, season_effect)
    season_effect = np.where((df['服装款式'] == '连衣裙') & (df['季节'] == '夏'), 2.5, season_effect)
    
    noise = np.random.normal(0, 5, n_samples)
    final_sales = base_sales * price_effect * discount_effect * promo_effect * season_effect + noise
    df['销量'] = np.maximum(final_sales, 0).astype(int)
    return df

# ===================== 图表1：月度销量趋势折线图 =====================
def plot_monthly_sales_trend(df):
    """
    用途：展示女装销量随时间的变化规律，分析淡旺季、大促节点的需求波动
    对应分析：需求分布-时间维度
    """
    # 按月统计总销量
    monthly_sales = df.groupby('月份')['销量'].sum().reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='月份', y='销量', data=monthly_sales, 
                 marker='o', linewidth=3, color='#1f77b4', markersize=8)
    
    # 标注大促节点
    plt.scatter([6, 11], [monthly_sales.loc[monthly_sales['月份']==6, '销量'].values[0],
                          monthly_sales.loc[monthly_sales['月份']==11, '销量'].values[0]],
                color='red', s=150, zorder=5, label='大促节点')
    
    plt.title('女装电商月度销量趋势图', fontsize=16, pad=20)
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('总销量（件）', fontsize=12)
    plt.xticks(range(1, 13))
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

# ===================== 图表2：促销×款式分组柱状图 =====================
def plot_promo_style_grouped_bar(df):
    """
    用途：对比日常/618/双11三种促销下，不同服装款式的销量差异
    对应分析：控制变量法-促销+款式交叉影响
    """
    # 按促销类型+款式聚合平均销量
    promo_style_sales = df.groupby(['促销类型', '服装款式'])['销量'].mean().reset_index()
    
    plt.figure(figsize=(14, 7))
    sns.barplot(x='服装款式', y='销量', hue='促销类型', data=promo_style_sales,
                palette=['#95a5a6', '#3498db', '#e74c3c'], edgecolor='white')
    
    plt.title('不同促销类型下各服装款式平均销量对比', fontsize=16, pad=20)
    plt.xlabel('服装款式', fontsize=12)
    plt.ylabel('平均销量（件）', fontsize=12)
    plt.legend(title='促销类型', fontsize=10)
    plt.xticks(rotation=0)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

# ===================== 图表5：折扣力度-销量散点图（带回归线） =====================
def plot_discount_sales_scatter(df):
    """
    用途：直观展示折扣力度与销量的相关性，验证价格弹性
    对应分析：影响因素挖掘-营销因素
    """
    plt.figure(figsize=(12, 6))
    # 散点+回归线
    sns.regplot(x='折扣力度', y='销量', data=df.sample(2000, random_state=42),  # 采样避免点过密
                scatter_kws={'alpha': 0.4, 'color': '#2ecc71'}, 
                line_kws={'color': '#e67e22', 'linewidth': 3})
    
    plt.title('折扣力度与女装销量相关性散点图', fontsize=16, pad=20)
    plt.xlabel('折扣力度（数值越小，优惠力度越大）', fontsize=12)
    plt.ylabel('销量（件）', fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

# ===================== 图表8：3D响应面图（价格×折扣→销量） =====================
def plot_3d_response_surface(df):
    """
    用途：展示价格、折扣力度双因素对销量的交互影响，对应响应面分析法
    对应分析：特征工程-双因素交互效应、创新点响应面分析
    """
    # 采样+拟合二次响应面
    sample_df = df.sample(3000, random_state=42)
    X = sample_df[['价格', '折扣力度']].values
    y = sample_df['销量'].values
    
    # 二元二次多项式拟合（响应面核心）
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, y)
    
    # 生成网格数据绘制曲面
    x_range = np.linspace(X[:, 0].min(), X[:, 0].max(), 50)
    y_range = np.linspace(X[:, 1].min(), X[:, 1].max(), 50)
    X_grid, Y_grid = np.meshgrid(x_range, y_range)
    grid_data = np.c_[X_grid.ravel(), Y_grid.ravel()]
    Z_grid = model.predict(poly.transform(grid_data)).reshape(X_grid.shape)
    
    # 绘制3D图
    fig = plt.figure(figsize=(14, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # 曲面+散点
    surf = ax.plot_surface(X_grid, Y_grid, Z_grid, cmap='viridis', alpha=0.7, edgecolor='none')
    ax.scatter(X[:, 0], X[:, 1], y, color='red', alpha=0.3, s=10, label='实际样本')
    
    ax.set_xlabel('商品价格（元）', fontsize=11, labelpad=10)
    ax.set_ylabel('折扣力度', fontsize=11, labelpad=10)
    ax.set_zlabel('预测销量（件）', fontsize=11, labelpad=10)
    ax.set_title('价格-折扣-销量 三维响应面图', fontsize=16, pad=20)
    fig.colorbar(surf, shrink=0.5, aspect=10, label='销量高低')
    ax.legend()
    plt.tight_layout()
    plt.show()

# ===================== 主函数：一键生成4张图表 =====================
if __name__ == "__main__":
    # 生成数据集（替换为真实数据时，注释本行，改用 pd.read_csv/Excel 读取）
    df = generate_women_clothing_data()
    print(f"数据集加载完成，共 {len(df)} 条样本")
    
    # 依次生成4张图表
    print("\n[1/4] 生成月度销量趋势折线图...")
    plot_monthly_sales_trend(df)
    
    print("[2/4] 生成促销×款式分组柱状图...")
    plot_promo_style_grouped_bar(df)
    
    print("[3/4] 生成折扣-销量散点图...")
    plot_discount_sales_scatter(df)
    
    print("[4/4] 生成3D响应面图...")
    plot_3d_response_surface(df)
    
    print("\n所有图表生成完成！")