import logging

from event_parser import parse_vacancy_id
from load_data import get_candidates, get_vacancy, set_selection_status
from rank_candidates import rank_candidates
from save_to_db import save_evaluations

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def index(event, context):
    vacancy_id = parse_vacancy_id(event)
    vacancy = get_vacancy(vacancy_id)
    set_selection_status(vacancy_id, "running")
    try:
        candidates = get_candidates(vacancy_id)
        if not candidates:
            logger.info("Vacancy %s has no candidates ready for ranking", vacancy_id)
        else:
            ranking = rank_candidates(vacancy, candidates)
            save_evaluations(vacancy_id, ranking)
            logger.info(
                "Ranked %s candidates for vacancy %s: %s",
                len(ranking),
                vacancy_id,
                [item.application_id for item in ranking],
            )
    except Exception:
        set_selection_status(vacancy_id, "failed")
        raise

    set_selection_status(vacancy_id, "done")
    return {"statusCode": 200}
