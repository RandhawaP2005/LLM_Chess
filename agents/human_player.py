from agents.agents_types import MoveRequest


class HumanPlayer:
    name = "Human Player"

    def choose_move(self, move: MoveRequest):
        move = str(input("Enter your move: "))
        return move