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
