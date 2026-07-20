# Day 3: Embeddings & Semantic Search

## Overview

This project focuses on the practical application of text embeddings, semantic search algorithms, and vector databases. The tasks demonstrate how to convert natural language into mathematical vectors to perform searches based on context and meaning rather than exact keyword matching.

## Technologies Used

* Python 3.10+
* Sentence Transformers
* NumPy
* ChromaDB
* Qdrant Client

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate

```


2. Install the required dependencies:
```bash
pip install sentence-transformers chromadb qdrant-client numpy

```



## Embedding Model

* **Model:** `all-MiniLM-L6-v2`
* **Dimensions:** 384
* **Size:** ~80 MB
* **Execution:** Runs locally without API keys

## Project Structure

```text
Day 3/
├── Task_01.py
├── Task_02.py
├── Task_03.py
├── Task_04.py
├── Task_05.py
├── Task_06.py
└── README.md

```

---

## Task 1: Pairwise Cosine Similarity

**Action:** Generated dense vector embeddings for a set of sentences and manually calculated the cosine similarity for every unique pair using NumPy.

**Result:** Ranked the sentence pairs from highest to lowest similarity. "A dog is chasing a ball" and "The puppy runs after the toy" ranked first with a score of 0.4868.

**Observation:** The model accurately identified semantic equivalence between the top sentences even though they shared zero primary keywords, while correctly assigning negative scores to unrelated concepts.

## Task 2: Custom Semantic Search Function

**Action:** Built a foundational search algorithm to compare a specific user query ("How do I fix my password issue?") against a list of potential support documents.

**Result:** Ranked the documents by relevance, correctly placing the password reset instruction at Rank 1 with a score of 0.6324.

**Observation:** Cosine similarity can be directly applied to build a highly effective, ranked search engine from scratch.

## Task 3: ChromaDB In-Memory Integration

**Action:** Replaced manual array calculations with ChromaDB. Initialized an in-memory database, inserted documents, and executed a query for "famous romantic tragedies."

**Result:** The database retrieved the document about William Shakespeare as the top result (Distance: 0.9906) and pushed unrelated entries like Albert Einstein to the bottom (Distance: 1.6659).

**Observation:** ChromaDB simplifies the workflow by handling embedding and indexing automatically. It uses Cosine Distance (where a lower score indicates higher similarity) rather than Cosine Similarity.

## Task 4: Qdrant with Metadata Filtering

**Action:** Deployed a Qdrant vector database to handle vectors alongside metadata payloads. Queried the database while applying a strict `FieldCondition` filter.

**Result:** Filtered a query about shutting down equipment so it only returned documents where the source was labeled "manual", successfully retrieving the correct shutdown procedure with a score of 0.6301.

**Observation:** Metadata filtering is essential in production systems to restrict search spaces and prevent the retrieval of semantically similar but contextually incorrect data (such as company news vs. user manuals).

## Task 5: The Vocabulary Disconnect Test

**Action:** Stress-tested the embedding model by querying "Cars are speeding up quicker nowadays" against a hidden target sentence containing completely different vocabulary.

**Result:** The system successfully matched the query to "Automobiles are accelerating faster than ever before" with a similarity score of 0.7440.

**Observation:** This proves that dense vector retrieval solves the "vocabulary disconnect" problem that causes traditional keyword-matching systems (like SQL `LIKE` queries) to fail.

## Task 6: RAG Utility Pipeline Validation

**Action:** Abstracted the vector insertion logic into a modular, reusable `embed_and_store` function designed to batch encode text, structure payloads, and upsert points into a Qdrant collection.

**Result:** Successfully executed the pipeline, verifying that the collection holds the newly embedded vectors.

**Observation:** Establishing a clean ETL (Extract, Transform, Load) pipeline is the final necessary step before connecting a vector database to a Large Language Model for a complete RAG architecture.


## Key Takeaways
* **Semantic Vector Space:** Dense embeddings map text based on contextual meaning rather than exact word matches, resolving the vocabulary disconnect problem.
* **Distance Metrics:** Cosine Similarity measures directional agreement (higher is better), while Cosine Distance measures conceptual separation (lower is better).
* **Metadata Filtering:** Single-stage payload filtering in databases like Qdrant prevents cross-domain context leakage during vector retrieval.
* **Vector Databases vs. Arrays:** Real vector databases (ChromaDB, Qdrant) use specialized indexing algorithms to enable millisecond queries across large datasets.