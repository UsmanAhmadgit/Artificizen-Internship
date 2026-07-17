from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

"""A reusable wrapper for the Groq API."""

def ask(prompt, system=None, model="llama-3.1-8b-instant", temperature=0.7, max_tokens=512):
    
    
    # Start with just the user message
    messages = []
    
    # If a system prompt is provided, insert it at the very beginning
    if system:
        messages.append({"role": "system", "content": system})
        
    # Append the user's prompt
    messages.append({"role": "user", "content": prompt})
    
    # Make the API call
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Return only the text string
    return response.choices[0].message.content