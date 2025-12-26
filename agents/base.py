from abc import ABC, abstractmethod
from types import MoveRequest

class BaseAgent(ABC):
    name: str = "BaseAgent"
    color: str = None

    @abstractmethod
    def choose_move(self, req: MoveRequest):
        """
            Must return a string representing the move from the legal moves list in the Move Request
        """
        raise NotImplementedError

    def set_color(self, color: str):
        self.color = color
