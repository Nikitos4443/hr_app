"""drop s3_key from resume_verification and video_verification

Revision ID: d5a9f2c8e1b3
Revises: c4d8e1a7f3b2
Create Date: 2026-11-12 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd5a9f2c8e1b3'
down_revision: Union[str, Sequence[str], None] = 'c4d8e1a7f3b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('resume_verification', 's3_key')
    op.drop_column('video_verification', 's3_key')


def downgrade() -> None:
    op.add_column('video_verification', sa.Column('s3_key', sa.String(), nullable=True))
    op.add_column('resume_verification', sa.Column('s3_key', sa.String(), nullable=True))
