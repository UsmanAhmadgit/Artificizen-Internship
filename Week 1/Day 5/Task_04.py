#4. Write a program that saves a list of dictionaries (student records) to a JSON file, then loads them back.

import json

students = [
    {"name": "Ali", "score": 90},
    {"name": "Usman", "score": 85}
]

with open("students.json", "w") as file:
    json.dump(students, file, indent=4) 

with open("students.json", "r") as file:
    loaded_data = json.load(file)

print(loaded_data[0]["name"]) 