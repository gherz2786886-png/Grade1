'''编写一个随机生成验证码的程序，验证码由英文和数字组成，长度为4个字符。'''
import random
import string   
def authentication_code():
    characters= string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(4))
print("生成的验证码是:", authentication_code())          
