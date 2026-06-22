id_StudentGivenName = "12345678"
digits_list = [int(char) for char in id_StudentGivenName]

working_digits = digits_list[:]
sum_first_last = digits_list[0] + digits_list[-1]
working_digits.append(sum_first_last)
working_digits.insert(1, 9)

print("Original digits_list:", digits_list)
print("Modified working_digits:", working_digits)