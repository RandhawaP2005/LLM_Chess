import chess

import chess_game.game as g
import agents.agents_types as ag_types
import agents.base_agent as base


def verify_move(move, move_list: list):
    if not isinstance(move, str):
        raise TypeError("Expected string but got {}".format(type(move)))

    try:
        chess.Move.from_uci(move)
    except TypeError or ValueError:
        raise ValueError("Expected single uci but got {}".format(move))

    if move not in move_list:
        raise ValueError("Move not in valid list{}".format(move))

    return chess.Move.from_uci(move)

# TODO: Decide if color is to be provided in the MoveRequest or set after game starts, or not needed at all
class GameManager:
    def __init__(self, game: g.Game, agent1, agent2):
        self.game = game
        self.White = agent1
        self.Black = agent2

    def generate_move_req(self) -> ag_types.MoveRequest:
        req = ag_types.MoveRequest(fen= self.game.get_fen(), legal_move_list= self.game.get_moves(), move_history= self.game.get_moves_history(), alliance= self.game.get_turn(), game_board= str(self.game.board))
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
            print(self.game.board)# check
            print(self.game.get_moves())
            if self.game.get_turn() == "White":
                print(self.game.get_moves)
                counter = 0
                while counter < 2:
                    moves = self.generate_move_req()
                    move_returned = self.White.choose_move(moves)
                    #print(move_returned + str(type(move_returned)) + "White")
                    try:
                        self.push_move(verify_move(move_returned, moves.legal_move_list))
                        break
                    except ValueError or TypeError:
                        counter += 1
                if counter == 2:
                    raise ValueError("Agent: {} returned invalid move twice. Forfeits game.".format(self.White.name))
                continue

            if self.game.get_turn() == "Black":
                counter = 0
                while counter < 2:
                    moves = self.generate_move_req()
                    move_returned = self.Black.choose_move(moves)
                    #print(move_returned + str(type(move_returned)) + "Black")
                    try:
                        self.push_move(verify_move(move_returned, moves.legal_move_list))
                        break
                    except ValueError or TypeError:
                        counter += 1
                if counter == 2:
                    raise ValueError("Agent: {} returned invalid move twice. Forfeits game".format(self.Black.name))

        print(self.game.game_result())
