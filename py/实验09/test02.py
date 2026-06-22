'''假设现在老师要随机点几位学生回答问题。编写一个函数，每次调用从中抽取一位学生。
在主程序中对其连续调用，并可以控制是否需要继续抽取。假设每次抽取的学生可以重复。'''
import random
def readStudentID:
    with open("student.txt",'r',encoding = 'utf-8') as f:
        line = f.readline()
        ID = line.strip().split( )
    return ID

def getRandomStudentID():
    return random.choice(readStudentID())
        
if __name__="__main__":
print('请抽取学生ID')
While Tru
    studentID = getRandomStudentID()
    print("抽取的学生ID是：",studentID)
    choice = input("是否继续抽取？(y/n)")
    if choice.lower() != 'y':
        break   


    