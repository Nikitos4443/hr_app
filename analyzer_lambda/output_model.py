from pydantic import BaseModel, Field


class RankedCandidate(BaseModel):
    application_id: int = Field(description="application_id of the candidate")
    order: int = Field(description="Place in the ranking, 1 is the best candidate")
    summary: str = Field(description="Why the candidate got this place, 3-5 sentences, English")


class RankingOutput(BaseModel):
    ranking: list[RankedCandidate]


def validate_ranking(output: RankingOutput, application_ids: set[int]) -> list[RankedCandidate]:
    ranking = sorted(output.ranking, key=lambda item: item.order)
    if {item.application_id for item in ranking} != application_ids or len(ranking) != len(
        application_ids
    ):
        raise ValueError("LLM ranking must contain every candidate exactly once")
    if [item.order for item in ranking] != list(range(1, len(ranking) + 1)):
        raise ValueError("LLM ranking orders must be 1..N without gaps or duplicates")
    return ranking
