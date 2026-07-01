#6. Write a function that returns the most frequent element in a list.

def get_most_frequent(logs):
    counts = {}
    for log in logs:
        counts[log] = counts.get(log, 0) + 1
        
    return max(counts, key=counts.get)


api_requests = ["GET", "POST", "GET", "PUT", "GET", "DELETE", "POST", "GET"]

winner = get_most_frequent(api_requests)

print(f"Server Logs: {api_requests}")
print(f"Most frequent request type: {winner}")