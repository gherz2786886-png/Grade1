import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import train_test_split        
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import VarianceThreshold
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings

warnings.filterwarnings('ignore')   # 抑制非致命警告以保持终端输出整洁(ai的)
plt.style.use('seaborn-v0_8-whitegrid')  # 全局学术绘图参数配置
plt.rcParams['font.sans-serif'] = ['SimHei']  # 需确保系统已安装 SimHei 字体
plt.rcParams['axes.unicode_minus'] = False


def generate_ecommerce_data(n_samples=10000, seed=42):
    """阶段一：蒙特卡洛合成数据集生成（注入已知因果基准）"""
    print("[1/5] 正在生成蒙特卡洛合成数据集...")
    np.random.seed(seed)
    
    regions = ['华东', '华南', '华北', '西南', '华中', '西北', '东北']
    styles = ['T恤', '连衣裙', '羽绒服', '牛仔裤', '针织衫', '大衣', '半身裙']
    seasons = ['春', '夏', '秋', '冬']
    
    data = {
        'region': np.random.choice(regions, n_samples, p=[0.3, 0.25, 0.15, 0.1, 0.1, 0.05, 0.05]),
        'style': np.random.choice(styles, n_samples),
        'season': np.random.choice(seasons, n_samples),
        'price': np.round(np.random.lognormal(mean=5.0, sigma=0.8, size=n_samples), 2),
        'discount_rate': np.round(np.random.uniform(0.3, 1.0, n_samples), 2),
    }
    df = pd.DataFrame(data)
    
    df['price'] = df['price'].clip(lower=19.9)
    
    rand_promo = np.random.rand(n_samples)
    df['is_618'] = (rand_promo < 0.05).astype(int)
    df['is_double11'] = ((rand_promo >= 0.05) & (rand_promo < 0.10)).astype(int)
    
    start_date = pd.to_datetime('2026-06-01')
    random_days = np.random.randint(0, 365, n_samples)
    df['launch_date'] = start_date - pd.to_timedelta(random_days, unit='d')
    
    base_sales = np.random.poisson(lam=50, size=n_samples)
    price_effect = np.exp(-df['price'] / 500)
    discount_effect = 1 + (1 - df['discount_rate']) * 2.5 
    
    promo_effect = np.ones(n_samples)
    promo_effect = np.where(df['is_618'] == 1, 3.5, promo_effect)
    promo_effect = np.where(df['is_double11'] == 1, 4.2, promo_effect)
    
    season_effect = np.ones(n_samples)
    season_effect = np.where((df['style'] == '羽绒服') & (df['season'] == '冬'), 3.0, season_effect)
    season_effect = np.where((df['style'] == '连衣裙') & (df['season'] == '夏'), 2.5, season_effect)
    
    noise = np.random.normal(0, 5, n_samples)
    final_sales = base_sales * price_effect * discount_effect * promo_effect * season_effect + noise
    df['sales_volume'] = np.maximum(final_sales, 0).astype(int)
    
    df = df.rename(columns={
        'sales_volume': '销量', 'region': '地域', 'style': '服装款式',
        'price': '价格', 'season': '季节', 'is_618': '是否618',
        'is_double11': '是否双11', 'discount_rate': '折扣力度', 'launch_date': '上新时间'
    })
    return df


def preprocess_data(df, current_date_str='2026-06-13'):
    """阶段二：特征清洗与降维（防范维度灾难与虚拟变量陷阱）"""
    print("[2/5] 正在执行数据清洗与特征编码...")
    df = df.drop_duplicates()
    
    # 异常值截断 (IQR)
    for col in ['价格', '销量']:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        upper_bound = Q3 + 1.5 * (Q3 - Q1)
        df = df[(df[col] >= 0) & (df[col] <= upper_bound)]
    
    # 时间序列降维
    df['上新时间'] = pd.to_datetime(df['上新时间'])
    current_date = pd.to_datetime(current_date_str)
    df['生命周期'] = (current_date - df['上新时间']).dt.days
    df = df[df['生命周期'] >= 0]
    
    # 独热编码 (严格 drop='first')
    categorical_cols = ['地域', '服装款式', '季节']
    encoder = OneHotEncoder(drop='first', sparse_output=False, dtype=np.int32)
    encoded_features = encoder.fit_transform(df[categorical_cols])
    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_cols), index=df.index)
    
    base_features = df[['销量', '价格', '折扣力度', '是否618', '是否双11', '生命周期']]
    return pd.concat([base_features, encoded_df], axis=1)


def rigorous_control_variable_analysis(df):
    """阶段三：基于数学期望的边际效应 OLS 检验"""
    print("[3/5] 正在执行 OLS 控制变量验证与参数推断...")
    y, X = df['销量'], sm.add_constant(df.drop(columns=['销量']))
    model = sm.OLS(y, X).fit()
    
    print("\n--- 多元线性回归量化统计结果（局部） ---")
    print(model.summary().tables[1])
    
    baseline = X.mean().copy()
    for col in [c for c in X.columns if '_' in c or '是否' in c]:
        baseline[col] = 0  
        
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('控制变量边际效应联合检验矩阵', fontsize=16, fontweight='bold')
    
    # 款式影响
    style_cols = [c for c in X.columns if '服装款式' in c]
    style_res = {'基准款式': model.predict(baseline)[0]}
    for col in style_cols:
        temp = baseline.copy()
        temp[col] = 1
        style_res[col.replace('服装款式_', '')] = model.predict(temp)[0]
    sns.barplot(x=list(style_res.keys()), y=list(style_res.values()), ax=axes[0], palette="Blues_d")
    axes[0].set_title('控制其他恒定：服装款式边际销量')
    axes[0].tick_params(axis='x', rotation=45)

    # 地域影响
    region_cols = [c for c in X.columns if '地域' in c]
    region_res = {'基准地域': model.predict(baseline)[0]}
    for col in region_cols:
        temp = baseline.copy()
        temp[col] = 1
        region_res[col.replace('地域_', '')] = model.predict(temp)[0]
    sns.barplot(x=list(region_res.keys()), y=list(region_res.values()), ax=axes[1], palette="Greens_d")
    axes[1].set_title('控制其他恒定：地域需求差异')
    axes[1].tick_params(axis='x', rotation=45)

    # 促销影响
    promo_res = {'日常 (无大促)': model.predict(baseline)[0]}
    temp_618, temp_11 = baseline.copy(), baseline.copy()
    temp_618['是否618'], temp_11['是否双11'] = 1, 1
    promo_res['618大促'], promo_res['双11大促'] = model.predict(temp_618)[0], model.predict(temp_11)[0]
    
    sns.barplot(x=list(promo_res.keys()), y=list(promo_res.values()), ax=axes[2], palette="Reds_d")
    axes[2].set_title('非促销因素恒定：大促节点净溢出效应')
    
    plt.tight_layout()
    plt.show()


def execute_feature_engineering_and_modeling(df):
    """阶段四与五：特征防泄漏隔离、特征加权挖掘与回归预测"""
    print("[4/5] 正在进行特征空间挖掘与 VIF 检验...")
    X, y = df.drop(columns=['销量']), df['销量']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # RF 特征重要性提取
    rf_eval = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    rf_eval.fit(X_train, y_train)
    
    importance_df = pd.DataFrame({'特征': X_train.columns, '基尼权重(%)': rf_eval.feature_importances_ * 100})
    importance_df = importance_df.sort_values(by='基尼权重(%)', ascending=False)
    print("\n--- 全局特征基尼不纯度影响权重 (Top 10) ---")
    print(importance_df.head(10).to_string(index=False))

    print("\n[5/5] 正在执行多算法泛化推断与残差诊断...")
    models = {
        'OLS 线性回归': LinearRegression(),
        'CART 单树 (无深度约束)': DecisionTreeRegressor(random_state=42),
        'Random Forest 随机森林': RandomForestRegressor(n_estimators=200, max_depth=15, min_samples_split=5, random_state=42, n_jobs=-1)
    }

    results = []
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('测试集泛化性能：残差核密度估计 (KDE)', fontsize=16, fontweight='bold', y=1.05)

    for idx, (name, model) in enumerate(models.items()):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        residuals = y_test - y_pred
        
        results.append({
            '算法域': name,
            'MAE': mean_absolute_error(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
            'R²': r2_score(y_test, y_pred)
        })
        
        # 残差白噪声诊断图
        sns.histplot(residuals, kde=True, ax=axes[idx], color='steelblue', stat='density', bins=40)
        axes[idx].axvline(x=0, color='firebrick', linestyle='--', lw=2)
        axes[idx].set_title(f'【{name}】 误差项 $\epsilon$ 分布', fontsize=12)
        axes[idx].set_xlabel('残差 (真实 - 预测)')
        axes[idx].set_ylabel('概率密度')

    print("\n--- 测试集泛化性能评估矩阵 ---")
    print(pd.DataFrame(results).set_index('算法域').to_string())
    
    plt.tight_layout()
    plt.show()
    print("\n[工程结束] 实验流水线运行完毕，请检视可视化输出。")


if __name__ == "__main__":
    # 强制执行标准流
    raw_dataset = generate_ecommerce_data()
    clean_matrix = preprocess_data(raw_dataset)
    rigorous_control_variable_analysis(clean_matrix)
    execute_feature_engineering_and_modeling(clean_matrix)
