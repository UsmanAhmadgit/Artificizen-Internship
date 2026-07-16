#2.	Call the Groq API using llama-3.1-8b-instant and print a completion for: “Summarise what a transformer model does in 3 sentences.”

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq()

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Summarise what a transformer model does in 3 sentences."}
    ],
    temperature=0.7
)

print(" Task 2: GROK API Call")
print(response.choices[0].message.content)