id_StudentGivenName = "2202502924"
digits_list = [int(char) for char in id_StudentGivenName]

total_sum = sum(digits_list)

product = 1
for d in digits_list:
    if d != 0:
        product *= d

print("Sum of all digits:", total_sum)
print("Product of non-zero digits:", product)