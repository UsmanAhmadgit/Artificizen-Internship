#6.	Install ragas and run a basic evaluation using faithfulness and answer_relevancy metrics on your 5 test cases. Print the scores and identify which question scored lowest and why.

import os
from dotenv import load_dotenv
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

# Import from Task 5
from Task_05 import setup_complex_database, ask_pipeline

load_dotenv()

def main():

    pdf_filename = "company_policy.pdf"

    if not os.path.exists(pdf_filename):
        print("ERROR: company_policy.pdf not found.")
        return

    setup_complex_database(pdf_filename)

    groq_chat_model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    evaluator_llm = LangchainLLMWrapper(groq_chat_model)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    evaluator_embeddings = LangchainEmbeddingsWrapper(
        embedding_model
    )

    faithfulness.llm = evaluator_llm

    answer_relevancy.llm = evaluator_llm
    answer_relevancy.embeddings = evaluator_embeddings

    test_cases = [
        {
            "question": "Under what exact conditions does an employee lose the intellectual property rights to a side project they made on their own time and personal hardware?",
            "ground_truth": "If the project utilizes features from core-utils-v4 OR if it directly competes with active R&D pipeline projects."
        },
        {
            "question": "Can an employee buy a $450 ergonomic chair using their stipend, and how long must they wait normally for hardware refreshes?",
            "ground_truth": "Yes, but VP authorization is required because it exceeds $400. Hardware refreshes occur every 36 months."
        },
        {
            "question": "What are the two requirements for a subcontractor to receive a temporary access card to the primary server room vault?",
            "ground_truth": "A fully executed NDA-Form-9B and physical escort by a staff member with at least 24 months of tenure."
        },
        {
            "question": "What is the disciplinary action required for a third infraction within the progressive discipline track?",
            "ground_truth": "I don't know."
        },
        {
            "question": "What is the policy regarding health insurance coverage extensions for family dependents during maternity leave?",
            "ground_truth": "I don't know."
        }
    ]

    questions = []
    answers = []
    contexts = []
    ground_truths = []

    print("=" * 60)
    print("Generating Answers...")
    print("=" * 60)

    for case in test_cases:

        question = case["question"]

        answer, retrieved_chunks = ask_pipeline(question)

        questions.append(question)
        answers.append(answer)
        contexts.append(retrieved_chunks)
        ground_truths.append(case["ground_truth"])

        print("\nQuestion:")
        print(question)

        print("\nAnswer:")
        print(answer)

        print("-" * 60)

    dataset = Dataset.from_dict(
        {
            "question": questions,
            "answer": answers,
            "contexts": contexts,
            "ground_truth": ground_truths,
        }
    )

    print("\nRunning RAGAS Evaluation...\n")

    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
        ],
    )

    df = result.to_pandas()

    print("=" * 60)
    print("RAGAS RESULTS")
    print("=" * 60)

    print(df)

    print("\nAverage Scores")
    print("-" * 30)

    print(
        df[["faithfulness", "answer_relevancy"]].mean()
    )

    combined_scores = (
        df["faithfulness"] +
        df["answer_relevancy"]
    )

    lowest = combined_scores.idxmin()

    print("\n" + "=" * 60)
    print("LOWEST SCORING QUESTION")
    print("=" * 60)

    print("\nQuestion:")
    print(questions[lowest])

    print("\nFaithfulness:")
    print(df.loc[lowest, "faithfulness"])

    print("\nAnswer Relevancy:")
    print(df.loc[lowest, "answer_relevancy"])

    print("\nPossible Reason:")

    faith = df.loc[lowest, "faithfulness"]
    rel = df.loc[lowest, "answer_relevancy"]

    if faith < 0.8 and rel < 0.8:
        print(
            "The retrieved context was insufficient and the generated answer was only partially relevant to the question."
        )

    elif faith < 0.8:
        print(
            "The generated answer contains information that is not completely supported by the retrieved context."
        )

    elif rel < 0.8:
        print(
            "The generated answer does not fully address the user's question."
        )

    else:
        print(
            "Although this question received the lowest score, it still performed reasonably well compared to the others."
        )

if __name__ == "__main__":
    main()

'''Observation: The terminal output vividly exposes a major flaw in automated metrics known as the "Refusal Penalty." 
When asked about maternity leave (which isn't in the document), the model properly followed instructions and answered exactly "I don't know". 
However, Ragas scored this as 0.0 for Faithfulness (because "I don't know" isn't written in the PDF context) and 0.0 for Answer Relevancy 
(because the metric cannot reverse-engineer a question from the phrase "I don't know"). This artificially tanked the overall averages, 
proving that standard metrics require custom adjustments to handle safe, grounded refusals fairly.'''