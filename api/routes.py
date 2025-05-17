# api/routes.py

from fastapi import APIRouter, Query
from rag.rag_engine import RAGPipeline

router = APIRouter()
rag = RAGPipeline()

@router.get("/ask/")
def ask_question(q: str = Query(..., description="Question to query the news RAG system")):
    try:
        answer = rag.ask(q)
        return {"question": q, "answer": answer}
    except Exception as e:
        return {"error": str(e)}
