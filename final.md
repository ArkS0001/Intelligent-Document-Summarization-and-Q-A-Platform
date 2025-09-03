```
document-summarizer/
│── main.py
│── run_streamlit.py
│── config.py
│── requirements.txt
│
├── app/
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
│   │   └── orchestration.py   # manages agent workflow
│   │
│   └── api/
│       └── routes.py

```
