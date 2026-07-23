
# Capstone Project: RAG-Powered Document Q&A Chatbot API

## Overview

This project is an enterprise-grade Retrieval-Augmented Generation (RAG) backend built with **FastAPI**. It exposes a production-ready document ingestion and question-answering API. The system parses PDF and TXT documents, extracts text, creates vector embeddings locally, indexes chunks into an in-memory vector database, and leverages the **Groq API** (`llama-3.3-70b-versatile`) for grounded, hallucination-free answers with source citations.

Key features include:

* **Session Memory:** 6-turn rolling window memory per session ID to handle follow-up context.
* **Semantic Caching:** Instant response delivery for identical queries via MD5 query hashing.
* **Real-Time Streaming:** Word-by-word streaming endpoint (`/chat/stream`).
* **Automated Integration Testing:** Comprehensive 5-test suite running via `pytest`.

---

##  Technologies Used

* **Framework & API:** Python 3.10+, FastAPI, Uvicorn, Pydantic v2
* **Vector Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2` — 384 dimensions)
* **Vector Database:** `qdrant-client` (In-Memory execution for zero-infrastructure setup)
* **Document Parsing:** PyMuPDF (`fitz`)
* **LLM Engine:** Groq API (`llama-3.3-70b-versatile`)
* **Testing & Validation:** `pytest`, FastAPI `TestClient`
* **Environment Management:** `python-dotenv`

---

##  Project Structure

```text
Capstone - RAG Chatbot/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── schemas.py
│   ├── main.py
│   └── services/
│       ├── __init__.py
│       ├── document_service.py
│       ├── vector_service.py
│       ├── cache_service.py
│       ├── memory_service.py
│       └── llm_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md                   

```

---

##  Full Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>

```

### 2. Create and Activate a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate

```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure Environment Variables

Copy the template `.env.example` file to create your active `.env` file:

```bash
cp .env.example .env

```

Open `.env` and insert your Groq API key:

```text
GROQ_API_KEY=gsk_your_actual_groq_api_key_here

```

### 5. Run Automated Tests

Before starting the server, run the automated integration test suite to verify pipeline health:

```bash
pytest

```

### 6. Launch the Application

Boot up the Uvicorn development server:

```bash
uvicorn app.main:app --reload

```

The application will start at `[http://127.0.0.1:8000](http://127.0.0.1:8000)`.

---

##  How to Ingest a Document & Query the API

The primary interface for testing and interacting with the API is the interactive **Swagger UI** generated automatically by FastAPI.

Open your browser and navigate to: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

### Step 1: Ingest a Document (`POST /ingest`)

To index document context into the vector database:

1. In Swagger UI, expand the **`POST /ingest`** endpoint and click **Try it out**.
2. Click the **Choose File** button under `file` and select a document (e.g., `company_policy.pdf` or a `.txt` file).
3. Click **Execute**.

**Example Response:**

```json
{
  "status": "success",
  "filename": "company_policy.pdf",
  "chunks_indexed": 3
}

```

---

### Step 2: Initial Query (`POST /chat`)

Ask questions based on the ingested document using a unique `session_id`.

1. Expand the **`POST /chat`** endpoint and click **Try it out**.
2. Pass the following JSON payload into the request body:

```json
{
  "session_id": "user_session_102",
  "query": "How often do hardware refreshes occur?"
}

```

3. Click **Execute**.

**Example Response:**

```json
{
  "answer": "According to the company policy, hardware refreshes occur on a 36-month timeline.",
  "sources": 
    {
      "filename": "company_policy.pdf",
      "chunk_index": 0,
      "text": "...SECTION 3: REMOTE WORK STIPENDS AND HARDWARE ECOSYSTEM PROVISIONS..."
    }
  
}

```

---

### Step 3: Multi-Turn Follow-Up Query (`POST /chat`)

The application uses session memory to track history. Send a follow-up query using the **same** `session_id` to demonstrate context resolution:

```json
{
  "session_id": "user_session_102",
  "query": "Are there any exceptions to this 36-month rule?"
}

```

**Example Response:**

```json
{
  "answer": "Yes, early upgrades are prohibited unless catastrophic hardware failure is verified by an IT Operations Tier-2 engineer.",
  "sources": 
    {
      "filename": "company_policy.pdf",
      "chunk_index": 0,
      "text": "...Early upgrades are explicitly prohibited unless catastrophic hardware failure..."
    }
  
}

```

---

### Step 4: Verify Caching State

Re-submit the exact same payload from Step 3. The API will intercept the request and respond in under 0.01 seconds:

```json
{
  "answer": "Yes, early upgrades are prohibited unless catastrophic hardware failure is verified by an IT Operations Tier-2 engineer.",
  "sources": [ ... ]
}

```

---

##  Key Takeaways

* **APIs Bridge RAG to Microservices:** Wrapping retrieval logic inside FastAPI standardizes output structure, making vector pipeline context easily consumable by web and mobile frontends.
* **Bounded Session Memory:** Bounding conversation history to a 6-turn sliding window resolves follow-up pronouns while protecting the context window from token overflow.
* **MD5 Semantic Caching:** Local query hashing eliminates unnecessary network calls to Groq for repeated queries, dropping response times from seconds to sub-milliseconds.
* **Defensive Embedding Model Loading:** Using a `try/except` fallback for `SentenceTransformer("all-MiniLM-L6-v2")` prevents unexpected timeout errors caused by HuggingFace network checks during local execution.

---

**Author:** Usman Ahmad