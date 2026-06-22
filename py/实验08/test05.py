def isLeapYear(n):
    if (n%4==0 and n%100!=0) or n%400==0:
        return True
    else:
        return False
    
if__name__=="__main__":
n=int(input("请输入一个年份："))
if isLeapYear(n):
    print(f"{n}是闰年")
else:
     print(f"{n}不是闰年")