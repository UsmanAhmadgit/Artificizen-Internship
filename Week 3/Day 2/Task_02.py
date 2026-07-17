#2.	Convert the above to a few-shot prompt by adding three labelled examples before the test message. Compare accuracy between zero-shot and few-shot.

from utils import ask

messages = [
    "My screen arrived cracked, I demand a refund!",
    "What time does your store open on Sundays?",
    "The delivery driver was incredibly polite and helpful.",
    "I can't figure out how to reset my password.",
    "This is the best laptop I have ever purchased."
]

system_prompt = """Classify the user message as Complaint, Question, or Compliment. 

Examples:
Message: "This software keeps crashing." -> Complaint
Message: "Do you offer student discounts?" -> Question
Message: "Amazing customer service today!" -> Compliment
"""

print("--- FEW-SHOT CLASSIFICATION ---")
for msg in messages:
    prompt = f"Message: \"{msg}\" ->"
    classification = ask(prompt=prompt, system=system_prompt, temperature=0.0)
    print(f"Message: '{msg}' \n-> {classification}\n")

print("Observation: Few-shot guarantees the exact formatting (like preventing the model from saying 'I would classify this message as a Complaint').")