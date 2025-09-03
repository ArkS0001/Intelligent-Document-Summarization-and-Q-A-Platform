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
