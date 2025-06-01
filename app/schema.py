from pydantic import BaseModel

class ChatBot(BaseModel):
    query: str