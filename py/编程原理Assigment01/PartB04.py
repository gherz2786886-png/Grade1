id_StudentGivenName = "220252924"

print("Before slicing id:", id(id_StudentGivenName))

first3 = id_StudentGivenName[:3]
last3 = id_StudentGivenName[-3:]
result = first3 + "-" + last3
print(result)
print("After slicing id:", id(id_StudentGivenName))