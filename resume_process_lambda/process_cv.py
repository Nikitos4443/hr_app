from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader

from config import MAX_PAGES, settings
from hr_core.models.vacancy_model import Vacancy
from output_model import OutputModel

SYSTEM_PROMPT = """You are an HR assistant that scores how well a CV matches a job vacancy.

Vacancy:
{vacancy}

Workflow:
1. Decide whether the document is a CV/resume at all. If it is not, set is_resume to false, score to 0 and explain in the description what the document is.
2. Compare the CV against the vacancy: requirements, responsibilities, years of experience and nice-to-have skills.
3. Return the final numerical assessment.

Scoring rules:
- The score is a number from 0 to 100. Be strict. 100 means a perfect match on every requirement.
- Missing a hard requirement must significantly lower the score.
- The description explains the score in 5-6 sentences. Description must be in English."""  # noqa: E501


def process_cv(path: str, vacancy: Vacancy) -> OutputModel:
    pages = PyPDFLoader(path, mode="page").load()[:MAX_PAGES]
    content = "\n\n".join(page.page_content for page in pages)
    agent = create_agent(
        model=init_chat_model(
            "google_genai:gemini-3.5-flash-lite", google_api_key=settings.google_api_key
        ),
        system_prompt=SYSTEM_PROMPT.format(
            vacancy=vacancy.model_dump_json(
                exclude={"id", "created_by", "status", "selection_status", "created_at"}
            )
        ),
        response_format=OutputModel,
    )
    response = agent.invoke({"messages": [{"role": "user", "content": content}]})
    return response["structured_response"]
