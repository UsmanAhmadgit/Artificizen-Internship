#3. Use filter() to extract all strings longer than 5 characters from a list.

words = ["ai", "python", "dev", "backend", "code", "engineer"]
long_words = list(filter(lambda x: len(x)>5, words))
print(long_words)