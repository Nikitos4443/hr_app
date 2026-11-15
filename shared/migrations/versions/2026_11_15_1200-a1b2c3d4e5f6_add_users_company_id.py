"""link users to companies

Revision ID: a1b2c3d4e5f6
Revises: d9a3b6e1f2c5
Create Date: 2026-11-15 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'd9a3b6e1f2c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_users_company_id'), 'users', ['company_id'], unique=False)
    op.create_foreign_key(
        op.f('fk_users_company_id_companies'), 'users', 'companies', ['company_id'], ['id']
    )


def downgrade() -> None:
    op.drop_constraint(op.f('fk_users_company_id_companies'), 'users', type_='foreignkey')
    op.drop_index(op.f('ix_users_company_id'), table_name='users')
    op.drop_column('users', 'company_id')
