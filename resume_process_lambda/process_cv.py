import logging
import time

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain.tools import tool
from langchain_community.document_loaders import PyPDFLoader

from database import get_vacancy
from output_model import OutputModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SYSTEM_PROMPT = """You are an HR assistant that scores how well a CV matches a job vacancy.

Workflow:
1. Call the "get_vacancy" tool exactly once with vacancy id `{vacancy_id}`. Never call it again.
2. Compare the CV against the vacancy: requirements, responsibilities, years of experience and nice-to-have skills.
3. Return the final numerical assessment.

Scoring rules:
- The score is a number from 0 to 100. Be strict. 100 means a perfect match on every requirement.
- Missing a hard requirement must significantly lower the score.
- The description explains the score in 5-6 sentences. Description must be in English."""  # noqa: E501


@tool(
    "get_vacancy",
    description=(
        "Get full vacancy data from mongo by id. "
        "The result is complete, call only once."
    ),
)
def get_job(id: str) -> dict:
    vacancy = get_vacancy(id)
    if vacancy is None:
        return {"error": f"Vacancy {id} not found"}
    return vacancy


def process_cv(path, id):
    print(f"Path: {path}, id: {id}")
    load_dotenv()
    docs = PyPDFLoader(path, mode="single").load()
    print("Creating agent")
    agent = create_agent(
        model="google_genai:gemini-3.5-flash-lite",
        tools=[get_job],
        system_prompt=SYSTEM_PROMPT.format(vacancy_id=id),
        response_format=OutputModel,
        middleware=[ToolCallLimitMiddleware(tool_name="get_vacancy", run_limit=1)],
    )

    print("Invoking agent")
    start = time.perf_counter()

    response = agent.invoke(
        {"messages": [{"role": "user", "content": docs[0].page_content}]}
    )
    logger.info("agent.invoke took %.3fs", time.perf_counter() - start)
    return response["structured_response"]
