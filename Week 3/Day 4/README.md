# Day 4: Retrieval-Augmented Generation (RAG) Pipeline

## Overview

This project focuses on building a Retrieval-Augmented Generation workflow that ingests document content, chunks it into manageable segments, stores embeddings in Qdrant, retrieves the most relevant context, and grounds an LLM so it answers only from the provided material.

## Technologies Used

* Python 3.10+
* Sentence Transformers
* Qdrant Client
* PyMuPDF4LLM
* Groq API
* python-dotenv

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate

```


2. Install the required dependencies:
```bash
pip install sentence-transformers qdrant-client pymupdf4llm groq python-dotenv

```


3. Create a `.env` file in the root directory and add your API key:
```text
GROQ_API_KEY=gsk_your_api_key_here

```

## Models Used

* **Embedding Model:** `all-MiniLM-L6-v2` (Dimensions: 384, Local Execution)
* **LLM:** `llama-3.3-70b-versatile` (Execution via Groq API)

## Project Structure

```text
Day 4/
├── Task_01.py
├── Task_02.py
├── Task_03.py
├── Task_04.py
├── Task_05.py
├── Task_06.py
├── company_policy.pdf
└── README.md

```

---

## Task 1: Text Chunking with Overlap

**Action:** I built a chunking function that splits a long document into overlapping segments so nearby chunks keep context.

**Result:** It produced clean overlapping chunks that looked well aligned across boundaries.

**Observation:** The overlap helps keep important sentences from getting cut off during embedding.

## Task 2: PDF Ingestion and Chunk Storage

**Action:** I extracted text from company_policy.pdf with PyMuPDF4LLM, converted it to readable Markdown, and chunked it for Qdrant storage.

**Result:** The PDF content was split and stored in a way that made it ready for search.

**Observation:** The original text still needs to stay in the payload because embeddings alone do not show the readable content.

## Task 3: Semantic Retrieval

**Action:** I built a retrieval function that embeds a user query and pulls the most relevant chunks from Qdrant.

**Result:** It returned the strongest matches and skipped the unrelated ones.

**Observation:** Vector distance makes the search work even when the wording is different.

## Task 4: Prompt Grounding

**Action:** I created a prompt template that injects the retrieved chunks and tells the model to answer only from that context.

**Result:** It kept the source context separate from the user question.

**Observation:** The strict prompt is what keeps the model grounded in the document.

## Task 5: Full RAG Pipeline

**Action:** I connected retrieval and generation into a full RAG flow using the Groq API.

**Result:** It answered supported questions and stayed quiet on missing facts.

**Observation:** The retrieved text becomes the main source of truth for the response.

## Task 6: Hallucination Check

**Action:** I tested the model with a question that was not supported by the document context.

**Result:** It refused to guess instead of inventing an answer.

**Observation:** This shows why RAG is useful when the source material has to be trusted.

## Key Takeaways
* **Chunking Matters:** Overlapping chunks preserve context across boundary cuts and improve retrieval quality.
* **Retrieval First:** Qdrant returns the most relevant context before the LLM generates an answer.
* **Grounded Generation:** Prompting the model with strict instructions keeps responses tied to the source document.
* **RAG Reduces Hallucination:** The pipeline is useful because it prioritizes retrieved facts over unsupported model guesses.