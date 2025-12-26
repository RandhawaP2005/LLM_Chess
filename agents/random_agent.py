import random

from base import BaseAgent
from types import MoveRequest

class RandomAgent(BaseAgent):
    name = "Random"

    def choose_move(self, req: MoveRequest):
        return random.choice(req.legal_move_list)