from typing import Literal

from pydantic import BaseModel, Field


class IntentClassifier(BaseModel):
    msg_intent: Literal["Vacancy", "Company", "Helper", "Unrelated"] = Field(
        ...,
        description=(
            "Vacancy - the question is about the job itself: responsibilities, requirements, "
            "salary, location, schedule, employment type, deadline, hiring process. "
            "Company - the question is about the employer: what the company does, its culture, "
            "website, size, products. "
            "Helper - the candidate greets the assistant or asks about the assistant itself: "
            "who it is, what it can do, how it can help, how to use this chat. "
            "Unrelated - anything that is not about this job or this company."
        ),
    )
