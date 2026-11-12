"""unique text_verification (application_id, question_id)

Revision ID: f7d2b4e0a6c1
Revises: e6c1a3d9f4b5
Create Date: 2026-11-12 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'f7d2b4e0a6c1'
down_revision: Union[str, Sequence[str], None] = 'e6c1a3d9f4b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        'uq_text_verification_application_question',
        'text_verification',
        ['application_id', 'question_id'],
    )


def downgrade() -> None:
    op.drop_constraint('uq_text_verification_application_question', 'text_verification', type_='unique')
