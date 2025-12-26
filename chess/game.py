from __future__ import annotations

import io
from datetime import date

import chess
import chess.pgn
import os

def is_fen(fen:str) -> bool:
    try:
        chess.Board(fen)
        return True
    except ValueError:
        return False

# Game class housing board
class Game:
    def __init__(self, position: str | None = None):
        self.game_over = False

        if position is None:
            self.board = chess.Board()
            self.game = chess.pgn.Game.from_board(self.board)
            self.game_node = self.game
            return

        if is_fen(position):
            self.board = chess.Board(position)
            self.game = chess.pgn.Game.from_board(self.board)
            self.game_node = self.game
            self.check_status()
            return

        game = chess.pgn.read_game(io.StringIO(position))
        if game:
            self.game = game
            self.game_node = game
            self.board = game.board()

            for move in self.game.mainline_moves():
                self.board.push(move)

            self.check_status()
            return

        raise ValueError("Input is neither valid FEN nor valid PGN.")

    def check_legal(self, move):
        if move in self.board.legal_moves:
            return True
        else:
            return False

    def make_move(self, move):
        if self.game_over:
            raise ValueError("Game is already over.")
        else:
            move = chess.Move.from_uci(move)
            if self.check_legal(move):
                self.game_node = self.game_node.add_main_variation(move)
                self.board.push(move)
                status = self.check_status()
                if status:
                    print(f"Game over. {status}")
            else:
                raise ValueError(f"Illegal move: {move}")

    def check_status(self):
        if self.board.is_checkmate():
            if not self.game_over:
                self.game_over = True
            return "Checkmate"
        if self.board.is_stalemate():
            if not self.game_over:
                self.game_over = True
            self.draw_reason = "Stalemate"
            return self.draw_reason
        if self.board.is_insufficient_material():
            if not self.game_over:
                self.game_over = True
            self.draw_reason = "Insufficient Material"
            return self.draw_reason
        if self.board.is_fifty_moves():
            if not self.game_over:
                self.game_over = True
            self.draw_reason = "50-move Rule"
            return self.draw_reason
        if self.board.is_repetition():
            if not self.game_over:
                self.game_over = True
            self.draw_reason = "Threefold Repetition"
            return self.draw_reason
        return None

    def get_pgn(self):
        return str(chess.pgn.Game.from_board(self.board))

    def get_fen(self):
        return self.board.fen()

    def get_turn(self):
        if self.board.turn == chess.WHITE:
            return "White"
        else:
            return "Black"

    def is_in_check(self):
        return self.board.is_check()

    def game_result(self):
        result = self.board.result()
        if result == "1-0":
            return "White wins"
        elif result == "0-1":
            return "Black wins"
        elif result == "*" and self.game_over != True:
            return "Game is still in progress"
        else:
            return f"Draw: {self.draw_reason}"

    def save_pgn(self):
        white = self.game.headers.get("White")
        black = self.game.headers.get("Black")
        today = date.today().strftime("%Y.%m.%d")
        self.game.headers["Date"] = today
        self.game.headers["Result"] = self.board.result()

        if white == "?":
            sanitized_white = "White"
        else:
            sanitized_white = white.replace(" ", "_")
        if black == "?":
            sanitized_black = "Black"
        else:
            sanitized_black = black.replace(" ", "_")


        base_name = f"{today}_{sanitized_white}_vs_{sanitized_black}"
        filename = f"{base_name}.pgn"
        path = f"../pgn/{filename}"

        counter = 1
        while os.path.exists(path):
            filename = f"{base_name}_{counter}.pgn"
            path = f"../pgn/{filename}"
            counter += 1

        try:
            with open(path, "x", encoding="utf-8") as f:
                exporter = chess.pgn.FileExporter(f)
                self.game.accept(exporter)
        except FileExistsError:
            raise FileExistsError

        print(f"Game Saved: {filename}")