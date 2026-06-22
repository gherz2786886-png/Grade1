import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ===================== 1. 跨系统中文字体配置（兼容Windows/macOS/Linux） =====================
def configure_chinese_font():
    sys_os = plt.matplotlib.get_backend()  # 兼容不同系统字体检测
    if 'Windows' in plt.matplotlib.rcParams['backend']:
        fonts = ['Microsoft YaHei', 'SimHei']
    elif 'macOS' in plt.matplotlib.rcParams['backend'] or 'Darwin' in plt.matplotlib.rcParams['backend']:
        fonts = ['Arial Unicode MS', 'PingFang SC']
    else:  # Linux
        fonts = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC']
    
    plt.rcParams['font.sans-serif'] = fonts
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    plt.style.use('seaborn-v0_8-whitegrid')
    print(f"[字体配置] 已加载适配字体: {fonts[0]}")

# ===================== 2. 生成电商示例数据（复用业务逻辑，可替换为真实数据） =====================
def generate_ecommerce_data(n_samples=10000, seed=42):
    """生成包含地域、款式、促销、销量的电商示例数据"""
    np.random.seed(seed)
    regions = ['华东', '华南', '华北', '西南', '华中', '西北', '东北']
    styles = ['T恤', '连衣裙', '羽绒服', '牛仔裤', '针织衫', '大衣', '半身裙']
    seasons = ['春', '夏', '秋', '冬']
    
    # 基础数据生成
    data = {
        '地域': np.random.choice(regions, n_samples, p=[0.3, 0.25, 0.15, 0.1, 0.1, 0.05, 0.05]),
        '服装款式': np.random.choice(styles, n_samples),
        '季节': np.random.choice(seasons, n_samples),
        '价格': np.round(np.random.lognormal(mean=5.0, sigma=0.8, size=n_samples), 2),
        '折扣力度': np.round(np.random.uniform(0.3, 1.0, n_samples), 2),
    }
    df = pd.DataFrame(data)
    
    # 618促销标签 + 销量因果逻辑
    rand_promo = np.random.rand(n_samples)
    df['是否618'] = (rand_promo < 0.05).astype(int)  # 5%数据为618促销
    base_sales = np.random.poisson(lam=50, size=n_samples)
    discount_effect = 1 + (1 - df['折扣力度']) * 2.5  # 折扣越大（数值越小）销量越高
    promo_effect = np.where(df['是否618'] == 1, 3.5, 1.0)  # 618销量提升3.5倍
    df['销量'] = np.maximum(base_sales * discount_effect * promo_effect + np.random.normal(0, 5, n_samples), 0).astype(int)
    
    return df

# ===================== 3. 地域-款式需求热力图 =====================
def plot_regional_style_heatmap(df):
    """
    绘制地域与服装款式的销量热力图
    :param df: 包含「地域」「服装款式」「销量」列的DataFrame
    """
    # 按地域+款式聚合平均销量
    heatmap_data = pd.crosstab(df['地域'], df['服装款式'], values=df['销量'], aggfunc='mean')
    
    # 绘制热力图
    plt.figure(figsize=(12, 8))
    sns.heatmap(
        heatmap_data, 
        annot=True,        # 显示数值
        fmt=".0f",         # 数值格式（无小数）
        cmap="YlGnBu",     # 配色方案
        linewidths=.5,     # 格子边框宽度
        cbar_kws={'label': '平均销量（件）'}  # 色条标签
    )
    
    plt.title('地域与服装款式需求热力矩阵', fontsize=16, pad=20)
    plt.ylabel('目标地域', fontsize=12)
    plt.xlabel('服装款式', fontsize=12)
    plt.xticks(rotation=30, ha='right')  # 款式名称旋转，避免重叠
    plt.tight_layout()  # 自适应布局
    plt.show()

# ===================== 4. 618促销-销量&折扣双轴分析图 =====================
def plot_promo_analysis(df):
    """
    绘制618促销对销量+折扣力度的双轴分析图
    :param df: 包含「是否618」「销量」「折扣力度」列的DataFrame
    """
    # 按618分组聚合平均销量/折扣
    promo_stats = df.groupby('是否618').agg({'销量': 'mean', '折扣力度': 'mean'})
    
    # 双轴图绘制
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # 左轴：销量（柱状图）
    color1 = 'tab:blue'
    ax1.set_xlabel('促销类型', fontsize=12)
    ax1.set_ylabel('平均销量 (件)', color=color1, fontsize=12)
    ax1.bar(
        ['日常', '618'], 
        promo_stats['销量'], 
        color=color1, 
        alpha=0.6, 
        width=0.5
    )
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(0, promo_stats['销量'].max() * 1.2)  # 留出顶部空间
    
    # 右轴：折扣力度（折线图）
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('平均折扣力度 (数值越小越优惠)', color=color2, fontsize=12)
    ax2.plot(
        ['日常', '618'], 
        promo_stats['折扣力度'], 
        color=color2, 
        marker='o', 
        linewidth=3, 
        markersize=8
    )
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(promo_stats['折扣力度'].min() * 0.8, promo_stats['折扣力度'].max() * 1.2)
    
    # 标题与布局
    plt.title('618促销活动对销量与折扣力度的联合效应', fontsize=16, pad=20)
    plt.tight_layout()
    plt.show()

# ===================== 主函数：一键运行所有图表 =====================
if __name__ == "__main__":
    # 1. 初始化配置
    configure_chinese_font()
    
    # 2. 生成数据（替换为 pd.read_excel('你的真实数据.xlsx') 即可使用真实数据）
    df = generate_ecommerce_data(n_samples=10000)
    print(f"[数据加载完成] 数据量：{len(df)} 条")
    print(df[['地域', '服装款式', '是否618', '销量', '折扣力度']].head())
    
    # 3. 绘制地域热力图
    print("\n[绘制图表1] 地域-款式需求热力图...")
    plot_regional_style_heatmap(df)
    
    # 4. 绘制促销分析图
    print("[绘制图表2] 618促销-销量&折扣双轴图...")
    plot_promo_analysis(df)