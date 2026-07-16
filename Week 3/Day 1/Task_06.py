#6.	Call the API with llama-3.3-70b-versatile and llama-3.1-8b-instant for the same prompt. Print both responses and the usage.total_tokens for each. Note the difference in response quality and latency.

import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

prompt = "Explain AGI in exactly two paragraphs."
models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]

for model_name in models:
    print(f"\n--- TESTING: {model_name} ---")
    
    # Start a timer
    start_time = time.time()
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    
    # Stop the timer
    latency = time.time() - start_time
    
    print(response.choices[0].message.content)
    print(f"\n[METRICS for {model_name}]")
    print(f"Total Tokens Used: {response.usage.total_tokens}")
    print(f"Latency: {latency:.2f} seconds")

print("\nObservation: The 8B model responds much faster, but the 70B model uses more sophisticated vocabulary and deeper conceptual explanations.")