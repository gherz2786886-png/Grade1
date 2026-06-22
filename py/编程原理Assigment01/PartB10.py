id_StudentGivenName = "2202502924"
digits_list = [int(char) for char in id_StudentGivenName]

factor = 10

def scale_id_digits(target_list, multiplier):
    new_list = []
    for num in target_list:
        new_list.append(num * multiplier)
    return new_list

result = scale_id_digits(digits_list, 4)
print(result)