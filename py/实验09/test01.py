'''1. 编写一个函数compare（file1,file2），比较两个文本文件内容
是否相同，如果内容相同返回True,否则返回False。在主程序中输入两个
要比较的两文件名，然后调用以上函数，
文件内容相同则输出“No difference!”;否则输出“difference!”。'''
def compare(file1,file2):
    with open(file1,'r',encoding='utf-8') as f1,open(file2,'r',encoding='utf-8') as f2:
        content1 = f1.read()
        content2 = f2.read()
        return content1 == content2
    
if __name__ =="__main__":
        file1 = input("请输入第一个文件名：")
        file2 = input("请输入第二个文件名：")
        result = compare(file1,file2)
        
        if result:
            print("No difference!")
        else:
            print("difference!")