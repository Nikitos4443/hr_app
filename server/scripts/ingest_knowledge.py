"""Manage the AI assistant's vector store from the command line.

Uploaded documents (same as POST /companies/{company_id}/knowledge); each file is one document
named after the file, re-running for a file replaces it:
    uv run --env-file ../.env python -m scripts.ingest_knowledge --company-id 1 docs/faq.md
    uv run --env-file ../.env python -m scripts.ingest_knowledge --company-id 1 --list
    uv run --env-file ../.env python -m scripts.ingest_knowledge --company-id 1 --delete faq.md

Companies and vacancies are indexed automatically when saved through the API. Re-index them
from SQL after enabling RAG, after seeding the DB directly, or if a background sync failed:
    uv run --env-file ../.env python -m scripts.ingest_knowledge --sync-catalog
    uv run --env-file ../.env python -m scripts.ingest_knowledge --sync-catalog --company-id 1

Run from server/; needs a Postgres DATABASE_URL with the pgvector migration applied.
"""

import argparse
import asyncio
from pathlib import Path

from modules.ai_assistant.rag import IKnowledgeIndex, get_knowledge_index
from modules.knowledge.KnowledgeService import ALLOWED_SUFFIXES
from sqlalchemy import select

from database import init_db as db
from hr_core.models.company_model import Company
from hr_core.sql.repositories.SQLVacanciesRepository import SQLVacanciesRepository
from hr_core.sql.tables import Companies


def load_catalog(company_id: int | None) -> list[tuple[Company, list]]:
    db.init_db()
    with db.SessionLocal() as session:
        stmt = select(Companies).order_by(Companies.id)
        if company_id is not None:
            stmt = stmt.where(Companies.id == company_id)
        companies = [Company.model_validate(row) for row in session.scalars(stmt)]
        vacancies = SQLVacanciesRepository(db=session)
        return [(c, vacancies.list_by_company(c.id)) for c in companies]


async def sync_catalog(index: IKnowledgeIndex, company_id: int | None) -> None:
    catalog = await asyncio.to_thread(load_catalog, company_id)
    if not catalog:
        print("no companies found")
    for company, vacancies in catalog:
        await index.index_company(company)
        for vacancy in vacancies:
            await index.index_vacancy(vacancy)
        print(f"company {company.id} ({company.name}): profile + {len(vacancies)} vacancies")


async def run(args: argparse.Namespace) -> None:
    index = get_knowledge_index()
    if index is None:
        raise SystemExit("DATABASE_URL must point to Postgres with the pgvector extension")

    if args.sync_catalog:
        await sync_catalog(index, args.company_id)
        return

    if args.list:
        for doc in await index.list_documents(args.company_id):
            print(f"{doc.source}: {doc.chunks} chunks")
        return

    if args.delete:
        for name in args.paths:
            removed = await index.delete_document(args.company_id, Path(name).name)
            print(f"{Path(name).name}: {removed} chunks removed")
        return

    for raw in args.paths:
        path = Path(raw)
        if not path.is_file() or path.suffix.lower() not in ALLOWED_SUFFIXES:
            print(f"skip {path}: not a .md/.txt file")
            continue
        text = path.read_text(encoding="utf-8-sig").strip()
        if not text:
            print(f"skip {path}: empty file")
            continue
        doc = await index.add_document(args.company_id, path.name, text)
        print(f"{doc.source}: {doc.chunks} chunks stored")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--company-id", type=int)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--list", action="store_true", help="show the company's documents")
    mode.add_argument("--delete", action="store_true", help="remove the given documents")
    mode.add_argument(
        "--sync-catalog", action="store_true", help="re-index companies and vacancies from SQL"
    )
    parser.add_argument("paths", nargs="*", help="files to load (or document names with --delete)")
    args = parser.parse_args()
    if not args.sync_catalog:
        if args.company_id is None:
            parser.error("--company-id is required")
        if not args.list and not args.paths:
            parser.error("give at least one file, or use --list")
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
