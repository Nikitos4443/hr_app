from abc import ABC, abstractmethod

from modules.auth.dto.principal import AuthPrincipal
from modules.knowledge.dto.knowledge_dto import KnowledgeDocumentDTO


class IKnowledgeService(ABC):
    @abstractmethod
    async def upload_document(
        self, actor: AuthPrincipal, company_id: int, filename: str | None, content: bytes
    ) -> KnowledgeDocumentDTO: ...

    @abstractmethod
    async def list_documents(
        self, actor: AuthPrincipal, company_id: int
    ) -> list[KnowledgeDocumentDTO]: ...

    @abstractmethod
    async def delete_document(self, actor: AuthPrincipal, company_id: int, source: str) -> None: ...
