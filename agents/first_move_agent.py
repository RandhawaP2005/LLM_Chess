from base import BaseAgent
from types import MoveRequest

class FirstMoveAgent(BaseAgent):
    name = "First Move"

    def choose_move(self, req: MoveRequest):
        return req.legal_move_list[0]