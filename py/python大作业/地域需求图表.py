import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_regional_style_heatmap(df):
    heatmap_data = pd.crosstab(df['地域'], df['服装款式'], values=df['销量'], aggfunc='mean')
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=.5)
    
    plt.title('地域与服装款式需求热力矩阵', fontsize=14)
    plt.ylabel('目标地域')
    plt.xlabel('服装款式')
    plt.show()



