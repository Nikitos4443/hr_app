import logging
from pathlib import PurePath

from fastapi import HTTPException
from starlette import status

from modules.ai_assistant.rag import IKnowledgeIndex
from modules.auth.dto.principal import AuthPrincipal
from modules.knowledge.dto.knowledge_dto import KnowledgeDocumentDTO
from modules.knowledge.IKnowledgeService import IKnowledgeService
from modules.users.IUserService import IUserService

logger = logging.getLogger(__name__)

ALLOWED_SUFFIXES = {".md", ".txt"}
MAX_FILE_BYTES = 1024 * 1024
MAX_SOURCE_LENGTH = 200


class KnowledgeService(IKnowledgeService):
    def __init__(self, index: IKnowledgeIndex | None, users_service: IUserService):
        self.index = index
        self.users_service = users_service

    async def upload_document(
        self, actor: AuthPrincipal, company_id: int, filename: str | None, content: bytes
    ) -> KnowledgeDocumentDTO:
        index = self._require_access(actor, company_id)
        source = self._source_name(filename)
        text = self._decode(content)
        try:
            doc = await index.add_document(company_id, source, text)
        except Exception as e:
            # Usually the embeddings API (quota, network) or the DB; the old version stays intact.
            logger.exception("failed to index %s for company %s", source, company_id)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to index the document"
            ) from e
        return KnowledgeDocumentDTO(source=doc.source, chunks=doc.chunks)

    async def list_documents(
        self, actor: AuthPrincipal, company_id: int
    ) -> list[KnowledgeDocumentDTO]:
        index = self._require_access(actor, company_id)
        docs = await index.list_documents(company_id)
        return [KnowledgeDocumentDTO(source=d.source, chunks=d.chunks) for d in docs]

    async def delete_document(self, actor: AuthPrincipal, company_id: int, source: str) -> None:
        index = self._require_access(actor, company_id)
        if await index.delete_document(company_id, source) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    def _require_access(self, actor: AuthPrincipal, company_id: int) -> IKnowledgeIndex:
        user = self.users_service.get_by_id(actor.id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        # 404 rather than 403, so other companies' ids are not revealed (same as CompanyService).
        if user.company_id != company_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        if self.index is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Knowledge base is not configured",
            )
        return self.index

    @staticmethod
    def _source_name(filename: str | None) -> str:
        # Keep only the base name: browsers may send paths, and the name is the document's id.
        name = PurePath((filename or "").replace("\\", "/")).name.strip()
        if not name:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="File name is required"
            )
        if PurePath(name).suffix.lower() not in ALLOWED_SUFFIXES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only .md and .txt files are supported",
            )
        if len(name) > MAX_SOURCE_LENGTH:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="File name is too long"
            )
        return name

    @staticmethod
    def _decode(content: bytes) -> str:
        if len(content) > MAX_FILE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail="File is larger than 1 MB"
            )
        try:
            text = content.decode("utf-8-sig").strip()
        except UnicodeDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="File must be UTF-8 text",
            ) from e
        if not text:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="File is empty"
            )
        return text
