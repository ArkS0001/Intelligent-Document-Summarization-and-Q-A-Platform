Got it 🚀 — let’s put together the **full agentic setup** with **Groq API + AutoGen Agents + ChromaDB + FastAPI + Streamlit UI**.
This will give you an **end-to-end workflow**: document ingestion, summarization, entity extraction, vector storage, and question answering.

---

# 📂 Project Structure

```
document-summarizer/
│── requirements.txt
│── config.py
│── main.py                # FastAPI backend
│── run_streamlit.py       # Streamlit frontend
│
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── routes.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── summarizer_agent.py
│   │   ├── entity_agent.py
│   │   ├── qna_agent.py
│   │   ├── validator_agent.py
│   │   └── exception_agent.py
│   │
│   ├── services/
│   │   ├── parser.py
│   │   ├── vector_store.py
│   │   └── orchestration.py
│   │
│   └── utils/
│       └── __init__.py
```

---

# 📦 requirements.txt

```txt
fastapi
uvicorn
pydantic
python-dotenv
streamlit
requests
langchain
langchain-community
sentence-transformers
chromadb
pypdf
docx2txt
pyautogen
```

---

# ⚙️ config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DB_DIR = "data/chroma"

LLM_CONFIG = {
    "config_list": [
        {
            "model": "llama-3.1-8b-instant",
            "api_key": GROQ_API_KEY,
            "base_url": "https://api.groq.com/openai/v1"
        }
    ],
    "cache_seed": 42,
}
```

---

# 🧠 Agents

## app/agents/summarizer\_agent.py

```python
from autogen import AssistantAgent
from config import LLM_CONFIG

summarizer_agent = AssistantAgent(
    name="SummarizerAgent",
    llm_config=LLM_CONFIG,
    system_message="You are an expert at summarizing documents into structured, concise outputs."
)
```

## app/agents/entity\_agent.py

```python
from autogen import AssistantAgent
from config import LLM_CONFIG

entity_agent = AssistantAgent(
    name="EntityExtractorAgent",
    llm_config=LLM_CONFIG,
    system_message="Extract key entities (names, dates, organizations, keywords) from the document text."
)
```

## app/agents/qna\_agent.py

```python
from autogen import AssistantAgent
from config import LLM_CONFIG

qna_agent = AssistantAgent(
    name="QnAAgent",
    llm_config=LLM_CONFIG,
    system_message="Answer questions using provided document context. Be precise and cite relevant parts."
)
```

## app/agents/validator\_agent.py

```python
from autogen import AssistantAgent
from config import LLM_CONFIG

validator_agent = AssistantAgent(
    name="ValidatorAgent",
    llm_config=LLM_CONFIG,
    system_message="Validate outputs from other agents. Ensure factual correctness, consistency, and clarity."
)
```

## app/agents/exception\_agent.py

```python
from autogen import AssistantAgent
from config import LLM_CONFIG

exception_agent = AssistantAgent(
    name="ExceptionAgent",
    llm_config=LLM_CONFIG,
    system_message="Handle errors gracefully and suggest fixes for failed agent tasks."
)
```

---

# ⚙️ Services

## app/services/parser.py

```python
import docx2txt
from PyPDF2 import PdfReader

def parse_file(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_path.endswith(".docx"):
        text = docx2txt.process(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    return text
```

## app/services/vector\_store.py

```python
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from config import CHROMA_DB_DIR, EMBEDDING_MODEL

embedding_fn = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)

def get_vector_store():
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    return Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embedding_fn
    )
```

## app/services/orchestration.py

```python
from app.agents.summarizer_agent import summarizer_agent
from app.agents.entity_agent import entity_agent
from app.agents.qna_agent import qna_agent
from app.agents.validator_agent import validator_agent

def run_summarization(text: str) -> str:
    result = summarizer_agent.run(text)
    validated = validator_agent.run(f"Validate this summary:\n{result}")
    return validated

def run_entity_extraction(text: str) -> str:
    result = entity_agent.run(text)
    validated = validator_agent.run(f"Validate these entities:\n{result}")
    return validated

def run_qna(query: str, context: str) -> str:
    result = qna_agent.run(f"Context:\n{context}\n\nQuestion: {query}")
    validated = validator_agent.run(f"Validate this answer:\n{result}")
    return validated
```

---

# 🌐 API Routes

## app/api/routes.py

```python
from fastapi import APIRouter, UploadFile, HTTPException
from app.services.parser import parse_file
from app.services.vector_store import get_vector_store
from app.services.orchestration import run_summarization, run_entity_extraction, run_qna

router = APIRouter()

@router.post("/ingest")
async def ingest(file: UploadFile):
    try:
        file_path = f"data/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = parse_file(file_path)

        summary = run_summarization(text)
        entities = run_entity_extraction(text)

        vectordb = get_vector_store()
        vectordb.add_texts([text, summary, entities])

        return {"summary": summary, "entities": entities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ask")
async def ask(query: str):
    try:
        vectordb = get_vector_store()
        docs = vectordb.similarity_search(query, k=3)
        context = "\n".join([d.page_content for d in docs])

        answer = run_qna(query, context)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

# 🚀 FastAPI Entrypoint

## main.py

```python
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Agentic Document Summarizer & QnA")

app.include_router(router)

# Run backend with:
# uvicorn main:app --reload
```

---

# 🎨 Streamlit Frontend

## run\_streamlit.py

```python
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📄 Agentic Document Summarizer & QnA")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    resp = requests.post(f"{API_URL}/ingest", files={"file": uploaded_file})
    if resp.status_code == 200:
        result = resp.json()
        st.write("### Summary")
        st.write(result["summary"])
        st.write("### Entities")
        st.write(result["entities"])
    else:
        st.error("Failed to process document")

query = st.text_input("Ask a question about your documents")
if query:
    resp = requests.get(f"{API_URL}/ask", params={"query": query})
    if resp.status_code == 200:
        st.write("### Answer")
        st.write(resp.json()["answer"])
    else:
        st.error("Failed to get answer")
```

---

# ⚡ How to Run

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
2. Set your **Groq API key** in `.env`:

   ```
   GROQ_API_KEY=your_api_key_here
   ```
3. Start FastAPI backend:

   ```bash
   uvicorn main:app --reload
   ```
4. Launch Streamlit frontend:

   ```bash
   streamlit run run_streamlit.py
   ```

---

✅ This setup gives you:

* **Agent-based document ingestion** (Summarization + Entity Extraction + Validation)
* **ChromaDB storage** for context retrieval
* **Agentic Q\&A workflow** (QnAAgent + ValidatorAgent)
* **FastAPI API** + **Streamlit UI**

---

Do you want me to also **add multi-agent conversations (e.g., ValidatorAgent talking back to SummarizerAgent if output is bad)**, or keep it **linear (summarize → validate → return)** for now?
