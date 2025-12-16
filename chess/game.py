import chess
import chess.pgn
from pathlib import Path

# Game class housing board
class Game:
    def __init__(self):
        self.board = chess.Board()

    def check_legal(self, move):
        if move in self.board.legal_moves:
            return True
        else:
            return False

    def make_move(self, move):
        move = chess.Move.from_uci(move)
        if self.check_legal(move):
            self.board.push(move)
        else:
            # TODO: Finish else statement later on
            ''
    def get_pgn(self):
        return str(chess.pgn.Game.from_board(self.board))

    def save_pgn(self):
        loc = Path("../pgn")
        loc.mkdir(parents=True, exist_ok=True)

        with open("../pgn/first.pgn", "w", encoding= 'utf-8') as f:
            f.write(self.get_pgn())