import unittest

import agents.first_move_agent as first_move_agent
import agents.random_agent as random_agent
import chess_game.game as g
from manager import game_manager as gm
import agents.Llama3_2 as Llama3_2
import agents.human_player as human_player

class TestManager(unittest.TestCase):
    def test(self):
        game = g.Game()
        a1 = random_agent.RandomAgent()
        a2 = random_agent.RandomAgent()

        manager = gm.GameManager(game, agent1 = a1, agent2 = a2)

        manager.ask_agent()
        game.save_pgn()

    def test_llama(self):
        game = g.Game()
        llama =  Llama3_2.Llama3_1()
        p2 = human_player.HumanPlayer()
        a2 = random_agent.RandomAgent()

        manager = gm.GameManager(game, agent1 = llama, agent2 = a2)
        manager.ask_agent()
        game.save_pgn()