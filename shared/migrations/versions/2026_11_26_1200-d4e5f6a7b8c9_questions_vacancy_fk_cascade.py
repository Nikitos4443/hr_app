"""questions.vacancy_id FK: cascade on vacancy delete

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-11-26 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

FK_NAME = 'fk_questions_vacancy_id_vacancies'


def upgrade() -> None:
    # Deleting a vacancy removes its questions. applications.vacancy_id keeps the
    # default (NO ACTION), so a vacancy with applications still cannot be deleted.
    op.drop_constraint(FK_NAME, 'questions', type_='foreignkey')
    op.create_foreign_key(
        FK_NAME, 'questions', 'vacancies', ['vacancy_id'], ['id'], ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint(FK_NAME, 'questions', type_='foreignkey')
    op.create_foreign_key(FK_NAME, 'questions', 'vacancies', ['vacancy_id'], ['id'])
