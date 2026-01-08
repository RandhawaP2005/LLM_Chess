import io

from game import Game
import chess.pgn
import unittest



class TestChess(unittest.TestCase):
    def test_chess_add_moves(self):
        game = Game()

        game.make_move("e2e4")
        game.make_move("e7e5")

        self.assertEqual(game.board.fen(),chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2").fen())

    def test_chess_load_stalemate(self):
        with open("../pgn/Exaform_vs_punarrandhawa_2025.12.16.pgn", "r", encoding= "utf-8") as f:
            pgn = f.read()
        game = Game(position=pgn, format="PGN")
        self.assertEqual(game.check_status(), "Stalemate")
        self.assertEqual(game.game_result(), "Draw: Stalemate")

        self.assertRaises(ValueError, game.make_move, "Kh1")

    def test_chess_play_checkmate(self):
        game = Game()

        game.make_move("e2e4")
        game.make_move("e7e5")
        game.make_move("d2d4")
        game.make_move("e5d4")
        print(game.get_moves())
        game.make_move("d1d4")
        game.make_move("d7d6")
        game.make_move("f1c4")
        game.make_move("a7a6")
        game.make_move("d4d5")
        game.make_move("b7b6")
        game.make_move("d5f7")


        print(game.get_moves_history())
        self.assertEqual(game.game_result(), "White wins")

    def test_chess_play_three_fold_repetition(self):
        game = Game()

        game.make_move("e2e4")
        game.make_move("e7e5")

        game.make_move("d1e2")
        game.make_move("d8e7")

        game.make_move("e2d1")
        game.make_move("e7d8")

        game.make_move("d1e2")
        game.make_move("d8e7")

        game.make_move("e2d1")
        game.make_move("e7d8")

        print(game.get_moves_history())
        self.assertTrue(game.board.is_repetition())
        self.assertTrue(game.game_over)
        self.assertEqual(game.game_result(), "Draw: Threefold Repetition")

    def test_chess_insufficient_material(self):
        game = Game(position="5N2/8/3K4/8/8/5k2/8/8 w - - 0 1", format="FEN")

        self.assertTrue(game.board.is_insufficient_material())
        self.assertTrue(game.game_over)
        self.assertEqual(game.game_result(), "Draw: Insufficient Material")

    def test_chess_50_moves_rule(self):
        game = Game("4Rr2/8/8/8/8/8/8/K6k w - - 100 1")

        self.assertTrue(game.board.can_claim_fifty_moves())
        self.assertTrue(game.game_over)
        self.assertEqual(game.game_result(), "Draw: 50-move Rule")

    def test_invalid_FEN(self):
        invalid_fens = [
            "8/8/8/8/8/8/8/8 w - -",  # too few fields
            "9/8/8/8/8/8/8/K6k w - - 0 1",  # invalid rank
            "8/8/8/8/8/8/8/K6x w - - 0 1",  # invalid piece
            "8/8/8/8/8/8/8/K6k x - - 0 1",  # invalid side to move
        ]

        for fen in invalid_fens:
            with self.assertRaises(ValueError):
                Game(fen)

        invalid_pgn = """
            [Event "Bad Game"
            [White "A"]
            [Black "B"]

            1. e4 e5
            """
        with self.assertRaises(ValueError):
            game = Game(invalid_pgn)

        invalid_pgn = """
            [Event "Illegal Move"]
            [White "A"]
            [Black "B"]

            1. Qh5 Qh4
            """
        with self.assertRaises(ValueError):
            game = Game(invalid_pgn)
    def test_invalid_move_format_raises(self):
        game = Game()

        invalid_moves = [
            "e2e",     # too short
            "e9e4",    # invalid square
            "e2e4e",   # too long
            "abcd",    # nonsense
            "e2-e4",   # wrong format
        ]

        for mv in invalid_moves:
            with self.assertRaises(ValueError):
                game.make_move(mv)

    def test_illegal_move_raises(self):
        game = Game()

        # From starting position, pawn cannot jump 3 squares
        with self.assertRaises(ValueError):
            game.make_move("e2e5")

        # From starting position, king cannot move like a knight
        with self.assertRaises(ValueError):
            game.make_move("e1f3")

        # Wrong color: black tries to move first
        with self.assertRaises(ValueError):
            game.make_move("e7e5")

    def test_live_game_test(self):
        game = Game()

        print(game.get_moves())
        print(game.get_moves_history())
        self.assertFalse(game.board.is_game_over())