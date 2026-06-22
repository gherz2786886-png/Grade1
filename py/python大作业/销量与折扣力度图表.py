import matplotlib.pyplot as plt
import numpy as np

def plot_promo_analysis(df):
    promo_stats = df.groupby('是否618').agg({'销量': 'mean', '折扣力度': 'mean'})
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('是否618促销')
    ax1.set_ylabel('平均销量 (件)', color=color)
    ax1.bar(['日常', '618'], promo_stats['销量'], color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('平均折扣力度 (数值越小越优惠)', color=color)
    ax2.plot(['日常', '618'], promo_stats['折扣力度'], color=color, marker='o', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('促销活动对销量与价格弹性的联合效应', fontsize=14)
    plt.show()