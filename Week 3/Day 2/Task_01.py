#1.	Write a zero-shot prompt that classifies a customer message as Complaint, Question, or Compliment. Test with five sample messages and print each classification.

from utils import ask

messages = [
    "My screen arrived cracked, I demand a refund!",
    "What time does your store open on Sundays?",
    "The delivery driver was incredibly polite and helpful.",
    "I can't figure out how to reset my password.",
    "This is the best laptop I have ever purchased."
]

system_prompt = "Classify the user message into exactly one of these categories: Complaint, Question, or Compliment."

print("--- ZERO-SHOT CLASSIFICATION ---")
for msg in messages:
    classification = ask(prompt=msg, system=system_prompt, temperature=0.0)
    print(f"Message: '{msg}' \n-> {classification}\n")