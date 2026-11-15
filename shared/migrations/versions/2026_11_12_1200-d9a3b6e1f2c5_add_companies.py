"""add companies table and link vacancies to it

Revision ID: d9a3b6e1f2c5
Revises: f7d2b4e0a6c1
Create Date: 2026-11-12 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd9a3b6e1f2c5'
down_revision: Union[str, Sequence[str], None] = 'f7d2b4e0a6c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_companies')),
    sa.UniqueConstraint('name', name=op.f('uq_companies_name'))
    )

    op.add_column('vacancies', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_vacancies_company_id'), 'vacancies', ['company_id'], unique=False)
    op.create_foreign_key(
        op.f('fk_vacancies_company_id_companies'), 'vacancies', 'companies', ['company_id'], ['id']
    )

    # Backfill: one company per distinct name already stored on vacancies.
    op.execute(
        "INSERT INTO companies (name) "
        "SELECT DISTINCT company FROM vacancies WHERE company IS NOT NULL"
    )
    op.execute(
        "UPDATE vacancies v SET company_id = c.id FROM companies c WHERE c.name = v.company"
    )


def downgrade() -> None:
    op.drop_constraint(op.f('fk_vacancies_company_id_companies'), 'vacancies', type_='foreignkey')
    op.drop_index(op.f('ix_vacancies_company_id'), table_name='vacancies')
    op.drop_column('vacancies', 'company_id')
    op.drop_table('companies')
