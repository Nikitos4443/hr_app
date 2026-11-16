"""Mirrors companies and vacancies into the vector store, which is the assistant's only source.

Called from the companies/vacancies routes as FastAPI background tasks, i.e. after the response
is sent: a slow or failing embeddings API must not slow down or break saving a vacancy. A failed
sync is only logged; `python -m scripts.ingest_knowledge --sync-catalog` re-indexes everything.
"""

import logging

from hr_core.models.company_model import Company
from hr_core.models.vacancy_model import Vacancy
from modules.ai_assistant.rag import IKnowledgeIndex

logger = logging.getLogger(__name__)


class CatalogSync:
    def __init__(self, index: IKnowledgeIndex | None):
        # None when there is no vector DB (SQLite dev/tests): syncing is then a no-op.
        self.index = index

    async def company_saved(self, company: Company) -> None:
        if self.index is None:
            return
        try:
            await self.index.index_company(company)
        except Exception:
            logger.exception("failed to index company %s", company.id)

    async def company_deleted(self, company_id: int) -> None:
        if self.index is None:
            return
        try:
            await self.index.delete_company(company_id)
        except Exception:
            logger.exception("failed to remove company %s from the index", company_id)

    async def vacancy_saved(self, vacancy: Vacancy) -> None:
        if self.index is None:
            return
        try:
            await self.index.index_vacancy(vacancy)
        except Exception:
            logger.exception("failed to index vacancy %s", vacancy.id)

    async def vacancy_deleted(self, vacancy_id: int) -> None:
        if self.index is None:
            return
        try:
            await self.index.delete_vacancy(vacancy_id)
        except Exception:
            logger.exception("failed to remove vacancy %s from the index", vacancy_id)
