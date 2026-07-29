# AI Legal Case Workspace

A robust, multimodal RAG backend designed to ingest and query legal documents.

## Overview
Legal teams often waste countless hours manually reviewing scattered evidence and case files stored in different formats, making it easy to miss critical details during trial preparation. 

The **AI Legal Case Workspace** solves this by bringing all case-related documents into a single, AI-powered platform. Lawyers can create dedicated, isolated chat rooms for each legal case, allowing them to search, summarize, and ask questions across every uploaded file for that specific case. This ensures teams stay focused, organize information efficiently, and prepare for trials with fast, source-backed answers.

**Target Audience:** Lawyers, paralegals, and legal assistants handling legal research.

**Supported File Types for AI Ingestion:**
* **Documents:** Contracts (DOCX), Court Rulings (PDF)
* **Media:** Evidence Photos (Images), Witness Interviews (Audio), CCTV/Deposition Recordings (Video)
* **Data & Notes:** Evidence Logs (CSV), Legal Notes (TXT/Markdown)

---

## Current Features
* **Backend Foundation:** Complete repository structure built with FastAPI and SQLAlchemy.
* **Authentication:** Secure user registration and login using JWT and modern `bcrypt` password hashing.
* **Case Management:** Protected CRUD operations for user-scoped Chat Rooms (ensuring users only have access to their own case files).
* **Database:** SQLite database seamlessly integrated with Alembic for version-controlled schema migrations.
* **Multi-Format Ingestion Pipeline:** Centralized dispatcher dynamically routing 16+ file types (PDF, DOCX, PPTX, CSV, TXT, Images, Audio, Video) to specialized extraction modules.
* **Intelligent Text Chunking:** Context-aware splitting algorithm featuring an 800-character limit and 1-element overlap (carrying over previous paragraphs or table rows) to prevent semantic loss and model truncation.
* **Local Deep-Learning OCR:** Integrated PaddleOCR and OpenCV for privacy-first, offline text extraction from standalone images (PNG/JPG) as well as pictures embedded deep within PDFs, DOCXs, and PPTXs.
* **Audio & Video Transcription:** Native Groq Whisper API integration to extract text from media files, injecting `[MM:SS]` timestamps directly into the text chunks for precise retrieval.
* **Structured Data Preservation:** Advanced parsing that respects original document architecture, cleanly breaking down DOCX/PPTX tables row-by-row while preserving section headings and slide titles across chunks.
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
This project requires environment variables to handle secrets and database URLs safely.
Copy the provided example file to create your own local environment file:

```bash
# On Linux/Mac:
cp .env.example .env

# On Windows (Command Prompt):
copy .env.example .env

```

Once copied, open the new `.env` file and replace the placeholder values (like `SECRET_KEY`) with your actual secure credentials.

**5. Initialize the database**
Run the Alembic migrations to build the database tables.

```bash
alembic upgrade head

```

**6. Start the server**

```bash
uvicorn main:app --reload

```

Navigate to `http://127.0.0.1:8000/docs` in your browser to access the interactive Swagger UI and test the API.
