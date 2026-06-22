import yfinance as yf
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ==========1.定义三大行业标的清单(2026热门美股)==========
industry_dict = {
    "AI半导体科技": ["NVDA", "MSFT", "AAPL", "AMD", "INTC", "TSLA", "AVGO", "QCOM", "AMZN", "META"],
    "生物制药医疗": ["JNJ", "PFE", "MRK", "ABBV", "GILD", "LLY", "AMGN", "BIIB", "REGN", "VTRS"],
    "油气能源": ["XOM", "CVX", "COP", "OXY", "HES", "MRO", "DVN", "APA", "FANG", "CXO"]
}

# 基本面指标列表
factor_cols = ["ROE", "毛利率", "EPS", "PE", "营收增速"]
all_result = []

# ==========2.循环爬取单只股票基本面数据==========
def get_fundamental(symbol):
    """获取单只股票5项基本面"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        # 提取指标，缺失值填充np.nan
        roe = info.get("returnOnEquity", np.nan) * 100 if info.get("returnOnEquity") else np.nan
        gross_margin = info.get("grossMargins", np.nan) * 100 if info.get("grossMargins") else np.nan
        eps = info.get("trailingEps", np.nan)
        pe = info.get("trailingPE", np.nan)
        rev_growth = info.get("revenueGrowth", np.nan) * 100 if info.get("revenueGrowth") else np.nan
        name = info.get("longName", symbol)
        return [symbol, name, roe, gross_margin, eps, pe, rev_growth]
    except Exception as e:
        print(f"{symbol}数据获取异常")
        return [symbol, "缺失名称", np.nan, np.nan, np.nan, np.nan, np.nan]

# 遍历三个行业
for industry_name, ticker_list in industry_dict.items():
    stock_data = []
    for tick in ticker_list:
        res = get_fundamental(tick)
        res.insert(1, industry_name) #插入行业名称
        stock_data.append(res)
    # 当前行业转为DataFrame
    df_ind = pd.DataFrame(stock_data, columns=["代码","行业","公司名"]+factor_cols)
    
    # ==========3.指标标准化+加权打分==========
    df_score = df_ind.copy()
    # 剔除PE为负(亏损无意义)、关键指标大面积空缺个股
    df_score = df_score[df_score["PE"]>0].dropna(subset=["ROE","毛利率","EPS"])
    
    # 正向指标：ROE、毛利率、EPS、营收增速(越大分越高)
    for col in ["ROE","毛利率","EPS","营收增速"]:
        minv = df_score[col].min()
        maxv = df_score[col].max()
        df_score[f"{col}_标准化"] = (df_score[col]-minv)/(maxv-minv) if maxv>minv else 0
    # 反向指标：PE(越小分越高，倒转标准化)
    pe_min = df_score["PE"].min()
    pe_max = df_score["PE"].max()
    df_score["PE_标准化"] = (pe_max - df_score["PE"])/(pe_max-pe_min) if pe_max>pe_min else 0
    
    # 权重设置：ROE(0.3)、毛利率(0.25)、EPS(0.25)、PE(0.1)、营收增速(0.1)
    df_score["综合得分"] = (
        df_score["ROE_标准化"]*0.3 +
        df_score["毛利率_标准化"]*0.25 +
        df_score["EPS_标准化"]*0.25 +
        df_score["PE_标准化"]*0.1 +
        df_score["营收增速_标准化"]*0.1
    )
    # 行业内按综合得分降序排序，取TOP5
    df_top5 = df_score.sort_values("综合得分",ascending=False).head(5)
    all_result.append(df_top5[["代码","行业","公司名","ROE","毛利率","EPS","PE","营收增速","综合得分"]])
    
    # 打印单行业结果
    print(f"\n==========【{industry_name}基本面TOP5上市公司】==========")
    print(df_top5[["代码","公司名","综合得分"]].to_string(index=False))

# ==========4.汇总全行业结果，保存Excel文件==========
final_df = pd.concat(all_result,ignore_index=True)
final_df.to_excel("美股三大行业基本面TOP5汇总.xlsx",index=False)
print("\n数据已保存：美股三大行业基本面TOP5汇总.xlsx")