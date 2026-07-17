#4.	Write a system prompt that turns the model into a senior Python code reviewer: strict, concise, no praise, actionable suggestions only. Submit a buggy code snippet and compare to a default system prompt output.

from utils import ask

buggy_code = """
def add_numbers(a, b):
    print(a + b)
    return a+b
"""

default_system = "You are a helpful coding assistant."

strict_system = """You are a senior Python code reviewer. 
Rules: Be extremely strict. Be concise. Offer zero praise. Provide actionable suggestions only. 
CRITICAL NEGATIVE CONSTRAINT: Do not provide any rewritten python code blocks or corrected code snippets. Provide text feedback ONLY."""

print("--- DEFAULT ASSISTANT ---")
print(ask(prompt=buggy_code, system=default_system))

print("\n--- STRICT SENIOR REVIEWER ---")
print(ask(prompt=buggy_code, system=strict_system))


'''Observation: 
Role prompting completely transformed the model's behavior. The Default Assistant was overly polite, verbose, and provided multiple code rewrites. The Strict Senior Reviewer successfully adopted a blunt, critical tone. 
Furthermore, by placing the negative constraint ('Do not provide any rewritten python code blocks') at the very end of the prompt using the Recency Effect, the model perfectly obeyed the instruction and only provided text feedback.'''
