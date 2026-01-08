import random

from agents.agents_types import MoveRequest

class RandomAgent:
    name = "Random"

    def choose_move(self, req: MoveRequest):
        return random.choice(req.legal_move_list)