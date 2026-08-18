# AI Legal Case Workspace

A robust, multimodal RAG application designed to ingest, organize, and query legal documents, evidence, and case files.

* **Industry:** Legal Tech / AI Legal Software
* **Target Audience:** Lawyers, paralegals, and legal assistants handling case research and trial preparation.

---

## Overview

### Problem Statement
Legal teams often waste countless hours manually reviewing scattered evidence and case files stored in different formats, making it easy to miss critical details during trial preparation. 

The **AI Legal Case Workspace** solves this by bringing all case-related documents into a single, AI-powered platform. Lawyers can create dedicated, isolated chat rooms for each legal case, allowing them to search, summarize, and ask questions across every uploaded file for that specific case. This ensures teams stay focused, organize information efficiently, and prepare for trials with fast, source-backed answers.

### Supported File Types for AI Ingestion
* **Documents:** Contracts (DOCX), Court Rulings (PDF)
* **Media:** Evidence Photos (Images), Witness Interviews (Audio), CCTV/Deposition Recordings (Video)
* **Data & Notes:** Evidence Logs (CSV), Legal Notes (TXT/Markdown)

---

## Environment Variables Required

Create a `.env` file in the root directory with the following required environment variables:

```env
# Database Settings
DATABASE_URL=sqlite:///./ai_legal.db

# Security & JWT Authentication
SECRET_KEY= your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# External AI APIs
GROQ_API_KEY= your-api-key

```

---

## Local Setup Instructions

**1. Clone the repository**

```bash
git clone <your-repository-url>
cd <your-repository-folder>

```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

```

**3. Install dependencies**

```bash
pip install -r requirements.txt

```

**4. Configure environment variables**
Copy the example environment file and fill in your credentials:

```bash
# On Linux/Mac:
cp .env.example .env

# On Windows (Command Prompt):
copy .env.example .env

```

**5. Initialize the database**
Run the Alembic migrations to build the database tables:

```bash
alembic upgrade head

```

**6. Start the application**

* **Start the FastAPI Backend:**
```bash
uvicorn main:app --reload

```


*(Access interactive Swagger API docs at `http://127.0.0.1:8000/docs`)*
* **Start the Streamlit Frontend (in a second terminal):**
```bash
streamlit run streamlit_app.py

```



---

## Quick Demo Steps

1. **Register & Log In:** Open the Streamlit web application (`http://localhost:8501`) and create a new user account.
2. **Create a Case Room:** On the main dashboard, enter a room name (e.g., *"State v. Miller - Case #402"*) and click **Create Room**.
3. **Enter the Room:** Click **Enter Room** to access the case chat workspace.
4. **Upload Case Evidence:** Use the sidebar file uploader to attach case PDFs, documents, images, or audio/video transcript files.
5. **Ask the AI:** Type a query into the chat box (e.g., *"What were the key facts in the police report?"*). The AI will stream a response with exact source references.
6. **Room & Account Management:** Test editing the room name, wiping chat history, or deleting the case room cleanly from the main dashboard.
