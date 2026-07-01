#2. Count the frequency of each word in a sentence using a dictionary.

text = "Hello, world! Python is: 100% awesome. Python is fun!"

clean_text = "".join([char for char in text if char.isalnum() or char == " "])

words = clean_text.lower().split()

word_counts = {}

for word in words:
    word_counts[word] = word_counts.get(word, 0) + 1

print("Original Text:", text)

for word, count in word_counts.items():
    print(f"{word}: {count}")