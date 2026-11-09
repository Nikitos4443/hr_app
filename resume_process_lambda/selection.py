def pick_candidate_to_reject(
    scores: dict[int, float], min_candidates: int, threshold: float
) -> int | None:
    if len(scores) <= min_candidates:
        return None

    below_threshold = {
        application_id: score for application_id, score in scores.items() if score < threshold
    }
    if not below_threshold:
        return None

    return min(below_threshold, key=lambda application_id: (below_threshold[application_id], application_id))
