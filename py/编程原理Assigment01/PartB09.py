id_StudentGivenName = "2202502924"
digits_list = [int(char) for char in id_StudentGivenName]

squared_filtered = [x**2 for x in digits_list if x > 2]
print(squared_filtered)