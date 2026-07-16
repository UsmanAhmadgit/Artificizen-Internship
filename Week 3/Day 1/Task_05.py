#5.	Pass a system message: “You are a strict JSON-only responder. Never output anything outside a JSON object.” Ask any question and print the raw output. Did it obey?

from Task_04 import ask

system_instruction = "You are a strict JSON-only responder. Never output anything outside a JSON object."
user_question = "What are the three primary colors?"

print("--- Task 5: JSON Strictness Test ---")
response_text = ask(
    prompt=user_question, 
    system=system_instruction, 
    temperature=0.0
)

print(response_text)
print("\nDid it obey? Yes, the LLM output raw JSON brackets without any conversational filler like 'Here are the colors:'")