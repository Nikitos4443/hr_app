"""add applications rejection_notified_at

Revision ID: b7e2d4f8c1a9
Revises: a3f1c9e2b7d4
Create Date: 2026-11-09 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b7e2d4f8c1a9'
down_revision: Union[str, Sequence[str], None] = 'a3f1c9e2b7d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('applications', sa.Column('rejection_notified_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('applications', 'rejection_notified_at')
