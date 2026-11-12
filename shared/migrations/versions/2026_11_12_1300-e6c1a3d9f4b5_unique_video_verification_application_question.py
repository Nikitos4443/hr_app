"""unique video_verification (application_id, question_id)

Revision ID: e6c1a3d9f4b5
Revises: d5a9f2c8e1b3
Create Date: 2026-11-12 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'e6c1a3d9f4b5'
down_revision: Union[str, Sequence[str], None] = 'd5a9f2c8e1b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        'uq_video_verification_application_question',
        'video_verification',
        ['application_id', 'question_id'],
    )


def downgrade() -> None:
    op.drop_constraint('uq_video_verification_application_question', 'video_verification', type_='unique')
