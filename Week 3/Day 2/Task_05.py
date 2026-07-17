#5.	Write a three-step prompt chain using your ask() function: Step 1 extracts action items from a meeting transcript. Step 2 assigns priority (High / Medium / Low) to each. Step 3 formats them as a JSON array. Run all three steps in sequence.

from utils import ask

transcript = """ Analyze the transcript below. Extract a simple list of action items, identifying exactly who volunteered or agreed to do the task (the worker), NOT the person who brought up the problem.
Usman: "We need to fix the database migration issue before Friday."
Ahmad: "I'll handle the migration. But someone needs to update the logo on the homepage."
Ali: "I'll do the logo update next week."
"""

print("--- STEP 1: Extract Action Items ---")
step_1_prompt = f"Extract a simple list of action items and who owns them from this transcript:\n{transcript}"
action_items = ask(prompt=step_1_prompt, temperature=0.0)
print(action_items)

print("\n--- STEP 2: Assign Priority ---")
step_2_prompt = f"Take these action items and assign a Priority (High/Medium/Low) based on urgency. Friday is High, next week is Low:\n{action_items}"
prioritized_items = ask(prompt=step_2_prompt, temperature=0.0)
print(prioritized_items)

print("\n--- STEP 3: Format as JSON ---")
step_3_prompt = f"Convert the following prioritized list into a valid JSON array of objects with keys 'task', 'owner', and 'priority'.\n{prioritized_items}"
json_output = ask(prompt=step_3_prompt, system="Output pure JSON only.", temperature=0.0)
print(json_output)

'''Observation: This run perfectly illustrated "Error Amplification" in prompt chaining. In Step 1, the 8B model fell into a proximity trap, incorrectly assigning the migration task to Usman instead of Ahmad because Usman's name was nearest to the word. 
Because subsequent steps only processed the output of the previous step, the hallucinated name was carried all the way into the final JSON. Adding precise instructions to Step 1 to look for who 'volunteered' fixes this pipeline leak.'''