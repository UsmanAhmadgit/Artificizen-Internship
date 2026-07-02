#5. Sort a list of dictionaries (e.g., students with name and marks) by marks using sorted() and a key function.

students = [{"name":"Ali", "marks":85},
            {"name":"Usman", "marks":92},
            {"name":"Ahmad", "marks":78}]
ranked = sorted(students, key= lambda x: x["marks"], reverse=True)
print(ranked)