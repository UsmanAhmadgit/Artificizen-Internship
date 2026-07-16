#3.	Run the same prompt three times at temperature=0 and three times at temperature=1.0. Print all six responses and write a one-line observation about the difference.

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

prompt = "Write the opening sentence of a sci-fi mystery novel set on Mars."

print("--- TEMPERATURE 0.0 ---")
for i in range(3):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    print(f"Attempt {i+1}: {res.choices[0].message.content}")

print("\n--- TEMPERATURE 1.0 ---")
for i in range(3):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0
    )
    print(f"Attempt {i+1}: {res.choices[0].message.content}")

print("\nObservation: Temperature 0.0 returns the exact same sentence every time, while Temperature 1.0 generates a completely unique sentence for every request.")