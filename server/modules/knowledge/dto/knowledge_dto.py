from pydantic import BaseModel


class KnowledgeDocumentDTO(BaseModel):
    source: str
    chunks: int
