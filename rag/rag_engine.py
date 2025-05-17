# rag/rag_engine.py
"""
Retrieval-Augmented Generation (RAG) Engine using FAISS and OpenAI.
"""

import json
import os
import faiss
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document

class RAGPipeline:
    def __init__(self, index_path="vector_store/news.index", json_path="data/news.json"):
        self.index_path = index_path
        self.json_path = json_path
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")

    def load_documents(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Document(page_content=d["description"], metadata={"title": d["title"]}) for d in data]

    def build_vector_store(self):
        docs = self.load_documents()
        vectorstore = FAISS.from_documents(docs, self.embeddings)
        vectorstore.save_local(self.index_path)
        print("Vector store built and saved.")

    def ask(self, query):
        vectorstore = FAISS.load_local(self.index_path, self.embeddings)
        qa = RetrievalQA.from_chain_type(llm=self.llm, retriever=vectorstore.as_retriever())
        return qa.run(query)
