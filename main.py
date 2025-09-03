from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Agentic Document Summarizer & QnA")

app.include_router(router)

# Run backend with:
# uvicorn main:app --reload
