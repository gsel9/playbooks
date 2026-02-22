from fastapi import FastAPI
from pydantic import BaseModel
from main import run_rag  # <-- reuse your existing logic

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_api(payload: Query):
    answer = run_rag(payload.question)
    return {"answer": answer}