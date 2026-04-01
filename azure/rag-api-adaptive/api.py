from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import run_rag

app = FastAPI()

class Query(BaseModel):
    """
    Data model for user message and conversation history.
    """
    user_id: str
    conv_id: str
    user_input: str


@app.post("/ask")
def ask_api(query: Query) -> Dict[str, Any]:
    """
    Endpoint to execute chat loop.
    """
    try:
        answer = run_rag(query.user_id, query.conv_id, query.user_input)
        return {"answer": answer}
    except Exception as exc:
        # log.exception("ask_api failed")  # add logging as needed
        raise HTTPException(status_code=500, detail=str(exc))
