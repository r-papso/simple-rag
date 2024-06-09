from pydantic import BaseModel


class Document(BaseModel):
    content: str = None
    path: str = None
