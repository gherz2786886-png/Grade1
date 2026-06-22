'''时间获取'''
import time
time.strptime('1999-6-18', '%Y-%m-%d')
print("这一天的星期是：", time.strptime('1999-6-18', '%Y-%m-%d').tm_wday)