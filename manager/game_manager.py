import chess

import chess_game.game as g
import agents.types as types
import agents.base as base


def verify_move(move, move_list: list):
    if not isinstance(move, str):
        raise TypeError("Expected string but got {}".format(type(move)))

    try:
        chess.Move.from_uci(move)
    except ValueError:
        raise ValueError("Expected single uci but got {}".format(move))

    if move not in move_list:
        raise ValueError("Move not in valid list{}".format(move))

    return True


class GameManager:
    def __init__(self, game: g.Game, agent1: base.BaseAgent, agent2: base.BaseAgent):
        self.game = game
        self.White = agent1
        self.Black = agent2

    def generate_move_req(self) -> types.MoveRequest:
        req = types.MoveRequest(fen= self.game.get_fen(), legal_move_list= self.game.get_moves(), move_history= self.game.get_moves_history())
        return req

    def push_move(self, move):
        if self.game.game_result() != "Game is still in progress":
            raise RuntimeError("Cant push move when game has ended")

        if not self.game.check_legal(move):
            raise ValueError("Illegal move: {}".format(move))

        self.game.make_move(move)

    # TODO: Implement agent failure policy. Discuss and decide the policy for consistency.
    def ask_agent(self):
        while not self.game.game_ended():
            if self.game.get_turn() == "White":
                moves = self.generate_move_req()
                move_returned = self.White.choose_move(moves)
                if verify_move(move_returned, moves.legal_move_list):
                    self.push_move(move_returned)
                continue

            if self.game.get_turn() == "Black":
                moves = self.generate_move_req()
                move_returned = self.Black.choose_move(moves)
                if verify_move(move_returned, moves.legal_move_list):
                    self.push_move(move_returned)

        print(self.game.game_result())
