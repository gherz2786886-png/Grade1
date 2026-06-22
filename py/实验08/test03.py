def fun(n):
    num = int(n)
    if num <= 10000:
        return tuple(int(c) for c in str(num))
    else:
        return "--------------------ERROR----------------------"
    
if __name__=="__main__":
    n=input("请输入一个10000以内的数：")
    print(fun(n))
   

 