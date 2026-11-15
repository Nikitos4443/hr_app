"""restrict user roles to company_admin and hr

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-11-15 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Legacy rows used the placeholder role "user"; map anything unknown to hr.
    op.execute("UPDATE users SET role = 'hr' WHERE role NOT IN ('company_admin', 'hr')")
    op.alter_column('users', 'role', existing_type=sa.String(), server_default='hr')
    op.create_check_constraint(
        op.f('ck_users_role_valid'), 'users', "role IN ('company_admin', 'hr')"
    )


def downgrade() -> None:
    op.drop_constraint(op.f('ck_users_role_valid'), 'users', type_='check')
    op.alter_column('users', 'role', existing_type=sa.String(), server_default=None)
