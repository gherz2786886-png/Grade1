def getBMI(weight,height):
    BMI=weight / (height**2)
    if BMI < 18:
        discribe = 'thin'
    elif BMI <= 25:
        discribe ='normol'
    elif BMI <= 30:
        discribe = 'fat'
    elif BMI <= 35:
        discribe = 'litle fat'
    elif BMI <= 40:
        discribe = 'medium fat'
    else:
        discribe = 'serious fat'
    return (BMI,discribe)

if __name__=="__main__":
    w = float(input("Please input your weight(kg):"))
    h = float(input("Please input your hight(m):"))
    
    BMI, discribe = getBMI(w, h)
    print(f"BMI value:{BMI},how discribe:{discribe}")
