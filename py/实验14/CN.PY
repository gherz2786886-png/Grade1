import yfinance as yf
import pandas as pd
import numpy as np
import warnings
import time
warnings.filterwarnings("ignore")

# 三大行业股票清单
industry_dict = {
    "AI半导体科技": ["NVDA", "MSFT", "AAPL", "AMD", "INTC", "TSLA", "AVGO", "QCOM", "AMZN", "META"],
    "生物制药医疗": ["JNJ", "PFE", "MRK", "ABBV", "GILD", "LLY", "AMGN", "BIIB", "REGN", "VTRS"],
    "油气能源": ["XOM", "CVX", "COP", "OXY", "HES", "MRO", "DVN", "APA", "FANG", "CXO"]
}
factor_cols = ["ROE", "毛利率", "EPS", "PE", "营收增速"]
all_result = []

# 优化获取函数：空值容错+延时防风控
def get_fundamental(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        # 分步取值，避免None参与乘法运算
        roe_raw = info.get("returnOnEquity")
        roe = roe_raw * 100 if roe_raw is not None else np.nan
        
        gm_raw = info.get("grossMargins")
        gross_margin = gm_raw * 100 if gm_raw is not None else np.nan
        
        eps = info.get("trailingEps", np.nan)
        pe = info.get("trailingPE", np.nan)
        
        rev_raw = info.get("revenueGrowth")
        rev_growth = rev_raw * 100 if rev_raw is not None else np.nan
        
        name = info.get("longName", symbol)
        time.sleep(0.3) # 每个股票请求间隔0.3秒，防止接口封禁
        return [symbol, name, roe, gross_margin, eps, pe, rev_growth]
    except Exception as e:
        print(f"{symbol}数据获取异常:{str(e)[:40]}")
        return [symbol, "缺失名称", np.nan, np.nan, np.nan, np.nan, np.nan]

# 遍历行业处理数据
for industry_name, ticker_list in industry_dict.items():
    stock_data = []
    for tick in ticker_list:
        res = get_fundamental(tick)
        res.insert(1, industry_name)
        stock_data.append(res)
    df_ind = pd.DataFrame(stock_data, columns=["代码","行业","公司名"]+factor_cols)
    # 剔除PE<=0和关键指标全空的个股
    df_score = df_ind[(df_ind["PE"]>0) & (~df_ind[["ROE","毛利率","EPS"]].isna().all(axis=1))].copy()
    if len(df_score) == 0:
        print(f"\n【{industry_name}】无有效基本面数据，跳过排名")
        continue
    # 正向指标标准化
    for col in ["ROE","毛利率","EPS","营收增速"]:
        minv, maxv = df_score[col].min(), df_score[col].max()
        df_score[f"{col}_标准化"] = (df_score[col]-minv)/(maxv-minv) if maxv>minv else 0
    # PE反向标准化
    pe_min, pe_max = df_score["PE"].min(), df_score["PE"].max()
    df_score["PE_标准化"] = (pe_max - df_score["PE"])/(pe_max-pe_min) if pe_max>pe_min else 0
    # 加权综合得分
    df_score["综合得分"] = (
        df_score["ROE_标准化"]*0.3 + df_score["毛利率_标准化"]*0.25 +
        df_score["EPS_标准化"]*0.25 + df_score["PE_标准化"]*0.1 +
        df_score["营收增速_标准化"]*0.1
    )
    df_top5 = df_score.sort_values("综合得分",ascending=False).head(5)
    all_result.append(df_top5[["代码","行业","公司名","ROE","毛利率","EPS","PE","营收增速","综合得分"]])
    print(f"\n==========【{industry_name}基本面TOP5】==========")
    print(df_top5[["代码","公司名","综合得分"]].round(3).to_string(index=False))

# 导出Excel
if all_result:
    final_df = pd.concat(all_result,ignore_index=True)
    final_df.to_excel("美股三大行业TOP5汇总.xlsx",index=False)
    print("\n✅ 数据已保存至：美股三大行业TOP5汇总.xlsx")
else:
    print("❌ 全部行业无有效数据，无法生成Excel")