from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_email: str
    subject: str
    description: str

class ChatResponse(BaseModel):
    answer: str
