from abc import ABC, abstractmethod


class INotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient: str, subject: str, body: str) -> None: ...
