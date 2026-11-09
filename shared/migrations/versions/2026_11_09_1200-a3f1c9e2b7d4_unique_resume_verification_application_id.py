"""unique resume_verification application_id

Revision ID: a3f1c9e2b7d4
Revises: fbcdcd230547
Create Date: 2026-11-09 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'a3f1c9e2b7d4'
down_revision: Union[str, Sequence[str], None] = 'fbcdcd230547'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index(op.f('ix_resume_verification_application_id'), table_name='resume_verification')
    op.create_index(op.f('ix_resume_verification_application_id'), 'resume_verification', ['application_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_resume_verification_application_id'), table_name='resume_verification')
    op.create_index(op.f('ix_resume_verification_application_id'), 'resume_verification', ['application_id'], unique=False)
