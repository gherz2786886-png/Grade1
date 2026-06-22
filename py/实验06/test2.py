import keyword
 
keywords = keyword.kwlist
print(keywords)
word = input("Please input a word:")
if word in keywords:
    print("The word is a keyword.")
else:
    print("The word is not a keyword.")