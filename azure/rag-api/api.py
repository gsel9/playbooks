from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import run_rag

app = FastAPI()

class Messages(BaseModel):
    """
    Data model for user message and conversation history.
    """
    user_input: str
    prior_messages: List[Dict[str, Any]] | None = None


# TODO: Create unique user/session ID to track individual conversation histories
# TODO: Create DB (cosmos?) to store conversation histories
@app.post("/ask")
async def ask_api(messages: Messages) -> Dict:
    """
    Endpoint to execute chat loop.
    """
    try:
        answer = await run_rag(messages.user_input, messages.prior_messages or [])
        return {"answer": answer}
    except Exception as exc:
        # log.exception("ask_api failed")  # add logging as needed
        raise HTTPException(status_code=500, detail=str(exc))
