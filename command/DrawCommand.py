from abc import ABC, abstractmethod


class DrawCommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
