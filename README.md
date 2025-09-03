# Intelligent-Document-Summarization-and-Q-A-Platform

Recommended Project Structure (Without MCP)
Agentic Rag basically
```
document-summarizer/
│── README.md
│── requirements.txt
│── .env
│── config.py
│── main.py                 # FastAPI entrypoint
│── run_streamlit.py        # Streamlit app launcher
│
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py       # FastAPI routes (ingest, summarize, Q&A)
│   │   └── schemas.py      # Pydantic models
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser.py       # PDF/DOCX/HTML parsing
│   │   ├── summarizer.py   # Summarization agent
│   │   ├── entity_extractor.py # Entity extraction
│   │   ├── qna.py          # Q&A over documents
│   │   └── validation.py   # Cross-agent validation & rollback
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py       # Logging setup
│   │   └── exceptions.py   # Custom exceptions
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_parser.py
│       ├── test_summarizer.py
│       ├── test_entities.py
│       ├── test_qna.py
│       └── test_endpoints.py
│
├── ui/
│   ├── __init__.py
│   ├── app.py              # Streamlit UI (upload, summary, Q&A)
│   └── components.py       # Reusable UI elements
│
└── data/
    ├── sample_docs/        # Example PDFs, DOCX, etc.
    └── outputs/            # Saved summaries, logs, reports

```

![WhatsApp Image 2025-09-03 at 7 15 59 PM](https://github.com/user-attachments/assets/5c1966a4-1592-457f-b211-809e99d0639f)
![WhatsApp Image 2025-09-03 at 7 15 59 PM(1)](https://github.com/user-attachments/assets/d695b1a8-86dd-4294-b87d-9d3d07e8c29a)
![WhatsApp Image 2025-09-03 at 7 15 59 PM(2)](https://github.com/user-attachments/assets/b1830db3-5bcc-41fe-b504-5aae318a05e5)
![WhatsApp Image 2025-09-03 at 7 16 00 PM](https://github.com/user-attachments/assets/98da4e67-7f69-4653-bb34-d1c4bd33d216)
![WhatsApp Image 2025-09-03 at 7 15 58 PM](https://github.com/user-attachments/assets/cf833173-4fd8-4326-a944-4b2324c88b7d)
![WhatsApp Image 2025-09-03 at 7 15 58 PM(1)](https://github.com/user-attachments/assets/a94c3553-511e-4896-8ef1-ddff350fb859)
