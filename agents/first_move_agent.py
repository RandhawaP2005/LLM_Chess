from base_agent import BaseAgent
from agents.agents_types import MoveRequest

class FirstMoveAgent:
    name = "First Move"

    def choose_move(self, req: MoveRequest):
        return req.legal_move_list[0]