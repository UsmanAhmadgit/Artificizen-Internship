#3. Write a program that reads a text file and reports the number of lines, words, and characters.

def analyze_text_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            
            num_chars = len(content)
            
            num_words = len(content.split())
            
            if num_chars == 0:
                num_lines = 0
            else:
                num_lines = len(content.split('\n'))
            
            print(f"--- Analysis for '{filepath}' ---")
            print(f"Lines:      {num_lines}")
            print(f"Words:      {num_words}")
            print(f"Characters: {num_chars}")
            print("-" * 30)
            
    except FileNotFoundError:
        print(f"Error: Could not find a file named '{filepath}'. Please check the name and try again.")

analyze_text_file("D:\Artificizen Internship\Week 1\Day 5\sample.txt")
