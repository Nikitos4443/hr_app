"""applications screening token, invite and purge tracking

Revision ID: c4d8e1a7f3b2
Revises: b7e2d4f8c1a9
Create Date: 2026-11-09 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c4d8e1a7f3b2'
down_revision: Union[str, Sequence[str], None] = 'b7e2d4f8c1a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('applications', sa.Column('screening_token', sa.String(), nullable=True))
    op.execute(
        "UPDATE applications SET screening_token = "
        "replace(gen_random_uuid()::text, '-', '') || replace(gen_random_uuid()::text, '-', '')"
    )
    op.alter_column('applications', 'screening_token', nullable=False)
    op.create_unique_constraint(op.f('uq_applications_screening_token'), 'applications', ['screening_token'])
    op.add_column('applications', sa.Column('screening_invited_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('applications', sa.Column('purged_at', sa.DateTime(timezone=True), nullable=True))
    op.alter_column('applications', 'full_name', existing_type=sa.String(), nullable=True)


def downgrade() -> None:
    op.alter_column('applications', 'full_name', existing_type=sa.String(), nullable=False)
    op.drop_column('applications', 'purged_at')
    op.drop_column('applications', 'screening_invited_at')
    op.drop_constraint(op.f('uq_applications_screening_token'), 'applications', type_='unique')
    op.drop_column('applications', 'screening_token')
