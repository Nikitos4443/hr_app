def parse_vacancy_id(event) -> int:
    try:
        return int(event["vacancy_id"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"event must contain integer 'vacancy_id', got: {event!r}") from error
