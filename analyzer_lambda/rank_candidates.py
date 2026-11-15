import json

from candidates import Candidate
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from config import LLM_MODEL, settings
from hr_core.models.vacancy_model import Vacancy
from output_model import RankedCandidate, RankingOutput, validate_ranking

SYSTEM_PROMPT = """You are an HR assistant that ranks candidates for a job vacancy.

Vacancy:
{vacancy}

You receive a JSON list of candidates. Each candidate has:
- application_id: the candidate identifier
- resume_score: 0-100 score of the CV against the vacancy
- resume_review: explanation of that score
- answers: the candidate's answers to the screening questions (video answers are transcriptions)

Workflow:
1. Evaluate every candidate against the vacancy requirements using the CV review and the answers.
2. Compare the candidates with each other, not in isolation.
3. Return a ranking that contains EVERY candidate exactly once.

Rules:
- order is the place in the ranking: 1 is the best candidate, orders go 1..N without gaps or duplicates.
- resume_score is an important signal but not the only one: weak, evasive or irrelevant answers must lower the place, strong answers can raise it.
- Video answers are speech transcriptions, ignore filler words and minor transcription errors.
- The summary explains in 3-5 sentences why the candidate got this place relative to the others. Summary must be in English.
- Use only application_id to refer to candidates."""  # noqa: E501


def rank_candidates(vacancy: Vacancy, candidates: list[Candidate]) -> list[RankedCandidate]:
    agent = create_agent(
        model=init_chat_model(LLM_MODEL, google_api_key=settings.google_api_key),
        system_prompt=SYSTEM_PROMPT.format(
            vacancy=vacancy.model_dump_json(
                exclude={"id", "created_by", "status", "selection_status", "created_at"}
            )
        ),
        response_format=RankingOutput,
    )
    content = json.dumps([c.model_dump() for c in candidates], ensure_ascii=False)
    response = agent.invoke({"messages": [{"role": "user", "content": content}]})
    return validate_ranking(response["structured_response"], {c.application_id for c in candidates})
