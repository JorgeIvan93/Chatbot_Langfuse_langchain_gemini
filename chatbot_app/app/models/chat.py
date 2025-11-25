from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Schema for incoming chat messages.
    """

    message: str


class ChatResponse(BaseModel):
    """
    Schema for chatbot responses.
    """

    reply: str
