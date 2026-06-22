id_StudentGivenName = "2202502924"
digits_list = [int(char) for char in id_StudentGivenName]

threshold = digits_list[2]
count = 0
while True:
    num = int(input("Enter an integer: "))
    if num < threshold:
        count += 1
    else:
        break

print(f"Loop terminated. Number of invalid entries: {count}")