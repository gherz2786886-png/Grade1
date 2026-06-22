sentense = input ("Please input a sentense:")
words = sentense.split()
max_len = 0 
for word in words:
    len_word = len(word)
    print("The length of the word is:", len_word)
    if len_word > max_len:
        max_len = len_word
print("The maximum length of the words is:", max_len)