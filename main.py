from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI(
    title="AI News Analyst - ETL + RAG System",
    description="Detects and analyzes misinformation in real-time news using RAG",
    version="1.0.0"
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
