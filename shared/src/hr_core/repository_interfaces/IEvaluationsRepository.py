from abc import ABC, abstractmethod

from hr_core.models.evaluation_model import Evaluation


class IEvaluationsRepository(ABC):
    @abstractmethod
    def create(self, entity: Evaluation) -> Evaluation: ...

    @abstractmethod
    def delete_by_application(self, application_id: int) -> None: ...
