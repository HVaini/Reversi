import unittest
from reversi.board import new_board, black_piece, white_piece
from AI.iterative_deepening_midgame import iterative_deepening_midgame
from AI.ai_move import evaluate_normal


class TestIterativeDeepening(unittest.TestCase):

    def test_iterative_deepening_time_limit_zero(self):
        board = new_board()

        val, move, depth = iterative_deepening_midgame(
            board,
            black_piece,
            evaluate=evaluate_normal,
            time_limit=0.0,
            max_depth=5
        )

        self.assertEqual(val, 0)
        self.assertIsNone(move)
        self.assertEqual(depth, 0)

    def test_iterative_deepening_time_runs_out(self):
        board = new_board()

        
        val, move, depth = iterative_deepening_midgame(
            board,
            black_piece,
            evaluate=evaluate_normal,
            time_limit=0.1,
            max_depth=50,
        )

        
        self.assertTrue(depth <= 7)

    def test_midgame_win_cutoff(self):
    
        #todistetusti voitollinen mutta monimutkainen tilanne
        board = [
            ['.','.','O','O','O','O','O','O'],
            ['.','.','O','O','O','O','O','O'],
            ['O','X','O','O','X','O','O','O'],
            ['O','O','X','X','O','X','O','O'],
            ['O','O','O','O','O','O','O','O'],
            ['O','O','O','O','O','O','O','O'],
            ['.','.','O','O','O','O','.','.'],
            ['.','.','O','O','O','O','.','.'],
        ]

        val, move, depth = iterative_deepening_midgame(
            board,
            white_piece,
            evaluate=evaluate_normal,
            time_limit=4.0,
            max_depth=60
        )

        assert move is not None
        assert val >= 100000
        assert depth <= 13