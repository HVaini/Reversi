import unittest

from reversi.board import new_board, black_piece, white_piece
from AI.minimax_midgame import minimax_midgame
from AI.ai_move import evaluate_normal


class TestMinimaxMidgame(unittest.TestCase):

    def test_depth_zero_returns_evaluate(self):
        # kun on päästy maksimisyvyyteen niin heuristiikan arvo val palautuu aina
        board = new_board()
        val, move = minimax_midgame(board, black_piece, depth=0, evaluate=evaluate_normal)
        self.assertEqual(val, evaluate_normal(board, black_piece))
        self.assertIsNone(move)

    def test_returns_valid_move_for_positive_depth(self):
        # alkutilanteessa pitäisi aina löytyä siirto tällä syvyydellä
        board = new_board()
        val, move = minimax_midgame(board, black_piece, depth=1, evaluate=evaluate_normal)
        self.assertIsInstance(val, int)
        self.assertIsNotNone(move)
        

    def test_no_legal_moves_passes_turn(self):
        # jos ei siirtoja palautuu valuaatio mutta ei siirtoa
        board = [[black_piece for i in range(8)] for i in range(8)]
        board[0][0] = white_piece  

        val, move = minimax_midgame(board, white_piece, depth=1, evaluate=evaluate_normal)
        self.assertIsInstance(val, int)
        self.assertIsNone(move)

    def test_depth_two_runs_without_error(self):
        # palautuuko siirto alkutilanteesta syvyydellä 2
        board = new_board()
        val, move = minimax_midgame(board, black_piece, depth=2, evaluate=evaluate_normal)
        self.assertIsInstance(val, int)
        self.assertIsNotNone(move)

