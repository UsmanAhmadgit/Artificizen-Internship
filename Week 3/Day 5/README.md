# Day 5: RAG with FastAPI + Multi-Turn Chat + Evaluation

## Overview

This project focuses on exposing a RAG pipeline via a FastAPI backend, adding advanced features like conversation memory, semantic caching, and streaming, and thoroughly evaluating the pipeline's performance using both manual grading and automated Ragas metrics.

## Technologies Used

* Python 3.10+
* FastAPI & Uvicorn
* Sentence Transformers
* Qdrant Client
* PyMuPDF (fitz)
* Groq API
* Ragas & Datasets
* LangChain Wrappers
* python-dotenv

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate

```

2. Install the core RAG dependencies:

```bash
pip install fastapi uvicorn sentence-transformers qdrant-client pymupdf groq python-dotenv datasets

```

3. **CRITICAL:** Install the strictly pinned evaluation dependencies to ensure Ragas v0.2 compatibility:

```bash
pip install ragas==0.2.15 langchain==0.2.17 langchain-core==0.2.43 langchain-community==0.2.19 langchain-groq==0.1.10 langchain-huggingface==0.0.3

```

4. Create a `.env` file in the root directory and add your API key:

```text
GROQ_API_KEY=gsk_your_api_key_here

```

## Models Used

* **Embedding Model:** `all-MiniLM-L6-v2` (Dimensions: 384, Local Execution)
* **LLM (Generation & Evaluation):** `llama-3.3-70b-versatile` (Execution via Groq API)

## Project Structure

```text
Day 5/
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

## Task 1: FastAPI RAG Endpoint

**Action:** I wrapped the baseline RAG pipeline in a FastAPI POST endpoint that returns the generated answer and a list of source citations.

**Result:** The pipeline became accessible over HTTP with structured JSON validation using Pydantic schemas.

**Observation:** Structuring the output guarantees that front-end applications can explicitly trace the AI's claims back to specific document chunks.

## Task 2: Multi-Turn Conversation Memory

**Action:** I implemented a session-based memory dictionary to store the last 6 conversational turns and passed them to the Groq API.

**Result:** The model successfully understood context and resolved pronouns in follow-up questions.

**Observation:** Limiting the history to a rolling window prevents context window overflow and saves API token usage.

## Task 3: Semantic Caching

**Action:** I built an optimization layer that hashes incoming queries using MD5 and returns stored answers for identical repeated requests.

**Result:** Repeated queries bypassed the vector search and LLM generation entirely, dropping response times to near zero.

**Observation:** Caching dramatically reduces API costs and latency for frequently asked questions.

## Task 4: Real-Time Streaming

**Action:** I configured the Groq client to stream tokens and used FastAPI's `StreamingResponse` with a custom Python generator.

**Result:** The API delivered the answer word-by-word in real time while still updating the cache and session history in the background.

**Observation:** Streaming significantly improves the perceived user experience by eliminating the long wait times for complete generations.

## Task 5: Interactive Manual Evaluation

**Action:** I scripted a 5-question test suite against a complex corporate PDF and built a CLI loop to manually grade the AI's outputs.

**Result:** The pipeline achieved a perfect accuracy score, successfully navigating strict conditions and correctly refusing out-of-context edge cases.

**Observation:** Manual grading is a critical first step to visually confirm the grounding prompt is working before deploying automated tools.

## Task 6: Automated Ragas Evaluation

**Action:** I integrated the Ragas framework (strictly pinned to version 0.2.15 with corresponding LangChain wrappers) to automatically grade the pipeline's answers against ground-truth data using Faithfulness and Answer Relevancy metrics.

**Result:** The evaluation completed, returning an average Faithfulness of 0.80 and Answer Relevancy of 0.35, correctly identifying negative edge cases as the lowest-scoring queries.

**Observation:** The terminal output vividly exposes a major flaw in automated metrics known as the "Refusal Penalty." When asked about maternity leave (which isn't in the document), the model properly followed instructions and answered exactly *"I don't know"*. However, Ragas scored this as 0.0 for Faithfulness (because "I don't know" isn't written in the PDF context) and 0.0 for Answer Relevancy (because the metric cannot reverse-engineer a question from the phrase "I don't know"). This artificially tanked the overall averages, proving that standard metrics require custom adjustments to handle safe, grounded refusals fairly.

## Key Takeaways

* **APIs Bridge the Gap:** Wrapping scripts in FastAPI transforms raw Python logic into usable microservices.
* **Memory Requires Management:** Conversational AI needs explicit, bounded storage arrays to maintain context without breaking limits.
* **Speed is an Illusion:** Streaming does not make the AI process faster, but delivering tokens progressively makes the application feel instant.
* **Dependency Stability:** The AI ecosystem updates rapidly; pinning exact package versions (e.g., LangChain and Ragas) is mandatory for production stability.
* **Evaluation is Important:** Automated tools like Ragas are powerful, but their mathematical approach penalizes safe LLM behavior (like refusing to hallucinate). Human oversight is still essential for interpreting pipeline health.