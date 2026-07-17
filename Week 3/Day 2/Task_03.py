#3.	Ask Groq to solve a logic puzzle. Run it once without CoT, then add “Think step by step” at the end. Print both answers and note whether CoT helped.

from utils import ask

puzzle = """There are 5 large boxes in a room. 
Inside each large box, there are 2 medium boxes. 
Inside each medium box, there are 4 tiny boxes. 
All of the tiny boxes are completely empty, except for exactly one tiny box which contains a single gold coin. 

CRITICAL DEFINITION: A box is ONLY "completely empty" if there is absolutely nothing inside it. If a box contains smaller boxes, it is NOT empty.

How many completely empty boxes are there in total in the room?."""
print("--- WITHOUT CHAIN OF THOUGHT ---")
base_response = ask(prompt=puzzle, temperature=0.0)
print(base_response)

print("\n--- WITH CHAIN OF THOUGHT ---")
cot_prompt = puzzle + " Think step-by-step before providing the final answer."
cot_response = ask(prompt=cot_prompt, temperature=0.0)
print(cot_response)

print('''\nObservation: The Impact of CoT, Prompt Clarity, and Model Scale
1. The Impact of Chain-of-Thought (CoT)
Adding explicit CoT ("Think step-by-step") proved that CoT alone cannot fix a fundamental misunderstanding. While CoT helps models with math, it failed to help the 8B model because the AI misunderstood the semantic logic of the puzzle. 
Adding CoT to the 8B model merely caused it to "hallucinate step-by-step" (getting 54 instead of 171) using flawed logic. The 70B model, conversely, was unaffected by CoT flags because its vast size allows it to naturally apply deep reasoning to every query.

2. The Impact of Instruction Clarity
The critical variable was the inclusion or removal of this exact guiding line:
"Evaluate the emptiness of the Large, Medium, and Tiny boxes separately before giving your final number."

When the line was ADDED: Both models successfully answered 39. The 8B model succeeded because this sentence acted as a strict guardrail, forcing it to analyze the physical state of each box size sequentially rather than just adding all numbers together.

When the line was REMOVED: The 8B model (llama-3.1-8b-instant) catastrophically failed (outputting 171 without CoT, and 54 with CoT). Without explicit instructions, the 8B model reverted to basic arithmetic and failed the semantic trap—it did not understand the physical reality that a box holding smaller boxes is not empty. 
In stark contrast, the 70B model (llama-3.3-70b-versatile) succeeded flawlessly (39) even without the guiding line. Its massive parameter count gives it native "common sense" regarding physical containment, meaning it didn't need its hand held to realize Large and Medium boxes weren't empty.

Summary: Small models (8B) are fragile and require highly specific prompt engineering to navigate logical traps. Large models (70B) possess robust zero-shot reasoning and can overcome vague prompts autonomously.''')