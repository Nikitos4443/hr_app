from dataclasses import dataclass

from hr_core.models.company_model import Company
from hr_core.models.vacancy_model import Vacancy


@dataclass
class ChatContext:
    vacancy: Vacancy
    company: Company | None
