"""enable pgvector extension for the AI assistant RAG

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-11-16 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # The langchain_pg_collection / langchain_pg_embedding tables are created by
    # langchain_postgres.PGVector itself on first use.
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS langchain_pg_embedding")
    op.execute("DROP TABLE IF EXISTS langchain_pg_collection")
    op.execute("DROP EXTENSION IF EXISTS vector")
