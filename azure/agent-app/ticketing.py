"""
Support ticket generation and file persistence.
"""

import json
import uuid
from pathlib import Path


def submit_support_ticket(email_address: str, description: str) -> str:
    """
    Generate a ticket, store it in a text file, and return a JSON message.
    """
    script_dir = Path(__file__).parent
    ticket_id = uuid.uuid4().hex[:6]
    file_name = f"ticket-{ticket_id}.txt"
    file_path = script_dir / file_name

    content = (
        f"Support ticket: {ticket_id}\n"
        f"Submitted by: {email_address}\n\n"
        f"Description:\n{description}\n"
    )
    file_path.write_text(content, encoding="utf-8")

    return json.dumps({
        "message": (
            f"Support ticket {ticket_id} submitted successfully. "
            f"Saved as {file_name}."
        )
    })
