from typing import Literal

from pydantic import BaseModel, Field


class IntentClassifier(BaseModel):
    msg_intent: Literal["Vacancy", "Company", "Unrelated"] = Field(
        ...,
        description=(
            "Vacancy - the question is about the job itself: responsibilities, requirements, "
            "salary, location, schedule, employment type, deadline, hiring process. "
            "Company - the question is about the employer: what the company does, its culture, "
            "website, size, products. "
            "Unrelated - anything that is not about this job or this company."
        ),
    )
