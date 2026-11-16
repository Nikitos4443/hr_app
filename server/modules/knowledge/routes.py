"""Company documents (FAQ, benefits, policies...) that the AI assistant searches when answering."""

from fastapi import APIRouter, Depends, UploadFile
from fastapi_utils.cbv import cbv
from ioc.index import get_knowledge_service
from starlette import status

from hr_core.models.user_model import UserRole
from modules.auth.guards import CurrentPrincipalDep, require_roles
from modules.knowledge.dto.knowledge_dto import KnowledgeDocumentDTO
from modules.knowledge.IKnowledgeService import IKnowledgeService
from modules.knowledge.KnowledgeService import MAX_FILE_BYTES

router = APIRouter(prefix="/companies/{company_id}/knowledge", tags=["knowledge"])


@cbv(router)
class KnowledgeRouter:
    knowledge_service: IKnowledgeService = Depends(get_knowledge_service)

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=KnowledgeDocumentDTO)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def upload_document(
        self, company_id: int, file: UploadFile, principal: CurrentPrincipalDep
    ):
        """Add a .md/.txt document, or replace the one with the same file name."""
        # One byte over the limit is enough to reject the file without reading all of it.
        content = await file.read(MAX_FILE_BYTES + 1)
        return await self.knowledge_service.upload_document(
            principal, company_id, file.filename, content
        )

    @router.get("/", response_model=list[KnowledgeDocumentDTO])
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def list_documents(self, company_id: int, principal: CurrentPrincipalDep):
        return await self.knowledge_service.list_documents(principal, company_id)

    @router.delete("/{source}", status_code=status.HTTP_204_NO_CONTENT)
    @require_roles(UserRole.COMPANY_ADMIN, UserRole.HR)
    async def delete_document(self, company_id: int, source: str, principal: CurrentPrincipalDep):
        await self.knowledge_service.delete_document(principal, company_id, source)
