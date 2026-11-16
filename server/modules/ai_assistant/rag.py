"""Everything the AI assistant knows comes from this pgvector store.

Each company's knowledge is a set of documents, split into chunks:
- kind="company":  the company profile (one per company, source "company");
- kind="vacancy":  one per vacancy (source "vacancy:<id>", has vacancy_id in metadata);
- kind="document": files uploaded by HR (FAQ, benefits, policies...), source = file name.

Company and vacancy documents are kept in sync by modules.knowledge.sync.CatalogSync.
"""

from dataclasses import dataclass
from functools import lru_cache
from typing import Protocol

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from modules.ai_assistant.format import format_company, format_vacancy
from sqlalchemy import func, select
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from config import EMBEDDING_DIM, EMBEDDING_MODEL, settings
from hr_core.models.company_model import Company
from hr_core.models.vacancy_model import Vacancy
from hr_core.sql.session import normalize_database_url

COLLECTION = "company_knowledge"
DEFAULT_K = 6
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

KIND_COMPANY = "company"
KIND_VACANCY = "vacancy"
KIND_DOCUMENT = "document"
COMPANY_SOURCE = "company"


def vacancy_source(vacancy_id: int) -> str:
    return f"vacancy:{vacancy_id}"


class IKnowledgeRetriever(Protocol):
    async def search(
        self, query: str, company_id: int | None, vacancy_id: int | None
    ) -> list[Document]: ...


def build_embeddings() -> GoogleGenerativeAIEmbeddings:
    # 768 dims instead of the default 3072: pgvector HNSW indexes support at most 2000.
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        output_dimensionality=EMBEDDING_DIM,
        google_api_key=settings.google_api_key,
    )


def is_postgres(database_url: str) -> bool:
    return make_url(normalize_database_url(database_url)).get_backend_name() == "postgresql"


def build_vector_store(database_url: str | None = None) -> PGVector:
    engine = create_async_engine(
        normalize_database_url(database_url or settings.database_url),
        # Neon pooler (PgBouncer) breaks psycopg auto-prepared statements (see hr_core.sql.session).
        connect_args={"prepare_threshold": None},
        pool_pre_ping=True,
    )
    return PGVector(
        embeddings=build_embeddings(),
        connection=engine,
        collection_name=COLLECTION,
        embedding_length=EMBEDDING_DIM,
        use_jsonb=True,
        # The extension is enabled by an Alembic migration; the app user may lack the rights.
        create_extension=False,
        async_mode=True,
    )


@lru_cache
def get_vector_store() -> PGVector | None:
    """One shared store per process; None when the DB is not Postgres (SQLite, tests)."""
    if not is_postgres(settings.database_url):
        return None
    return build_vector_store()


class KnowledgeRetriever:
    def __init__(self, store: PGVector, k: int = DEFAULT_K):
        self.store = store
        self.k = k

    async def search(
        self, query: str, company_id: int | None, vacancy_id: int | None
    ) -> list[Document]:
        """Chunks of this company: its profile, its documents and only the current vacancy
        (a candidate chatting about one vacancy must not get answers from another)."""
        if company_id is None or not query.strip():
            return []
        return await self.store.asimilarity_search(
            query,
            k=self.k,
            filter={
                "$and": [
                    {"company_id": {"$eq": company_id}},
                    {
                        "$or": [
                            {"kind": {"$ne": KIND_VACANCY}},
                            {"vacancy_id": {"$eq": vacancy_id if vacancy_id is not None else -1}},
                        ]
                    },
                ]
            },
        )


def build_retriever() -> KnowledgeRetriever | None:
    """None without Postgres: the assistant then has no knowledge to answer from."""
    store = get_vector_store()
    return KnowledgeRetriever(store) if store else None


@dataclass(frozen=True)
class KnowledgeDocument:
    source: str
    chunks: int


class IKnowledgeIndex(Protocol):
    async def add_document(self, company_id: int, source: str, text: str) -> KnowledgeDocument: ...

    async def list_documents(self, company_id: int) -> list[KnowledgeDocument]: ...

    async def delete_document(self, company_id: int, source: str) -> int: ...

    async def index_company(self, company: Company) -> None: ...

    async def delete_company(self, company_id: int) -> None: ...

    async def index_vacancy(self, vacancy: Vacancy) -> None: ...

    async def delete_vacancy(self, vacancy_id: int) -> None: ...


class KnowledgeIndex:
    def __init__(self, store: PGVector):
        self.store = store
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
        )

    # --- documents uploaded by HR ---

    async def add_document(self, company_id: int, source: str, text: str) -> KnowledgeDocument:
        chunks = await self._replace(
            company_id, source, text, {"kind": KIND_DOCUMENT}, header=f"Company document {source}"
        )
        return KnowledgeDocument(source=source, chunks=chunks)

    async def list_documents(self, company_id: int) -> list[KnowledgeDocument]:
        async with self.store.session_maker() as session:
            collection = await self.store.aget_collection(session)
            if collection is None:
                return []
            table = self.store.EmbeddingStore
            source = table.cmetadata["source"].astext
            rows = await session.execute(
                select(source, func.count())
                .where(
                    table.collection_id == collection.uuid,
                    table.cmetadata["company_id"].astext == str(company_id),
                    table.cmetadata["kind"].astext == KIND_DOCUMENT,
                )
                .group_by(source)
                .order_by(source)
            )
            return [KnowledgeDocument(source=name, chunks=count) for name, count in rows]

    async def delete_document(self, company_id: int, source: str) -> int:
        return await self._delete(company_id, source=source, kind=KIND_DOCUMENT)

    # --- company profile and vacancies (mirrors of the SQL rows) ---

    async def index_company(self, company: Company) -> None:
        await self._replace(
            company.id,
            COMPANY_SOURCE,
            format_company(company),
            {"kind": KIND_COMPANY},
            header=f"Company {company.name}",
        )

    async def delete_company(self, company_id: int) -> None:
        """Everything of the company: profile, vacancies and uploaded documents."""
        await self._delete(company_id)

    async def index_vacancy(self, vacancy: Vacancy) -> None:
        if vacancy.company_id is None:
            return
        await self._replace(
            vacancy.company_id,
            vacancy_source(vacancy.id),
            format_vacancy(vacancy),
            {"kind": KIND_VACANCY, "vacancy_id": vacancy.id},
            header=f'Vacancy "{vacancy.title}" at {vacancy.company}',
        )

    async def delete_vacancy(self, vacancy_id: int) -> None:
        # "vacancy:<id>" is unique across companies, so the company is not needed.
        await self._delete(None, source=vacancy_source(vacancy_id), kind=KIND_VACANCY)

    # --- internals ---

    async def _replace(
        self, company_id: int, source: str, text: str, metadata: dict, *, header: str
    ) -> int:
        """Add or replace one document. New chunks are upserted before stale ones are removed,
        so a failed embedding call leaves the previous version in place."""
        chunks = self.splitter.create_documents(
            [text], metadatas=[{**metadata, "company_id": company_id, "source": source}]
        )
        # Every chunk repeats what it belongs to: a chunk with only "Salary: 3000 USD" is
        # useless to the search and to the model without knowing which vacancy it is.
        for chunk in chunks:
            chunk.page_content = f"{header}\n{chunk.page_content}"
        new_ids = [f"{company_id}:{source}:{i}" for i in range(len(chunks))]
        old_ids = await self._chunk_ids(company_id, source=source)
        await self.store.aadd_documents(chunks, ids=new_ids)
        if stale := sorted(set(old_ids) - set(new_ids)):
            await self.store.adelete(stale, collection_only=True)
        return len(chunks)

    async def _delete(
        self, company_id: int | None, *, source: str | None = None, kind: str | None = None
    ) -> int:
        ids = await self._chunk_ids(company_id, source=source, kind=kind)
        if ids:
            await self.store.adelete(ids, collection_only=True)
        return len(ids)

    async def _chunk_ids(
        self, company_id: int | None, *, source: str | None = None, kind: str | None = None
    ) -> list[str]:
        async with self.store.session_maker() as session:
            collection = await self.store.aget_collection(session)
            if collection is None:
                return []
            table = self.store.EmbeddingStore
            conditions = [table.collection_id == collection.uuid]
            if company_id is not None:
                conditions.append(table.cmetadata["company_id"].astext == str(company_id))
            if source is not None:
                conditions.append(table.cmetadata["source"].astext == source)
            if kind is not None:
                conditions.append(table.cmetadata["kind"].astext == kind)
            return list(await session.scalars(select(table.id).where(*conditions)))


def get_knowledge_index() -> IKnowledgeIndex | None:
    store = get_vector_store()
    return KnowledgeIndex(store) if store else None


def format_docs(docs: list[Document]) -> str:
    if not docs:
        return "No information found."
    return "\n\n---\n\n".join(doc.page_content for doc in docs)
