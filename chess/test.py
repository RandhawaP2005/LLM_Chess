from game import Game

if __name__ == "__main__":
    game = Game()

    game.make_move("e2e4")

    print(game.get_pgn())

    game.save_pgn()