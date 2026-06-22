dic_student = {}
for i in range(5):
    name,age = input(f"请输入第{i+1}个学生的姓名和年龄（用空格分隔）：").split()
    dic_student[name] = age


'''王建    18
张云    19
张秋雨  18
刘欢    17
姜宇    19
'''