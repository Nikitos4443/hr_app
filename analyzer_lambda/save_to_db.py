from db import SessionLocal

from hr_core.models.evaluation_model import Evaluation
from hr_core.sql.repositories.SQLEvaluationsRepository import SQLEvaluationsRepository
from output_model import RankedCandidate


def save_evaluations(vacancy_id: int, ranking: list[RankedCandidate]) -> None:
    with SessionLocal() as session:
        SQLEvaluationsRepository(db=session).replace_for_vacancy(
            vacancy_id,
            [
                Evaluation(
                    application_id=item.application_id,
                    vacancy_id=vacancy_id,
                    order=item.order,
                    summary=item.summary,
                )
                for item in ranking
            ],
        )
