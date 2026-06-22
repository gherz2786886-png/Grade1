# ====================== 第一部分：判断闰年的函数 ======================
def is_leap_year(year):
    # 满足条件返回True（是闰年），不满足返回False（不是）
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# ====================== 第二部分：主函数（调用+输出） ======================
if __name__ == "__main__":
    print("2000年到3000年之间的闰年有：")
    for year in range(2000, 3001):
        if is_leap_year(year):
            print(year, end=" ")