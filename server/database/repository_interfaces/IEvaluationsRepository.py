from abc import ABC, abstractmethod

from database.models.evaluation_model import Evaluation


class IEvaluationsRepository(ABC):
    @abstractmethod
    def create(self, entity: Evaluation) -> Evaluation: ...
