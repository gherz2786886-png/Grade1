dict(John=123,Marry=111,Tommy=123456)
print("请输入用户名和密码：")
用户名,密码 = input().split()
if dict.get(用户名) != 密码:
    print("密码错误！")
if dict.get(用户名) is None:
    print("用户名错误！")
else:
    print("登录成功！")