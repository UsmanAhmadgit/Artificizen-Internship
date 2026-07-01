#5. Given a sentence, count the vowels and consonants separately.

sentence = "Python is amazing, and learning it is fun!"

vowels = {"a", "e", "i", "o", "u"}

vowel_count = 0
consonant_count = 0

for char in sentence.lower():
    if char.isalpha():
        if char in vowels:
            vowel_count += 1
        else:
            consonant_count += 1

print(f"Original Sentence: '{sentence}'")
print(f"Total Vowels:     {vowel_count}")
print(f"Total Consonants: {consonant_count}")