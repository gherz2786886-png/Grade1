id_StudentGiveName = "2202502924"
name_StudentGivenName = "Horzion Leo"
digits_list = [int(char) for char in id_StudentGiveName]

last_digit = digits_list[-1]
id_int = int(id_StudentGiveName)
if last_digit % 2 == 0:
    calc_val = id_int / 1000
else:
    calc_val = id_int /500

print(type(calc_val))
print("{0:4f}".format(calc_val))